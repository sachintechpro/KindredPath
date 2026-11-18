import os
import json
import urllib.request
import urllib.error
from datetime import date, datetime
from flask import Flask, request, render_template_string

app = Flask(__name__)
ADMIN_EMAIL = "sachin.techpro@gmail.com"
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "")

BASE = """
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} · KindredPath</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#28352f;--green:#24463f;--sage:#a8b9a5;--gold:#d6a65d;--paper:#faf8f3;--muted:#6c7770;--line:#e6e8e1}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px 'DM Sans',sans-serif}a{color:var(--green)}
.nav{display:flex;justify-content:space-between;align-items:center;padding:22px max(6vw,22px);border-bottom:1px solid var(--line)}
.brand{font:600 25px 'Playfair Display',serif;color:var(--green);text-decoration:none}.brand span{color:var(--gold)}
.nav a:not(.brand){text-decoration:none;font-size:13px;color:var(--muted);margin-left:20px}
.wrap{max-width:1050px;margin:0 auto;padding:56px 24px}.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:45px;align-items:center}
.eyebrow{color:#718276;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700}
h1,h2,h3{font-family:'Playfair Display',serif;font-weight:500}.hero h1{font-size:clamp(38px,5vw,60px);line-height:1.08;letter-spacing:-1.5px;margin:18px 0}
.hero p{color:var(--muted);line-height:1.8;font-size:17px}.panel{background:#fff;border:1px solid var(--line);border-radius:24px;padding:28px;box-shadow:0 14px 40px #263c3010}
.orb{min-height:300px;border-radius:28px;background:radial-gradient(circle at 65% 28%,#e5d2a9 0 12%,transparent 13%),radial-gradient(circle at 38% 60%,#a9b9a5 0 24%,transparent 25%),linear-gradient(145deg,#e9eee5,#f2e9d8);display:flex;align-items:end;padding:28px;color:#34463b;font:500 24px 'Playfair Display',serif}
.btn{display:inline-block;background:var(--green);color:white;border:0;border-radius:999px;padding:14px 23px;text-decoration:none;font-weight:600;cursor:pointer}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field{display:flex;flex-direction:column;gap:7px}.full{grid-column:1/-1}
label{font-size:13px;font-weight:600}input,select,textarea{font:inherit;padding:13px 14px;border:1px solid #dfe4dc;border-radius:12px;background:#fff;color:var(--ink);width:100%}
textarea{min-height:90px;resize:vertical}.hint{font-size:12px;color:var(--muted);line-height:1.7}.notice{padding:14px 16px;border-radius:12px;background:#edf2eb;color:#365247;line-height:1.6;margin:18px 0}
.footer{padding:28px;text-align:center;color:var(--muted);font-size:12px}.error{background:#f8e9e5;color:#823c2d;padding:13px 16px;border-radius:12px;margin-bottom:16px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}.cards .panel p{color:var(--muted);line-height:1.7}
@media(max-width:760px){.hero{grid-template-columns:1fr}.orb{min-height:190px}.wrap{padding:36px 18px}.grid,.cards{grid-template-columns:1fr}.full{grid-column:auto}.nav{padding:18px}}
</style></head><body>
<header class="nav"><a class="brand" href="/">kindred<span>path</span></a><div><a href="/learn">Explore</a><a href="/meet">Request a conversation</a></div></header>
{{ body|safe }}<footer class="footer">KindredPath · Educational resources and thoughtful conversations.<br>Information on this site is general education, not financial, tax, legal, or insurance advice.</footer>
</body></html>
"""

def page(title, body, **ctx):
    return render_template_string(BASE, title=title, body=render_template_string(body, **ctx))

def send_email(to_address, subject, text_body):
    if not RESEND_API_KEY or not FROM_EMAIL:
        raise RuntimeError("Email delivery is not configured yet.")
    payload = {"from": FROM_EMAIL, "to": [to_address], "subject": subject, "text": text_body}
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + RESEND_API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        app.logger.error("Email provider rejected a message (HTTP %s).", exc.code)
        raise RuntimeError("Email delivery failed.") from exc
    except Exception as exc:
        app.logger.error("Email delivery failed: %s", type(exc).__name__)
        raise RuntimeError("Email delivery failed.") from exc

@app.get("/")
def home():
    return page("A clearer next step", """
    <main class="wrap">
      <section class="hero"><div><div class="eyebrow">Learn · Reflect · Connect</div>
        <h1>Make room for the things that matter.</h1>
        <p>Life changes. Priorities shift. KindredPath offers approachable educational resources to help you ask better questions about family priorities, financial confidence, and your next professional chapter.</p>
        <p>Explore at your own pace. When you are ready, request a conversation at a time that works for you.</p>
        <a class="btn" href="/meet">Request a conversation →</a></div>
        <div class="orb">Your next chapter,<br>with a little more clarity.</div>
      </section>
      <section style="margin-top:68px"><div class="eyebrow">Explore the learning paths</div><div class="cards">
        <article class="panel"><h2>Family &amp; future</h2><p>Learn about family conversations, protection concepts, long-term planning, and preparing thoughtful questions for qualified professionals.</p><a href="/learn#family">Explore family topics →</a></article>
        <article class="panel"><h2>Professional growth</h2><p>Explore career direction, business development, mentorship, communication, and building your next opportunity.</p><a href="/learn#career">Explore growth topics →</a></article>
      </div></section>
      <div class="notice">KindredPath is an educational and meeting-introduction website. It does not provide individualized financial, investment, tax, legal, or insurance advice. Product comparisons, recommendations, and personal tax discussions are not published on this website.</div>
    </main>
    """)

@app.get("/learn")
def learn():
    return page("Educational resources", """
    <main class="wrap"><div class="eyebrow">A starting point for learning</div><h1 style="font-size:44px">Good questions create better conversations.</h1>
    <p style="color:var(--muted);line-height:1.8;max-width:760px">Use these general prompts to organize your thinking. They are educational starting points, not recommendations for a particular person or family.</p>
    <div class="cards">
      <section class="panel" id="family"><h2>Family, priorities &amp; planning</h2><ul><li>Which people depend on your time, care, or support?</li><li>What changes might affect your family's priorities over the next few years?</li><li>Which important documents and decisions should your family understand?</li><li>What questions would you like to ask a licensed or qualified professional?</li></ul></section>
      <section class="panel"><h2>Financial confidence</h2><ul><li>How do you distinguish short-term needs from long-term goals?</li><li>What does an emergency reserve mean in general?</li><li>Which financial terms or concepts would you like explained?</li><li>What information should you prepare before a professional consultation?</li></ul></section>
      <section class="panel"><h2>Planning conversations</h2><ul><li>Who should be part of important family conversations?</li><li>How can you make your questions and priorities clear?</li><li>What would make a first meeting useful to you?</li></ul></section>
      <section class="panel" id="career"><h2>Professional growth</h2><ul><li>Which strengths do you want to develop or apply differently?</li><li>What would meaningful progress look like in the next year?</li><li>Which skills, relationships, or experiences could support your goals?</li><li>What kind of mentorship or accountability would help?</li></ul></section>
    </div>
    <div class="notice">For personal financial, insurance, tax, or legal decisions, consult an appropriately licensed or qualified professional. This website does not recommend specific products or strategies.</div>
    <p><a class="btn" href="/meet">Request a conversation →</a></p></main>
    """)

@app.route("/meet", methods=["GET", "POST"])
def meet():
    error = None
    if request.method == "POST":
        # Honeypot field for basic bot filtering. Never persist submitted form data.
        if request.form.get("website", "").strip():
            return page("Request received", "<main class='wrap'><h1>Thank you.</h1><p>Your request has been received.</p></main>")
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        pathway = request.form.get("pathway", "General educational conversation").strip()
        meeting_date = request.form.get("meeting_date", "").strip()
        meeting_time = request.form.get("meeting_time", "").strip()
        timezone_name = request.form.get("timezone", "Pacific Time").strip()
        note = request.form.get("note", "").strip()
        if not name or len(name) > 120 or "@" not in email or len(email) > 254:
            error = "Please enter your name and a valid email address."
        elif not meeting_date or not meeting_time:
            error = "Please choose a preferred date and time."
        else:
            try:
                requested_date = date.fromisoformat(meeting_date)
                datetime.strptime(meeting_time, "%H:%M")
                if requested_date < date.today():
                    raise ValueError()
            except ValueError:
                error = "Please choose a valid future date and time."
        if not error:
            pretty_time = datetime.strptime(meeting_time, "%H:%M").strftime("%I:%M %p")
            details = (
                f"Name: {name}\nEmail: {email}\nTopic: {pathway}\n"
                f"Preferred meeting: {meeting_date} at {pretty_time} ({timezone_name})\n"
                f"Additional note: {note or 'None'}\n\n"
                "This is a meeting-time request, not a confirmed booking. Please reply to coordinate confirmation."
            )
            try:
                send_email(ADMIN_EMAIL, f"KindredPath meeting request — {name}", details)
                send_email(email, "We received your KindredPath conversation request",
                    f"Hello {name},\n\nThank you for contacting KindredPath. We received your request for a conversation about {pathway}. Your preferred time is {meeting_date} at {pretty_time} ({timezone_name}).\n\nThis is not yet a confirmed appointment. We will follow up by email to confirm or suggest another time.\n\nKindredPath")
                return page("Request received", """
                <main class="wrap" style="max-width:700px"><div class="notice">Request sent successfully</div>
                <h1 style="font-size:44px">Thank you, {{name}}.</h1>
                <p style="color:var(--muted);line-height:1.8">A confirmation email has been sent to your inbox, and the request has been emailed to our coordinator. Your selected time is a preference, not a confirmed appointment. We will email you to confirm the time or suggest an alternative.</p>
                <a class="btn" href="/">Return to KindredPath</a></main>
                """, name=name)
            except RuntimeError:
                error = "We could not send your request right now. Please try again later or contact us by email."
    return page("Request a conversation", """
    <main class="wrap" style="max-width:760px"><div class="eyebrow">A simple email-only request</div>
    <h1 style="font-size:43px;margin-bottom:10px">Choose a time to connect.</h1>
    <p class="hint">Share your contact details and a preferred meeting time. We will email you to confirm availability. Submitting this form does not book an appointment automatically.</p>
    {% if error %}<div class="error">{{error}}</div>{% endif %}
    <form class="panel" method="post"><div class="grid">
      <div class="field"><label for="name">Your name *</label><input id="name" name="name" required maxlength="120" autocomplete="name"></div>
      <div class="field"><label for="email">Email address *</label><input id="email" type="email" name="email" required maxlength="254" autocomplete="email"></div>
      <div class="field full"><label for="pathway">What would you like to discuss?</label><select id="pathway" name="pathway"><option>Family &amp; future education</option><option>Financial confidence (general education)</option><option>Professional growth</option><option>General introduction</option></select></div>
      <div class="field"><label for="meeting_date">Preferred date *</label><input id="meeting_date" type="date" name="meeting_date" min="{{today}}" required></div>
      <div class="field"><label for="meeting_time">Preferred time (Pacific) *</label><select id="meeting_time" name="meeting_time" required><option value="">Choose a time</option><option value="09:00">9:00 AM</option><option value="10:00">10:00 AM</option><option value="11:00">11:00 AM</option><option value="12:00">12:00 PM</option><option value="13:00">1:00 PM</option><option value="14:00">2:00 PM</option><option value="15:00">3:00 PM</option><option value="16:00">4:00 PM</option><option value="17:00">5:00 PM</option></select></div>
      <input type="hidden" name="timezone" value="Pacific Time (US)">
      <div class="field full"><label for="note">Anything you'd like us to know? (optional)</label><textarea id="note" name="note" maxlength="1200" placeholder="Please do not include account numbers, Social Security numbers, or sensitive personal information."></textarea></div>
      <div class="field" style="position:absolute;left:-5000px" aria-hidden="true"><label>Leave this empty</label><input name="website" tabindex="-1" autocomplete="off"></div>
      <div class="field full"><button class="btn" type="submit">Email my meeting request →</button><p class="hint">Your form details are used to send these two emails only. KindredPath does not save the submission in a lead database or candidate account.</p></div>
    </div></form></main>
    """, error=error, today=date.today().isoformat())

@app.get("/health")
def health():
    return {"ok": True, "service": "KindredPath", "mode": "stateless-email-only"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
