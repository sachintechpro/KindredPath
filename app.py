import os, json, secrets, hashlib, hmac, urllib.request, urllib.error
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, request, redirect, url_for, session, flash, render_template_string, abort
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
DATABASE_URL = os.environ["DATABASE_URL"]
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
EMAIL_TO = os.environ.get("LEAD_EMAIL_TO", "sachin.techpro@gmail.com")

def db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor, sslmode="require")

def init_db():
    with db() as conn, conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
          id BIGSERIAL PRIMARY KEY, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT, city TEXT,
          pathway TEXT NOT NULL, life_stage TEXT, interests TEXT, timing TEXT,
          notes TEXT, source_agent TEXT, source_campaign TEXT, source_post TEXT,
          whatsapp_consent BOOLEAN NOT NULL DEFAULT FALSE, consent_text TEXT,
          consent_at TIMESTAMPTZ, consent_ip TEXT, status TEXT NOT NULL DEFAULT 'New',
          admin_notes TEXT, last_contacted_at TIMESTAMPTZ
        );
        CREATE TABLE IF NOT EXISTS followups (
          id BIGSERIAL PRIMARY KEY, lead_id BIGINT REFERENCES leads(id) ON DELETE CASCADE,
          due_at TIMESTAMPTZ, channel TEXT, task TEXT NOT NULL, status TEXT DEFAULT 'Open',
          created_at TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS activity_log (
          id BIGSERIAL PRIMARY KEY, lead_id BIGINT REFERENCES leads(id) ON DELETE CASCADE,
          action TEXT NOT NULL, detail TEXT, created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """)

def admin_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("admin"): return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapped

def send_email(lead):
    key = os.environ.get("RESEND_API_KEY")
    sender = os.environ.get("FROM_EMAIL")
    if not key or not sender: return False
    payload = {"from": sender, "to": [EMAIL_TO],
      "subject": f"New KindredPath inquiry — {lead['name']}",
      "text": (f"New inquiry received\\nName: {lead['name']}\\nEmail: {lead['email']}\\n"
               f"Phone: {lead.get('phone') or 'Not provided'}\\nPathway: {lead['pathway']}\\n"
               f"Interests: {lead.get('interests') or 'Not provided'}\\n"
               f"Source: {lead.get('source_agent') or 'Direct'} / {lead.get('source_campaign') or '-'}\\n"
               f"WhatsApp consent: {'Yes' if lead.get('whatsapp_consent') else 'No'}")}
    req = urllib.request.Request("https://api.resend.com/emails", data=json.dumps(payload).encode(),
      headers={"Authorization": "Bearer "+key, "Content-Type":"application/json"}, method="POST")
    try:
        urllib.request.urlopen(req, timeout=12).read()
        return True
    except Exception as e:
        app.logger.warning("Email notification failed: %s", e)
        return False

def send_whatsapp_template(lead, meeting_text):
    token=os.environ.get("WHATSAPP_TOKEN"); phone_id=os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    template=os.environ.get("WHATSAPP_TEMPLATE_NAME"); lang=os.environ.get("WHATSAPP_TEMPLATE_LANG","en_US")
    if not all([token,phone_id,template]) or not lead.get("whatsapp_consent"): return False, "WhatsApp is not configured or consent is absent."
    number="".join(c for c in (lead.get("phone") or "") if c.isdigit())
    if not number: return False, "No phone number is available."
    body={"messaging_product":"whatsapp","to":number,"type":"template",
      "template":{"name":template,"language":{"code":lang},"components":[{"type":"body","parameters":[
        {"type":"text","text":lead["name"][:60]},{"type":"text","text":meeting_text[:200]}]}]}}
    req=urllib.request.Request(f"https://graph.facebook.com/v22.0/{phone_id}/messages",
      data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},method="POST")
    try:
        urllib.request.urlopen(req,timeout=15).read()
        return True,"WhatsApp template message submitted."
    except urllib.error.HTTPError as e:
        return False, f"WhatsApp API returned HTTP {e.code}."
    except Exception:
        return False,"WhatsApp message could not be sent."

BASE = """
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} · KindredPath</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#28352f;--green:#24463f;--sage:#a8b9a5;--gold:#d6a65d;--paper:#faf8f3;--white:#fff;--muted:#6c7770;--line:#e6e8e1}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px 'DM Sans',sans-serif}a{color:var(--green)}.nav{display:flex;justify-content:space-between;align-items:center;padding:22px max(6vw,22px);border-bottom:1px solid var(--line)}.brand{font:600 25px 'Playfair Display',serif;color:var(--green);text-decoration:none;letter-spacing:-.4px}.brand span{color:var(--gold)}.nav a:not(.brand){text-decoration:none;font-size:13px;color:var(--muted);margin-left:20px}.wrap{max-width:1050px;margin:0 auto;padding:56px 24px}.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:45px;align-items:center}.eyebrow{color:#718276;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700}.hero h1{font:500 clamp(38px,5vw,60px)/1.08 'Playfair Display',serif;letter-spacing:-1.5px;margin:18px 0}.hero p{color:var(--muted);line-height:1.8;font-size:17px}.panel{background:#fff;border:1px solid var(--line);border-radius:24px;padding:28px;box-shadow:0 14px 40px #263c3010}.orb{min-height:300px;border-radius:28px;background:radial-gradient(circle at 65% 28%,#e5d2a9 0 12%,transparent 13%),radial-gradient(circle at 38% 60%,#a9b9a5 0 24%,transparent 25%),linear-gradient(145deg,#e9eee5,#f2e9d8);display:flex;align-items:end;padding:28px;color:#34463b;font:500 24px 'Playfair Display',serif}.btn{display:inline-block;background:var(--green);color:white;border:0;border-radius:999px;padding:14px 23px;text-decoration:none;font-weight:600;cursor:pointer}.btn.secondary{background:#eaf0e9;color:var(--green)}.formgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field{display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}label{font-size:13px;font-weight:600}input,select,textarea{font:inherit;padding:13px 14px;border:1px solid #dfe4dc;border-radius:12px;background:#fff;color:var(--ink);width:100%}textarea{min-height:95px;resize:vertical}.hint{font-size:12px;color:var(--muted);line-height:1.6}.check{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.6}.check input{width:auto;margin-top:4px}.flash{padding:12px 16px;background:#f6e9d4;border-radius:12px;margin-bottom:16px}.table{width:100%;border-collapse:collapse;font-size:13px}.table th,.table td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}.table th{color:var(--muted);font-weight:600}.pill{background:#eaf0e9;border-radius:30px;padding:5px 9px;font-size:11px}.footer{padding:28px;text-align:center;color:var(--muted);font-size:12px}.adminnav{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px}.adminnav a{font-size:13px}.stat{font:500 30px 'Playfair Display',serif;color:var(--green)}@media(max-width:760px){.hero{grid-template-columns:1fr}.orb{min-height:190px}.wrap{padding:36px 18px}.formgrid{grid-template-columns:1fr}.field.full{grid-column:auto}.nav{padding:18px}.table{display:block;overflow-x:auto;white-space:nowrap}}
</style></head><body><header class="nav"><a class="brand" href="/">kindred<span>path</span></a><div><a href="/inquire">Start a conversation</a><a href="/admin">Private admin</a></div></header>
{% with messages=get_flashed_messages() %}{% for message in messages %}<div class="wrap" style="padding-top:12px;padding-bottom:0"><div class="flash">{{message}}</div></div>{% endfor %}{% endwith %}
{{ body|safe }}<footer class="footer">KindredPath · A thoughtful first conversation, at your pace.</footer></body></html>
"""

def page(title, body, **ctx):
    return render_template_string(BASE, title=title, body=render_template_string(body, **ctx))

@app.get("/")
def home():
    return page("A clearer next step", """
    <main class="wrap"><section class="hero"><div><div class="eyebrow">A private, thoughtful conversation</div>
    <h1>Make room for the things that matter.</h1><p>Life changes. Priorities shift. KindredPath helps you start a calm, practical conversation about family planning, financial confidence, or your next professional chapter.</p>
    <p>Share only what feels comfortable. We’ll use your note to understand what matters to you and prepare for a personal conversation.</p>
    <a class="btn" href="/inquire">Begin a conversation <span aria-hidden="true">→</span></a></div>
    <div class="orb">Your next chapter,<br>with a little more clarity.</div></section>
    <section style="margin-top:70px"><div class="eyebrow">Two ways to begin</div><div class="formgrid" style="margin-top:18px">
    <div class="panel"><h2 style="font:500 25px 'Playfair Display'">Family &amp; future</h2><p class="hint">Explore family priorities, protection questions, retirement readiness, and planning conversations.</p><a href="/inquire?pathway=Family%20planning">Explore this path →</a></div>
    <div class="panel"><h2 style="font:500 25px 'Playfair Display'">Professional growth</h2><p class="hint">Talk about career direction, business development, mentorship, or building your next opportunity.</p><a href="/inquire?pathway=Professional%20development">Explore this path →</a></div></div></section>
    <p class="hint" style="margin-top:28px">KindredPath is an introduction and meeting-coordination service, not a financial, tax, legal, or insurance advisory service. Any professional recommendations are discussed privately in a meeting after understanding your circumstances.</p></main>
    """)

@app.route("/inquire", methods=["GET","POST"])
def inquire():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip()
        if not name or not email or "@" not in email:
            flash("Please enter your name and a valid email address."); return redirect(url_for("inquire"))
        consent=request.form.get("whatsapp_consent")=="yes"
        consent_text="I agree to receive WhatsApp messages from KindredPath solely to coordinate my requested meeting. I understand I can withdraw consent at any time by replying STOP or contacting us."
        lead={"name":name,"email":email,"phone":request.form.get("phone","").strip(),
          "pathway":request.form.get("pathway","Family planning"),"interests":request.form.get("interests","").strip(),
          "city":request.form.get("city","").strip(),"life_stage":request.form.get("life_stage","").strip(),
          "timing":request.form.get("timing","").strip(),"notes":request.form.get("notes","").strip(),
          "source_agent":request.form.get("source_agent","").strip(),"source_campaign":request.form.get("source_campaign","").strip(),
          "source_post":request.form.get("source_post","").strip(),"whatsapp_consent":consent}
        with db() as conn, conn.cursor() as cur:
            cur.execute("""INSERT INTO leads(name,email,phone,city,pathway,life_stage,interests,timing,notes,source_agent,source_campaign,source_post,whatsapp_consent,consent_text,consent_at,consent_ip)
            VALUES(%(name)s,%(email)s,%(phone)s,%(city)s,%(pathway)s,%(life_stage)s,%(interests)s,%(timing)s,%(notes)s,%(source_agent)s,%(source_campaign)s,%(source_post)s,%(whatsapp_consent)s,%(consent_text)s,%(consent_at)s,%(consent_ip)s) RETURNING id""",
            {**lead,"consent_text":consent_text if consent else None,"consent_at":datetime.now(timezone.utc) if consent else None,"consent_ip":request.headers.get("X-Forwarded-For",request.remote_addr) if consent else None})
            lead_id=cur.fetchone()["id"]
            cur.execute("INSERT INTO activity_log(lead_id,action,detail) VALUES(%s,%s,%s)",(lead_id,"Inquiry received","Public inquiry form submitted"))
        send_email(lead)
        return redirect(url_for("thanks"))
    path=request.args.get("pathway","Family planning")
    return page("Start a conversation", """
    <main class="wrap" style="max-width:760px"><div class="eyebrow">A few details to help us prepare</div><h1 style="font:500 42px 'Playfair Display';margin:12px 0">Let’s start with what matters to you.</h1><p class="hint">This should take about a minute. You can keep your answers brief and skip anything that doesn’t feel relevant.</p>
    <form class="panel" method="post"><div class="formgrid">
    <div class="field"><label>Your name *</label><input name="name" required autocomplete="name" placeholder="First and last name"></div>
    <div class="field"><label>Email address *</label><input type="email" name="email" required autocomplete="email" placeholder="you@example.com"></div>
    <div class="field"><label>Mobile number</label><input name="phone" autocomplete="tel" placeholder="+1 (555) 555-5555"></div>
    <div class="field"><label>City (optional)</label><input name="city" placeholder="City, State"></div>
    <div class="field full"><label>What would you like to discuss?</label><select name="pathway"><option {{'selected' if path=='Family planning' else ''}}>Family planning</option><option {{'selected' if path=='Professional development' else ''}}>Professional development</option><option>Both / Not sure yet</option></select></div>
    <div class="field"><label>What stage are you in?</label><select name="life_stage"><option value="">Prefer not to say</option><option>Growing family / new child</option><option>Caring for parents or family</option><option>Building financial confidence</option><option>Approaching retirement</option><option>Career or business transition</option><option>Exploring options</option></select></div>
    <div class="field"><label>When would you like to connect?</label><select name="timing"><option>As soon as practical</option><option>Within the next 2 weeks</option><option>Within a month</option><option>Just exploring</option></select></div>
    <div class="field full"><label>What topics are on your mind?</label><textarea name="interests" placeholder="For example: caring for aging parents, a new baby, retirement planning, career growth..."></textarea></div>
    <div class="field full"><label>Anything else you’d like us to know? (optional)</label><textarea name="notes" placeholder="A little context helps us make the conversation useful. Please avoid account numbers, Social Security numbers, or medical details."></textarea></div>
    <input type="hidden" name="source_agent" value="{{request.args.get('agent','')}}"><input type="hidden" name="source_campaign" value="{{request.args.get('campaign','')}}"><input type="hidden" name="source_post" value="{{request.args.get('post','')}}">
    <div class="field full"><label class="check"><input type="checkbox" name="whatsapp_consent" value="yes"><span><strong>Optional WhatsApp consent:</strong> I agree to receive WhatsApp messages from KindredPath solely to coordinate my requested meeting. I understand I can withdraw consent at any time by replying STOP or contacting us. This is not consent to promotional messages.</span></label><p class="hint">Leave unchecked if you prefer email or phone. Your inquiry will still be submitted.</p></div>
    <div class="field full"><button class="btn" type="submit">Send my note →</button><p class="hint">By submitting, you ask us to contact you about this inquiry. Please share only information you are comfortable providing.</p></div></div></form></main>
    """, path=path)

@app.get("/thanks")
def thanks():
    return page("Thank you", """<main class="wrap" style="max-width:680px;text-align:center"><div class="orb" style="min-height:180px;justify-content:center;margin-bottom:30px">Thank you for reaching out.</div><h1 style="font:500 42px 'Playfair Display'">Your next step starts with a conversation.</h1><p style="color:var(--muted);line-height:1.8">Your note has been received. We’ll review what you shared and follow up to coordinate a suitable time. No product recommendations or tax analysis will be sent through this form; any relevant discussion takes place privately in your meeting.</p><a class="btn" href="/">Back to KindredPath</a></main>""")

@app.get("/login")
def login():
    return page("Admin sign in", """<main class="wrap" style="max-width:430px"><div class="panel"><h1 style="font:500 32px 'Playfair Display'">Private workspace</h1><form method="post" action="/login"><div class="field"><label>Username</label><input name="username" required></div><div class="field" style="margin-top:14px"><label>Password</label><input type="password" name="password" required></div><button class="btn" style="margin-top:20px">Sign in</button></form></div></main>""")

@app.post("/login")
def login_post():
    u=request.form.get("username",""); p=request.form.get("password","")
    valid_user=hmac.compare_digest(u,ADMIN_USER)
    valid_pass=bool(ADMIN_PASSWORD) and hmac.compare_digest(p,ADMIN_PASSWORD)
    if ADMIN_PASSWORD_HASH:
        valid_pass=valid_pass or hmac.compare_digest(hashlib.sha256(p.encode()).hexdigest(),ADMIN_PASSWORD_HASH)
    if valid_user and valid_pass:
        session.clear(); session["admin"]=True; return redirect(request.args.get("next") or url_for("admin"))
    flash("Sign-in failed."); return redirect(url_for("login"))

@app.get("/logout")
def logout():
    session.clear(); return redirect(url_for("home"))

@app.get("/admin")
@admin_required
def admin():
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) total, COUNT(*) FILTER (WHERE status='New') new_count, COUNT(*) FILTER (WHERE whatsapp_consent) wa_count FROM leads")
        stats=cur.fetchone()
        cur.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT 150")
        leads=cur.fetchall()
    return page("Lead workspace", """<main class="wrap"><div class="eyebrow">Private admin workspace</div><h1 style="font:500 38px 'Playfair Display'">Inquiry overview</h1><div class="adminnav"><a href="/admin">Leads</a><a href="/logout">Sign out</a></div><div class="formgrid" style="margin-bottom:25px"><div class="panel"><div class="stat">{{stats.total}}</div><div class="hint">Total inquiries</div></div><div class="panel"><div class="stat">{{stats.new_count}}</div><div class="hint">New inquiries · {{stats.wa_count}} WhatsApp opt-ins</div></div></div><div class="panel"><table class="table"><thead><tr><th>Candidate</th><th>Pathway / intent</th><th>Source</th><th>Status</th><th>Received</th></tr></thead><tbody>{% for l in leads %}<tr><td><a href="/admin/lead/{{l.id}}"><strong>{{l.name}}</strong></a><br>{{l.email}}<br>{{l.phone or ''}}</td><td>{{l.pathway}}<br>{{l.interests or ''}}</td><td>{{l.source_agent or 'Direct'}}<br>{{l.source_campaign or ''}}</td><td><span class="pill">{{l.status}}</span></td><td>{{l.created_at.strftime('%b %d, %Y')}}</td></tr>{% else %}<tr><td colspan="5">No inquiries yet.</td></tr>{% endfor %}</tbody></table></div></main>""", stats=stats, leads=leads)

@app.get("/admin/lead/<int:lead_id>")
@admin_required
def lead_detail(lead_id):
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM leads WHERE id=%s",(lead_id,)); lead=cur.fetchone()
        if not lead: abort(404)
        cur.execute("SELECT * FROM followups WHERE lead_id=%s ORDER BY due_at NULLS LAST",(lead_id,)); tasks=cur.fetchall()
        cur.execute("SELECT * FROM activity_log WHERE lead_id=%s ORDER BY created_at DESC",(lead_id,)); logs=cur.fetchall()
    return page("Inquiry detail", """<main class="wrap"><div class="adminnav"><a href="/admin">← All inquiries</a><a href="/logout">Sign out</a></div><div class="eyebrow">Private candidate record · #{{lead.id}}</div><h1 style="font:500 38px 'Playfair Display'">{{lead.name}}</h1><div class="formgrid"><section class="panel"><h3>Contact &amp; intent</h3><p>{{lead.email}}<br>{{lead.phone or 'No phone'}}<br>{{lead.city or ''}}</p><p><b>Pathway:</b> {{lead.pathway}}<br><b>Life stage:</b> {{lead.life_stage or 'Not specified'}}<br><b>Timing:</b> {{lead.timing or 'Not specified'}}</p><p><b>Topics:</b><br>{{lead.interests or 'Not provided'}}</p><p><b>Additional context:</b><br>{{lead.notes or 'Not provided'}}</p><p><b>Source:</b> {{lead.source_agent or 'Direct'}} / {{lead.source_campaign or '-'}} / {{lead.source_post or '-'}}</p><p><b>WhatsApp consent:</b> {{'Yes' if lead.whatsapp_consent else 'No'}}<br><span class="hint">{{lead.consent_text or 'No WhatsApp consent recorded'}}</span></p></section><section class="panel"><h3>Internal assessment &amp; follow-up</h3><form method="post" action="/admin/lead/{{lead.id}}/update"><div class="field"><label>Pipeline status</label><select name="status">{% for s in ['New','Contacted','Meeting scheduled','Meeting completed','Nurture','Closed'] %}<option {{'selected' if lead.status==s else ''}}>{{s}}</option>{% endfor %}</select></div><div class="field" style="margin-top:14px"><label>Private admin notes (never sent to candidate)</label><textarea name="admin_notes">{{lead.admin_notes or ''}}</textarea></div><button class="btn" style="margin-top:15px">Save updates</button></form><hr style="border:0;border-top:1px solid var(--line);margin:25px 0"><h3>WhatsApp meeting coordination</h3>{% if lead.whatsapp_consent %}<form method="post" action="/admin/lead/{{lead.id}}/whatsapp"><div class="field"><label>Meeting coordination details</label><input name="meeting_text" required placeholder="Proposed time: Thursday at 3:00 PM PT"></div><button class="btn secondary" style="margin-top:12px">Send approved template</button><p class="hint">Requires configured Meta WhatsApp Cloud API and an approved template. No message is sent without the stored opt-in.</p></form>{% else %}<p class="hint">Not available: the candidate did not opt in to WhatsApp.</p>{% endif %}</section></div><section class="panel" style="margin-top:20px"><h3>Follow-up task</h3><form method="post" action="/admin/lead/{{lead.id}}/followup" class="formgrid"><div class="field"><label>Task</label><input name="task" required placeholder="Prepare meeting agenda"></div><div class="field"><label>Due date</label><input type="date" name="due_date"></div><div class="field"><label>Channel</label><select name="channel"><option>Email</option><option>Phone</option><option>WhatsApp</option><option>Meeting</option></select></div><div class="field" style="justify-content:end"><button class="btn">Add follow-up</button></div></form><h3>Open tasks</h3>{% for t in tasks %}<p>{{t.task}} · {{t.channel or '—'}} · {{t.due_at.strftime('%b %d, %Y') if t.due_at else 'No date'}} · {{t.status}}</p>{% else %}<p class="hint">No follow-up tasks.</p>{% endfor %}<h3>Activity history</h3>{% for x in logs %}<p class="hint">{{x.created_at.strftime('%b %d %H:%M')}} · {{x.action}} — {{x.detail or ''}}</p>{% endfor %}</section><p class="hint" style="margin-top:20px">Internal analysis is for meeting preparation only. Do not share preliminary product or tax observations as advice or recommendations.</p></main>""", lead=lead, tasks=tasks, logs=logs)

@app.post("/admin/lead/<int:lead_id>/update")
@admin_required
def update_lead(lead_id):
    with db() as conn, conn.cursor() as cur:
        cur.execute("UPDATE leads SET status=%s,admin_notes=%s WHERE id=%s RETURNING id",(request.form.get("status","New"),request.form.get("admin_notes",""),lead_id))
        if cur.fetchone():
            cur.execute("INSERT INTO activity_log(lead_id,action,detail) VALUES(%s,%s,%s)",(lead_id,"Record updated","Status and internal notes saved"))
    return redirect(url_for("lead_detail",lead_id=lead_id))

@app.post("/admin/lead/<int:lead_id>/followup")
@admin_required
def add_followup(lead_id):
    due=request.form.get("due_date") or None
    with db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO followups(lead_id,task,due_at,channel) SELECT id,%s,%s,%s FROM leads WHERE id=%s",(request.form.get("task"),due,request.form.get("channel"),lead_id))
        cur.execute("INSERT INTO activity_log(lead_id,action,detail) VALUES(%s,%s,%s)",(lead_id,"Follow-up created",request.form.get("task")))
    return redirect(url_for("lead_detail",lead_id=lead_id))

@app.post("/admin/lead/<int:lead_id>/whatsapp")
@admin_required
def whatsapp(lead_id):
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM leads WHERE id=%s",(lead_id,)); lead=cur.fetchone()
    if not lead: abort(404)
    ok,msg=send_whatsapp_template(lead,request.form.get("meeting_text",""))
    flash(msg)
    if ok:
        with db() as conn, conn.cursor() as cur:
            cur.execute("UPDATE leads SET last_contacted_at=NOW() WHERE id=%s",(lead_id,))
            cur.execute("INSERT INTO activity_log(lead_id,action,detail) VALUES(%s,%s,%s)",(lead_id,"WhatsApp sent","Meeting coordination template submitted"))
    return redirect(url_for("lead_detail",lead_id=lead_id))

@app.get("/health")
def health(): return {"ok":True,"service":"KindredPath"}

with app.app_context():
    init_db()

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
