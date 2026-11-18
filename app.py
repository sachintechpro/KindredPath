import os, json, urllib.request, urllib.error
from datetime import date, datetime
from flask import Flask, request, render_template_string

app = Flask(__name__)
ADMIN_EMAIL = "sachin.techpro@gmail.com"
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "")

BASE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} · KindredPath</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#182a2b;--deep:#123b3c;--teal:#176b67;--mint:#dceee8;--coral:#e88b70;--sand:#f5efe4;--paper:#fbfaf7;--muted:#657273;--line:#dfe7e2;--white:#fff;--shadow:0 20px 60px rgba(18,59,60,.10)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px 'DM Sans',sans-serif}a{color:var(--teal)}button,input,select{font:inherit}
.nav{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:17px max(5vw,20px);background:rgba(251,250,247,.92);backdrop-filter:blur(16px);border-bottom:1px solid #dfe7e280}
.brand{font:600 27px Fraunces,serif;color:var(--deep);text-decoration:none;letter-spacing:-.5px}.brand b{color:var(--coral);font-weight:600}.navlinks{display:flex;gap:24px;align-items:center}.navlinks a{text-decoration:none;font-size:13px;color:var(--muted);font-weight:600}.navlinks .pill{background:var(--deep);color:#fff;padding:10px 16px;border-radius:999px}
.wrap{max-width:1180px;margin:auto;padding:68px 24px}.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:55px;align-items:center;min-height:610px}.eyebrow{text-transform:uppercase;letter-spacing:2.5px;font-size:10px;font-weight:800;color:var(--teal)}h1,h2,h3{font-family:Fraunces,serif;font-weight:500;letter-spacing:-.7px}.hero h1{font-size:clamp(44px,6vw,76px);line-height:.98;margin:18px 0}.hero h1 em{font-style:normal;color:var(--coral)}.hero p{color:var(--muted);font-size:18px;line-height:1.8;max-width:670px}.btn{display:inline-flex;align-items:center;gap:8px;background:var(--deep);color:#fff;border:0;border-radius:999px;padding:14px 22px;text-decoration:none;font-weight:700;cursor:pointer}.btn.alt{background:var(--mint);color:var(--deep)}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.hero-art{position:relative;min-height:460px;border-radius:38px;background:linear-gradient(145deg,#dceee8,#f6eadb);overflow:hidden;box-shadow:var(--shadow)}.sun{position:absolute;width:180px;height:180px;border-radius:50%;background:#f2c48f;right:50px;top:45px}.hill{position:absolute;width:500px;height:300px;border-radius:50% 50% 0 0;background:#9fc6b7;bottom:-110px;left:-100px;transform:rotate(-9deg)}.hill2{position:absolute;width:440px;height:250px;border-radius:50% 50% 0 0;background:#5f9990;bottom:-120px;right:-80px;transform:rotate(12deg)}.artcard{position:absolute;left:34px;top:190px;background:#fff;padding:20px 22px;border-radius:20px;box-shadow:0 15px 40px #123b3c22;width:245px}.artcard strong{font:500 25px Fraunces,serif;color:var(--deep)}.artcard small{display:block;color:var(--muted);margin-top:5px}
.section{padding:35px 0 70px}.sectionhead{display:flex;justify-content:space-between;gap:25px;align-items:end;margin-bottom:24px}.sectionhead h2{font-size:40px;margin:7px 0}.sectionhead p{max-width:560px;color:var(--muted);line-height:1.7}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:23px;min-height:190px;transition:.2s;box-shadow:0 5px 20px #123b3c06}.card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}.icon{font-size:26px}.card h3{font-size:23px;margin:12px 0 6px}.card p{color:var(--muted);line-height:1.6;margin:0}.card a{display:inline-block;margin-top:14px;text-decoration:none;font-weight:700;font-size:13px}
.questionband{background:var(--deep);color:#fff;border-radius:34px;padding:45px;display:grid;grid-template-columns:1fr 1fr;gap:35px;align-items:center}.questionband h2{font-size:43px;margin:0}.questionband p{color:#d8e5e1;line-height:1.7}.question{background:#fff;color:var(--ink);padding:15px 18px;border-radius:16px;margin:8px 0;display:flex;justify-content:space-between;gap:10px;text-decoration:none;font-weight:700}.question span{color:var(--coral)}
.lab{background:linear-gradient(135deg,#eef5f1,#f7efe5);border-radius:34px;padding:42px}.lab h2{font-size:43px;margin:6px 0}.lab p{color:var(--muted);line-height:1.7}.labgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:25px}.tool{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;text-decoration:none;color:var(--ink)}.tool h3{margin:7px 0;font-size:22px}.tool p{font-size:13px;margin:0}
.panel{background:#fff;border:1px solid var(--line);border-radius:26px;padding:30px;box-shadow:var(--shadow)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.field{display:flex;flex-direction:column;gap:7px}.full{grid-column:1/-1}label{font-size:13px;font-weight:800}input,select{width:100%;padding:13px 14px;border:1px solid #d7e1db;border-radius:13px;background:#fff;color:var(--ink)}input[type=range]{padding:0;accent-color:var(--teal)}.rangeval{font-weight:800;color:var(--teal)}.result{background:var(--deep);color:#fff;border-radius:22px;padding:25px;margin-top:22px}.result .big{font:500 40px Fraunces,serif;color:#f6c49a}.result small{color:#d8e5e1;line-height:1.6}.notice{padding:15px 17px;border-radius:14px;background:#edf4f0;color:#365755;line-height:1.6;margin:20px 0;font-size:13px}.footer{padding:40px 24px;text-align:center;color:var(--muted);font-size:12px;line-height:1.8;border-top:1px solid var(--line)}
.timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:25px 0}.life{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px}.life strong{display:block;font:500 21px Fraunces,serif}.life small{color:var(--muted)}
@media(max-width:900px){.hero{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}.labgrid{grid-template-columns:1fr 1fr}.questionband{grid-template-columns:1fr}.timeline{grid-template-columns:1fr 1fr}}
@media(max-width:650px){.navlinks a:not(.pill){display:none}.wrap{padding:42px 18px}.hero{min-height:auto}.hero h1{font-size:50px}.hero-art{min-height:330px}.cards,.labgrid,.grid{grid-template-columns:1fr}.full{grid-column:auto}.questionband,.lab{padding:28px}.sectionhead{display:block}.timeline{grid-template-columns:1fr}.artcard{left:20px;top:150px}}
</style></head>
<body>
<header class="nav"><a class="brand" href="/">kindred<b>path</b></a><nav class="navlinks"><a href="/explore">Explore</a><a href="/future-lab">Future Lab</a><a href="/meet" class="pill">Start a conversation</a></nav></header>
{{ body|safe }}
<footer class="footer">KindredPath · Explore. Imagine. Prepare.<br>Educational information only. Calculators use illustrative assumptions and are not financial, tax, legal, insurance, or investment advice. Product availability, terms, costs, and outcomes vary.</footer>
</body></html>
"""

def page(title, body, **ctx):
    return render_template_string(BASE, title=title, body=render_template_string(body, **ctx))

def send_email(to_address, subject, text_body):
    if not RESEND_API_KEY or not FROM_EMAIL:
        raise RuntimeError("Email delivery is not configured yet.")
    payload={"from":FROM_EMAIL,"to":[to_address],"subject":subject,"text":text_body}
    req=urllib.request.Request("https://api.resend.com/emails",data=json.dumps(payload).encode(),headers={"Authorization":"Bearer "+RESEND_API_KEY,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=15) as r:r.read()
    except Exception as exc:
        app.logger.error("Email delivery failed: %s",type(exc).__name__)
        raise RuntimeError("Email delivery failed.") from exc

@app.get("/")
def home():
    return page("Explore your family's future", """
<main class="wrap">
<section class="hero">
<div><div class="eyebrow">Explore · Imagine · Prepare</div>
<h1>Your family's future has <em>more than one chapter.</em></h1>
<p>KindredPath helps you explore the questions behind family protection, education, healthcare, retirement and legacy — with simple explanations and interactive what-if tools.</p>
<div class="actions"><a class="btn" href="/future-lab">Enter the Future Lab →</a><a class="btn alt" href="/explore">Explore family topics</a></div>
</div>
<div class="hero-art"><div class="sun"></div><div class="hill"></div><div class="hill2"></div><div class="artcard"><strong>What if?</strong><small>Small decisions today can change the shape of tomorrow.</small></div></div>
</section>

<section class="section">
<div class="sectionhead"><div><div class="eyebrow">One family. Many questions.</div><h2>Where does your curiosity take you?</h2></div><p>Start with a life question, not a product. Then discover the concepts and conversations that may be relevant.</p></div>
<div class="cards">
<article class="card"><div class="icon">👨‍👩‍👧</div><h3>Family protection</h3><p>What happens to the household if income suddenly changes?</p><a href="/explore#family-protection">Explore →</a></article><article class="card"><div class="icon">🎓</div><h3>Children & education</h3><p>What could education cost by the time your child gets there?</p><a href="/explore#children-and-education">Explore →</a></article><article class="card"><div class="icon">🏥</div><h3>Healthcare & Medicare</h3><p>What costs might still exist after Medicare?</p><a href="/explore#healthcare-and-medicare">Explore →</a></article><article class="card"><div class="icon">👵</div><h3>Aging parents</h3><p>How might caregiving affect a family?</p><a href="/explore#aging-parents">Explore →</a></article><article class="card"><div class="icon">💰</div><h3>Savings & retirement</h3><p>What could consistent saving become over time?</p><a href="/explore#savings-and-retirement">Explore →</a></article><article class="card"><div class="icon">🛡️</div><h3>Unexpected events</h3><p>What happens when illness, disability or an accident interrupts plans?</p><a href="/explore#unexpected-events">Explore →</a></article><article class="card"><div class="icon">🏛️</div><h3>Legacy & estate</h3><p>If you were not here tomorrow, would your wishes be clear?</p><a href="/explore#legacy-and-estate">Explore →</a></article><article class="card"><div class="icon">🏠</div><h3>Home & stability</h3><p>How much financial runway would your household have?</p><a href="/explore#home-and-stability">Explore →</a></article>
</div></section>

<section class="section"><div class="questionband"><div><div class="eyebrow" style="color:#8fd0c6">Start with a question</div><h2>What are you most curious about?</h2><p>Pick a question. We will show you the concept, a practical example and a simple way to explore the numbers.</p></div>
<div><a class="question" href="/future-lab#tool-1">How much could $500/month become?<span>→</span></a><a class="question" href="/future-lab#tool-2">What could college cost in the future?<span>→</span></a><a class="question" href="/future-lab#tool-3">How long could my savings last?<span>→</span></a><a class="question" href="/future-lab#tool-4">What happens if I need long-term care?<span>→</span></a><a class="question" href="/future-lab#tool-5">What does Medicare not cover?<span>→</span></a></div></div></section>

<section class="section"><div class="lab"><div class="eyebrow">Future Lab</div><h2>Change one number. See what happens.</h2><p>Use sliders and ranges to explore hypothetical futures. No login. No pressure. Just a clearer way to think about possibilities.</p><div class="labgrid"><a class="tool" href="/future-lab#tool-1">💰<h3>Future value</h3><p>See what recurring savings could become.</p></a><a class="tool" href="/future-lab#tool-2">🎓<h3>Education gap</h3><p>Explore a hypothetical college funding gap.</p></a><a class="tool" href="/future-lab#tool-3">🛡️<h3>Protection runway</h3><p>Estimate months of household expenses covered.</p></a></div></div></section>
</main>""")

@app.get("/explore")
def explore():
    return page("Explore family topics", """
<main class="wrap"><div class="eyebrow">The Family Journey</div><h1 style="font-size:56px;margin:12px 0">Questions first. Products second.</h1>
<p style="max-width:760px;color:var(--muted);font-size:17px;line-height:1.8">KindredPath explains common financial and insurance concepts in plain language. The goal is to help you recognize questions worth discussing with an appropriately licensed or qualified professional.</p>
<div class="timeline"><div class="life"><strong>👶 Growing</strong><small>Children · education · protection</small></div><div class="life"><strong>🏠 Building</strong><small>Home · income · savings</small></div><div class="life"><strong>🎯 Preparing</strong><small>Retirement · healthcare</small></div><div class="life"><strong>👵 Caring</strong><small>Parents · caregiving · longevity</small></div><div class="life"><strong>🏛️ Leaving</strong><small>Legacy · estate · beneficiaries</small></div></div>
<div class="cards" style="grid-template-columns:repeat(3,1fr)">
<article class="card" id="family-protection" style="min-height:280px"><div class="icon">🛡️</div><h3>Family protection</h3><p><strong>Explore:</strong> Term life, whole life, universal life, IUL, final expense, disability, critical illness, accident, long-term care and umbrella concepts.</p><p style="margin-top:10px"><strong>Example:</strong> A parent with two children may want to understand how income replacement, debts and future education could be addressed if something unexpected happens.</p><a href="/future-lab">Try a related calculator →</a></article><article class="card" id="children-and-education" style="min-height:280px"><div class="icon">🎓</div><h3>Children & education</h3><p><strong>Explore:</strong> 529 plans, custodial accounts, education savings, scholarships, financial aid and education funding strategies.</p><p style="margin-top:10px"><strong>Example:</strong> A family with a 6-year-old can explore how time, monthly contributions and future education costs interact.</p><a href="/future-lab">Try a related calculator →</a></article><article class="card" id="healthcare-and-medicare" style="min-height:280px"><div class="icon">🏥</div><h3>Healthcare & Medicare</h3><p><strong>Explore:</strong> Medicare Part A, Part B, Part C, Part D, Medigap, prescription costs, long-term care and health savings concepts.</p><p style="margin-top:10px"><strong>Example:</strong> Someone approaching Medicare age can explore which types of healthcare costs may remain after Original Medicare.</p><a href="/future-lab">Try a related calculator →</a></article><article class="card" id="aging-parents" style="min-height:280px"><div class="icon">👵</div><h3>Aging parents</h3><p><strong>Explore:</strong> Caregiving, home care, assisted living, nursing care, long-term care insurance and family coordination.</p><p style="margin-top:10px"><strong>Example:</strong> Three siblings helping a parent can explore how care needs might affect household budgets and responsibilities.</p><a href="/future-lab">Try a related calculator →</a></article><article class="card" id="savings-and-retirement" style="min-height:280px"><div class="icon">💰</div><h3>Savings & retirement</h3><p><strong>Explore:</strong> 401(k), Roth IRA, traditional IRA, brokerage accounts, annuities, Social Security, pensions and HSA concepts.</p><p style="margin-top:10px"><strong>Example:</strong> A 40-year-old saving $500 a month can experiment with time and hypothetical return assumptions.</p><a href="/future-lab">Try a related calculator →</a></article><article class="card" id="legacy-and-estate" style="min-height:280px"><div class="icon">🏛️</div><h3>Legacy & estate</h3><p><strong>Explore:</strong> Wills, trusts, beneficiaries, life insurance, charitable giving, estate and business succession concepts.</p><p style="margin-top:10px"><strong>Example:</strong> A parent can explore why beneficiary designations and estate documents matter alongside a broader legacy plan.</p><a href="/future-lab">Try a related calculator →</a></article>
</div>
<div class="notice">Some product names above describe categories rather than recommendations. Insurance and financial products differ by carrier, contract, eligibility, costs, guarantees and risks. Learn the concept first, then discuss your situation with a qualified professional.</div>
</main>""")

@app.get("/future-lab")
def future_lab():
    return page("Future Lab", """
<main class="wrap"><div class="eyebrow">Interactive what-if tools</div><h1 style="font-size:58px;margin:12px 0">Future Lab</h1>
<p style="max-width:760px;color:var(--muted);font-size:17px;line-height:1.8">Move the sliders. Change one assumption. Watch the story change. These are educational illustrations, not forecasts or recommendations.</p>

<section class="panel" id="tool-1" style="margin-top:28px"><div class="eyebrow">01 · Savings</div><h2>What could your monthly saving become?</h2>
<div class="grid">
<div class="field"><label>Monthly contribution <span class="rangeval" id="s1v">$500</span></label><input id="s1" type="range" min="100" max="3000" step="50" value="500"></div>
<div class="field"><label>Years <span class="rangeval" id="s2v">25</span></label><input id="s2" type="range" min="5" max="40" value="25"></div>
<div class="field"><label>Illustrative annual return <span class="rangeval" id="s3v">6%</span></label><input id="s3" type="range" min="2" max="10" step=".5" value="6"></div>
</div><div class="result"><small>Illustrative future value</small><div class="big" id="r1">$346,000</div><small id="r1sub">Contributions: $150,000 · Illustrative growth: $196,000</small></div></section>

<section class="panel" id="tool-2" style="margin-top:22px"><div class="eyebrow">02 · Education</div><h2>What might education cost when your child gets there?</h2>
<div class="grid"><div class="field"><label>Child's age <span class="rangeval" id="e1v">6</span></label><input id="e1" type="range" min="0" max="17" value="6"></div>
<div class="field"><label>Current annual cost <span class="rangeval" id="e2v">$30,000</span></label><input id="e2" type="range" min="10000" max="80000" step="1000" value="30000"></div>
<div class="field"><label>Illustrative inflation <span class="rangeval" id="e3v">3%</span></label><input id="e3" type="range" min="1" max="6" step=".5" value="3"></div>
<div class="field"><label>Current education savings <span class="rangeval" id="e4v">$10,000</span></label><input id="e4" type="range" min="0" max="100000" step="1000" value="10000"></div></div>
<div class="result"><small>Illustrative four-year future education cost</small><div class="big" id="r2">$177,000</div><small id="r2sub">Illustrative gap after current savings: $167,000</small></div></section>

<section class="panel" id="tool-3" style="margin-top:22px"><div class="eyebrow">03 · Protection</div><h2>How many months could your savings cover?</h2>
<div class="grid"><div class="field"><label>Monthly household expenses <span class="rangeval" id="p1v">$6,000</span></label><input id="p1" type="range" min="2000" max="15000" step="250" value="6000"></div>
<div class="field"><label>Accessible savings <span class="rangeval" id="p2v">$30,000</span></label><input id="p2" type="range" min="0" max="250000" step="2500" value="30000"></div>
<div class="field"><label>Income-replacement target <span class="rangeval" id="p3v">12 months</span></label><input id="p3" type="range" min="3" max="36" value="12"></div></div>
<div class="result"><small>Current illustrative runway</small><div class="big" id="r3">5.0 months</div><small id="r3sub">Target: 12 months · Illustrative gap: 7.0 months of expenses</small></div></section>

<div class="notice">These calculators deliberately use simplified assumptions. They do not model taxes, fees, inflation in all cases, investment volatility, insurance underwriting, policy charges, Medicare eligibility, government benefits, college aid, or individual circumstances. Use them to generate questions—not decisions.</div>
</main>
<script>
const money=n=>"$"+Math.round(n).toLocaleString();
function fv(pmt,years,rate){let r=rate/100/12,n=years*12;return r? pmt*((Math.pow(1+r,n)-1)/r):pmt*n}
function bind(id,fmt,fn){const e=document.getElementById(id);const v=document.getElementById(id+"v");e.oninput=()=>{v.textContent=fmt(+e.value);fn()};}
function calc1(){let p=+s1.value,y=+s2.value,r=+s3.value,total=fv(p,y,r),c=p*y*12; r1.textContent=money(total);r1sub.textContent="Contributions: "+money(c)+" · Illustrative growth: "+money(total-c)}
bind("s1",v=>money(v),calc1);bind("s2",v=>v,calc1);bind("s3",v=>v+"%",calc1);calc1();
function calc2(){let age=+e1.value,cost=+e2.value,inf=+e3.value,sav=+e4.value,years=Math.max(0,18-age),future=cost*Math.pow(1+inf/100,years)*4,gap=Math.max(0,future-sav);r2.textContent=money(future);r2sub.textContent="Illustrative gap after current savings: "+money(gap)+" · "+years+" years until age 18"}
bind("e1",v=>v,calc2);bind("e2",v=>money(v),calc2);bind("e3",v=>v+"%",calc2);bind("e4",v=>money(v),calc2);calc2();
function calc3(){let exp=+p1.value,sav=+p2.value,target=+p3.value,months=sav/exp,gap=Math.max(0,target-months);r3.textContent=months.toFixed(1)+" months";r3sub.textContent="Target: "+target+" months · Illustrative gap: "+gap.toFixed(1)+" months of expenses"}
bind("p1",v=>money(v),calc3);bind("p2",v=>money(v),calc3);bind("p3",v=>v+" months",calc3);calc3();
</script>""")

@app.route("/meet", methods=["GET","POST"])
def meet():
    error=None
    if request.method=="POST":
        if request.form.get("website","").strip():
            return page("Request received","<main class='wrap'><h1>Thank you.</h1><p>Your request has been received.</p></main>")
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip()
        pathway=request.form.get("pathway","General educational conversation").strip()
        meeting_date=request.form.get("meeting_date","").strip(); meeting_time=request.form.get("meeting_time","").strip()
        note=request.form.get("note","").strip()
        if not name or len(name)>120 or "@" not in email or len(email)>254:error="Please enter your name and a valid email address."
        elif not meeting_date or not meeting_time:error="Please choose a preferred date and time."
        if not error:
            try:
                d=date.fromisoformat(meeting_date); datetime.strptime(meeting_time,"%H:%M")
                if d<date.today():raise ValueError()
            except ValueError:error="Please choose a valid future date and time."
        if not error:
            pretty=datetime.strptime(meeting_time,"%H:%M").strftime("%I:%M %p")
            details=f"Name: {name}\nEmail: {email}\nTopic: {pathway}\nPreferred meeting: {meeting_date} at {pretty} (Pacific Time)\nNote: {note or 'None'}"
            try:
                send_email(ADMIN_EMAIL,f"KindredPath conversation request — {name}",details)
                send_email(email,"We received your KindredPath request",f"Hello {name},\n\nWe received your request to discuss {pathway}. Preferred time: {meeting_date} at {pretty} Pacific Time. This is a request, not a confirmed appointment.\n\nKindredPath")
                return page("Request received","<main class='wrap'><div class='notice'>Request sent successfully</div><h1 style='font-size:48px'>Thank you, {{name}}.</h1><p style='color:var(--muted);line-height:1.8'>We received your request and will email you to confirm the time or suggest an alternative.</p><a class='btn' href='/'>Return to KindredPath</a></main>",name=name)
            except RuntimeError:error="We could not send your request right now. Please try again later."
    return page("Start a conversation","<main class='wrap' style='max-width:760px'><div class='eyebrow'>Connect</div><h1 style='font-size:48px'>Let's explore the question together.</h1><p style='color:var(--muted);line-height:1.8'>Choose a preferred time. This sends an email request; it does not automatically book an appointment.</p>{% if error %}<div class='notice'>{{error}}</div>{% endif %}<form class='panel' method='post'><div class='grid'><div class='field'><label>Name *</label><input name='name' required maxlength='120'></div><div class='field'><label>Email *</label><input name='email' type='email' required maxlength='254'></div><div class='field full'><label>What are you curious about?</label><select name='pathway'><option>Family & future</option><option>Children & education</option><option>Healthcare & Medicare</option><option>Retirement & savings</option><option>Aging parents</option><option>Legacy & estate</option><option>General introduction</option></select></div><div class='field'><label>Preferred date *</label><input name='meeting_date' type='date' min='{{today}}' required></div><div class='field'><label>Preferred time (Pacific) *</label><select name='meeting_time' required><option value=''>Choose</option><option value='09:00'>9:00 AM</option><option value='10:00'>10:00 AM</option><option value='11:00'>11:00 AM</option><option value='13:00'>1:00 PM</option><option value='14:00'>2:00 PM</option><option value='15:00'>3:00 PM</option><option value='16:00'>4:00 PM</option></select></div><div class='field full'><label>Anything you'd like us to know?</label><input name='note' maxlength='1200' placeholder='Please do not include sensitive personal information.'></div><div style='position:absolute;left:-5000px'><input name='website' tabindex='-1'></div><div class='field full'><button class='btn' type='submit'>Email my request →</button></div></div></form></main>",error=error,today=date.today().isoformat())

@app.get("/health")
def health(): return {"ok":True,"service":"KindredPath","mode":"interactive"}

if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
