#!/usr/bin/env python3
"""Builds the static simonvalentine.com site into the repository root.

Run from the repo root:   python3 _build/build.py

Everything lives in this one file: shared layout (header/footer), page content
and the three articles. Edit the text here, re-run, commit. GitHub Pages ignores
folders starting with an underscore, so this script is never published.
"""
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SV_MARK = re.sub(r'<svg ', '<svg aria-hidden="true" focusable="false" ', (ROOT / "assets/img/sv-mark.svg").read_text().strip(), count=1)
BUILD = Path(__file__).resolve().parent
SITE_URL = "https://simonvalentine.com"
YEAR = 2026

LINKEDIN = "https://www.linkedin.com/in/simonvalentine/"
EMAIL = "contact@simonvalentine.com"
NEWSLETTER = "https://www.linkedin.com/newsletters/talent-acquisition-6884431755651145728/"
TA_EXCHANGE = "https://www.linkedin.com/company/taexchange"
YOUR_PLATFORM = LINKEDIN
ACQUIRE_TALENT = "https://www.linkedin.com/company/acquiretalentpartners/"
PODCAST = "https://soundcloud.com/simonvalentine"
LEADERSHIP_PROGRAM = LINKEDIN

ICON_LINKEDIN = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
ICON_MIC = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>'
ICON_PEOPLE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9" r="2.5"/><path d="M16 14.2A5 5 0 0 1 21.5 19"/></svg>'
ICON_STAR = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'
ICON_NEWS = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h13v14H6a2 2 0 0 1-2-2zM17 9h3v8a2 2 0 0 1-2 2"/><path d="M8 9h5M8 13h5"/></svg>'

NAV = [
    ("about/", "About"),
    ("work/", "Work"),
    ("ventures/", "Ventures"),
    ("articles/", "Articles"),
]

QUOTES = [
    ("Simon always demonstrated innovative ways to approach hiring, be it new tech or resourcing strategies.", "Anish Lalchandani", "HR Leader"),
    ("Simon is one of the hardest working people I have had the pleasure to work with. Very professional and dedicated.", "Dawn Pellar", "Global Leader"),
    ("Simon demonstrated professionalism, innovativeness and work ethic all but assure successful programs.", "Tom Young", "Director"),
]

CLIENTS = ["Manpower", "Costain", "Standard Chartered", "Cisco", "Uber"]

# ---------------------------------------------------------------- articles

ARTICLES = [
    {
        "slug": "the-importance-of-continuous-learning-and-upskilling-for-aspiring-talent-acquisition-leaders",
        "title": "The Importance of Continuous Learning and Upskilling for Aspiring Talent Acquisition Leaders",
        "date": "2023-06-27",
        "date_label": "27 June 2023",
        "summary": "How Talent Acquisition Managers can build the skills, network and mindset to step up into leadership.",
    },
    {
        "slug": "impact-of-ai-on-talent-acquisition-what-you-need-to-know",
        "title": "Impact of AI on Talent Acquisition: What you need to know",
        "date": "2023-05-16",
        "date_label": "16 May 2023",
        "summary": "Where AI already helps recruiters, where it needs care, and what to weigh before you adopt it.",
    },
    {
        "slug": "one-talent-acquisition-community-you-need-to-be-a-part-of-in-2022",
        "title": "One Talent Acquisition community you need to be a part of in 2022",
        "date": "2022-01-05",
        "date_label": "5 January 2022",
        "summary": "Why I started the TA Exchange: a place for Talent Acquisition leaders to collaborate, share and discuss.",
    },
]

SKIP_LINES = {"Simon Valentine", "Subscribe on LinkedIn"}
TEXT_FIXES = {
    "To see the results click here to go to the link of the poll .": None,
    "What do you think about AI in talent acquisition? Let me know in the comments below!":
        'What do you think about AI in talent acquisition? <a href="' + LINKEDIN + '">Tell me on LinkedIn</a>.',
    "https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G":
        '<a href="https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G">Reuters: Amazon scraps secret AI recruiting tool that showed bias against women</a>',
    "These more advanced ways that Ai is being used is where organisations need to be careful… just remember what happened in 2018. See the link below for more context.":
        "These more advanced uses of AI are where organisations need to be careful… just remember what happened in 2018. The article below gives more context.",
    "If are a Talent Acquisition Manager and are considering getting some coaching, being mentored or want to join a community of like-minded Talent Acquisition leaders apply to be a part of the TA Exchange.":
        'If you are a Talent Acquisition Manager and are considering getting some coaching, being mentored or want to join a community of like-minded Talent Acquisition leaders, apply to be a part of the <a href="' + TA_EXCHANGE + '">TA Exchange</a>.',
    "If you are interested to learn more, follow us at TA Exchange Linkedin Company Page or add your email via this link TA Exchange Website to be kept updated.":
        'If you are interested to learn more, follow the <a href="' + TA_EXCHANGE + '">TA Exchange LinkedIn page</a> to be kept updated.',
}


def article_body(slug):
    raw = json.loads((BUILD / "articles_raw.json").read_text())
    key = next(k for k in raw if slug in k)
    out, in_list = [], False
    for tag, text in raw[key]["blocks"]:
        text = text.strip()
        if text in SKIP_LINES or text.startswith("#"):
            continue
        if text in TEXT_FIXES:
            fixed = TEXT_FIXES[text]
            if fixed is None:
                continue
            body = fixed
        else:
            body = html.escape(text, quote=False)
        if tag == "li":
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{body}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        is_heading = tag in ("h2", "h3") or (len(text) < 70 and not text.endswith((".", "?", "!", "…")) and "<a" not in body)
        if is_heading and len(text) > 90:
            is_heading = False
        out.append(f"<h2>{body}</h2>" if is_heading else f"<p>{body}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


# ---------------------------------------------------------------- layout

def rel(depth):
    return "../" * depth


def esc(s):
    return html.escape(s, quote=True)


def header(depth, current):
    r = rel(depth)
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if current == href else ""
        links.append(f'<a href="{r}{href}"{cur}>{label}</a>')
    cur = ' aria-current="page"' if current == "contact/" else ""
    links.append(f'<a class="nav-cta" href="{r}contact/"{cur}>Get in touch</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r or './'}" aria-label="Simon Valentine, home">Simon.</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer(depth):
    r = rel(depth)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-brand">
      <a class="brand" href="{r or './'}" aria-label="Simon Valentine, home">Simon.</a>
      <p>Talent Acquisition advisor, consultant and community leader. Based in Switzerland, working worldwide.</p>
    </div>
    <div>
      <h2>Pages</h2>
      <ul>
        <li><a href="{r}about/">About</a></li>
        <li><a href="{r}work/">Work</a></li>
        <li><a href="{r}articles/">Articles</a></li>
        <li><a href="{r}contact/">Contact</a></li>
      </ul>
    </div>
    <div>
      <h2>Ventures</h2>
      <ul>
        <li><a href="{ACQUIRE_TALENT}">Acquire Talent</a></li>
        <li><a href="{TA_EXCHANGE}">TA Exchange</a></li>
        <li><a href="{YOUR_PLATFORM}">Your Platform</a></li>
      </ul>
    </div>
    <div>
      <h2>Connect</h2>
      <ul>
        <li><a href="{LINKEDIN}">LinkedIn</a></li>
        <li><a href="{NEWSLETTER}">Newsletter</a></li>
        <li><a href="mailto:{EMAIL}">Email</a></li>
        <li><a href="{r}go/">All links</a></li>
      </ul>
    </div>
    <div class="footer-base">
      <span>© {YEAR} Simon Valentine Limited</span>
      <span><a href="{r}privacy-policy/">Privacy</a> &nbsp; <a href="{r}terms-of-service/">Terms</a></span>
    </div>
  </div>
</footer>"""


def page(path, title, description, body, current=None, chrome=True, og_image="simon-lakefront.jpg"):
    """Write one page. `path` is the output directory relative to the root ('' for home)."""
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    r = rel(depth)
    canonical = SITE_URL + "/" + (path if path != "404.html" else "")
    full_title = title if title.startswith("Simon Valentine") else f"{title} | Simon Valentine"
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14212b">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}favicon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css">
</head>
<body>
{header(depth, current) if chrome else '<a class="skip" href="#main">Skip to content</a>'}
<main id="main">
{body.replace('{r}', r)}
</main>
{footer(depth) if chrome else ''}
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
"""
    if path == "404.html":
        out = ROOT / "404.html"
    else:
        out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print("wrote", out.relative_to(ROOT))


def picture(name, alt, cls="", eager=False, sizes="100vw"):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="{{r}}assets/img/{name}.webp" type="image/webp">'
            f'<img{c} src="{{r}}assets/img/{name}.jpg" alt="{esc(alt)}" {loading} decoding="async"></picture>')


def quotes_html():
    items = "".join(
        f'<figure class="quote"><blockquote><p>{esc(q)}</p></blockquote><figcaption>{esc(n)}<span>{esc(role)}</span></figcaption></figure>'
        for q, n, role in QUOTES)
    return f'<div class="quotes">{items}</div>'


def clients_html():
    items = "".join(f"<li>{esc(c)}</li>" for c in CLIENTS)
    return f'<p class="clients-label">Some of the employers, clients and partners I have worked with</p><ul class="clients">{items}</ul>'


def article_list(items):
    rows = "".join(
        f'<li><a href="{{r}}{a["slug"]}/"><time datetime="{a["date"]}">{a["date_label"]}</time><h3>{esc(a["title"])}</h3></a></li>'
        for a in items)
    return f'<ul class="article-list">{rows}</ul>'


def contact_buttons(dark=False):
    return f"""<div class="actions">
  <a class="btn btn-primary" href="{LINKEDIN}">{ICON_LINKEDIN}Message me on LinkedIn</a>
  <a class="btn btn-ghost" href="mailto:{EMAIL}">{ICON_MAIL}Email me</a>
</div>"""


def closing(heading, text):
    return f"""<section class="section band-dark on-dark closing">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    {contact_buttons(dark=True)}
  </div>
</section>"""


# ---------------------------------------------------------------- pages

def build_home():
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>There’s more to hiring than meets the eye.</h1>
      <p class="hero-lede">I help organisations transform how they find and hire talent, through advisory, hands-on consulting and a global community of Talent Acquisition leaders.</p>
      {contact_buttons()}
      <p class="hero-meta">Consultant, advisor, leader and investor. Switzerland, England and New Zealand.</p>
    </div>
    <figure class="hero-photo">{picture('simon-bench-portrait', 'Simon Valentine sitting on a bench by Lake Geneva', eager=True)}</figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>What I do</h2>
      <p>Twenty years inside Talent Acquisition teams, from delivery to global leadership, now put to work for the organisations and people I partner with.</p>
    </div>
    <ul class="services">
      <li><h3>Advisory</h3><div><p>I identify opportunities for organisations to transform their Talent Acquisition function, and give leadership teams straight, practical counsel.</p></div></li>
      <li><h3>Consulting</h3><div><p>I provide solutions that improve your Talent Acquisition function, from diagnosing what is broken to building the processes that fix it.</p><a class="more" href="{{r}}work/">How we would work together</a></div></li>
      <li><h3>Community</h3><div><p>I lead the TA Exchange, an international community of Talent Acquisition leaders who share what works and what doesn’t.</p><a class="more" href="{TA_EXCHANGE}">The TA Exchange on LinkedIn</a></div></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap gallery">
    {picture('simon-old-town', 'Simon Valentine walking through an old town street')}
    {picture('simon-binoculars', 'Simon Valentine looking through binoculars by Lake Geneva')}
    {picture('simon-lake-rail', 'Simon Valentine leaning on a railing by the lake')}
  </div>
</section>

<section class="section band-dark on-dark">
  <div class="wrap">
    <div class="figures">
      <div><strong>20+</strong><span>years in Talent Acquisition</span></div>
      <div><strong>40+</strong><span>industries and geographies</span></div>
      <div><strong>3</strong><span>continents I call home</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What people say</h2><p>Recommendations from people I have worked alongside. <a href="https://www.linkedin.com/in/simonvalentine/details/recommendations/">See more on LinkedIn</a>.</p></div>
    {quotes_html()}
  </div>
</section>

<section class="section">
  <div class="wrap">{clients_html()}</div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head"><h2>Writing</h2><p>Thoughts on Talent Acquisition and the future of hiring. New pieces go out first in my <a href="{NEWSLETTER}">LinkedIn newsletter</a>.</p></div>
    {article_list(ARTICLES)}
  </div>
</section>

{closing("Let’s talk about your hiring.", "Tell me what you are working on. LinkedIn is the quickest way to reach me, or send an email.")}
"""
    page("", "Simon Valentine | Talent Acquisition advisor and consultant",
         "Simon Valentine helps organisations transform their Talent Acquisition function through advisory, consulting and the TA Exchange community.",
         body)


def build_about():
    body = f"""
<section class="page-intro with-photo">
  <div class="wrap">
    <div>
      <h1>A New Zealander in hiring, by way of the world.</h1>
      <p>I have spent more than twenty years in Talent Acquisition, working across cultures and continents. Here is how it started.</p>
    </div>
    <figure>{picture('simon-headshot', 'Portrait of Simon Valentine in a suit', eager=True)}</figure>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <figure>{picture('simon-lake-bench', 'Simon Valentine on a lakeside bench with the Alps behind')}</figure>
    <div>
      <ol class="timeline">
        <li><h3>Growing up</h3><p>I grew up in rural New Zealand, one of seven children of two hard-working parents. We lived in a number of small towns, my parents often worked two jobs, and a lot of my life lessons came from my brothers and sisters.</p></li>
        <li><h3>Into recruitment</h3><p>When I finished my degree I asked my professor how I could apply what I had learnt. He said the best place was a company’s Human Resources department, and the best way in was through recruitment. I started straight out of university in New Zealand.</p></li>
        <li><h3>Talent Acquisition, worldwide</h3><p>Twenty-plus years later I am still in Talent Acquisition. The work has taken me around the world and exposed me to many cultures, and today I split my time between Switzerland, England and New Zealand.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head"><h2>What people say</h2><p>A few words from people I have worked with.</p></div>
    {quotes_html()}
  </div>
</section>

<section class="section band">
  <div class="wrap">{clients_html()}</div>
</section>

{closing("Want to work together?", "Whether it is your Talent Acquisition function or your own career, I am happy to talk it through.")}
"""
    page("about/", "About", "Simon Valentine grew up in rural New Zealand and has spent more than twenty years in Talent Acquisition around the world.",
         body, current="about/", og_image="simon-headshot.jpg")


def build_work():
    body = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>Better hiring starts with the right function behind it.</h1>
    <p>Acquiring the right talent is key to a company’s success. Here are the ways I can help yours.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <ul class="services">
      <li><h3>Advisory</h3><div><p>Strategic counsel for leadership teams navigating talent complexity. I identify where your Talent Acquisition function can transform and help you decide what to do first.</p></div></li>
      <li><h3>Consulting</h3><div><p>Hands-on transformation, from diagnosing what is broken to building the systems, processes and team capability that fix it for good.</p></div></li>
      <li><h3>Community</h3><div><p>Through the TA Exchange, Talent Acquisition leaders get a curated peer network to share insights and navigate the future of hiring together.</p><a class="more" href="{{r}}ventures/">More about my ventures</a></div></li>
    </ul>
  </div>
</section>

<section class="section band-dark on-dark">
  <div class="wrap">
    <div class="section-head"><h2>How it works</h2><p>A simple process, shaped around your organisation.</p></div>
    <ol class="steps">
      <li><h3>Conversation</h3><p>We talk about your goals and challenges. No commitment required.</p></li>
      <li><h3>Diagnosis</h3><p>I review your current Talent Acquisition function and find where the real opportunities are.</p></li>
      <li><h3>Strategy</h3><p>Together we build a practical roadmap tailored to your goals.</p></li>
      <li><h3>Delivery</h3><p>I work alongside your team so the strategy is delivered and the results show.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2>On stage and in the room</h2>
      <div class="prose"><p>Alongside client work I speak at events and run sessions for Talent Acquisition leaders, on topics from AI in recruitment to building a function that scales.</p><p>If you would like me to speak at your event, get in touch.</p></div>
    </div>
    <figure>{picture('simon-speaking', 'Simon Valentine speaking on stage at an event')}</figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What clients say</h2></div>
    {quotes_html()}
  </div>
</section>

{closing("Ready to transform your Talent Acquisition?", "Start with a conversation about your goals.")}
"""
    page("work/", "Work with me", "Advisory, consulting and community: how Simon Valentine helps organisations improve their Talent Acquisition function.",
         body, current="work/", og_image="simon-speaking.jpg")


def build_ventures():
    body = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>Building the future of Talent Acquisition.</h1>
    <p>Three ventures, each tackling a different part of how organisations and Talent Acquisition leaders grow.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">{picture('simon-lake-bag', 'Simon Valentine by Lake Geneva with the mountains behind', cls='wide-photo')}</div>
</section>

<section class="section">
  <div class="wrap">
    <article class="venture">
      <div><h2>Acquire Talent</h2><p class="kind">Advisory and consulting</p></div>
      <div>
        <p class="tagline">Helping organisations make informed decisions when transforming their Talent Acquisition function.</p>
        <p>Practical, relevant and implementable strategies so your organisation can achieve its goals in acquiring the best talent.</p>
        <div class="actions"><a class="btn btn-ghost" href="{ACQUIRE_TALENT}">Acquire Talent on LinkedIn</a></div>
      </div>
    </article>
    <article class="venture">
      <div><h2>TA Exchange</h2><p class="kind">Community</p></div>
      <div>
        <p class="tagline">Leading the way in Talent Acquisition.</p>
        <p>A private community for Talent Acquisition professionals to share, discuss and engage on the biggest challenges and opportunities facing the industry today.</p>
        <div class="actions"><a class="btn btn-ghost" href="{TA_EXCHANGE}">TA Exchange on LinkedIn</a></div>
      </div>
    </article>
    <article class="venture">
      <div><h2>Your Platform</h2><p class="kind">Careers and personal brand</p></div>
      <div>
        <p class="tagline">Helping Talent Acquisition leaders reach the next level in their career.</p>
        <p>Whether you want to build your personal brand, grow your network or position yourself as a thought leader, Your Platform gives you the tools and strategy to get there, including the Talent Acquisition Leadership Program.</p>
        <div class="actions"><a class="btn btn-ghost" href="{YOUR_PLATFORM}">Ask me about Your Platform</a></div>
      </div>
    </article>
  </div>
</section>

{closing("Interested in one of these?", "Let’s talk about how we could work together.")}
"""
    page("ventures/", "Ventures", "Acquire Talent, TA Exchange and Your Platform: Simon Valentine's ventures in Talent Acquisition.",
         body, current="ventures/")


def build_articles():
    rows = "".join(
        f'<li><a href="{{r}}{a["slug"]}/"><time datetime="{a["date"]}">{a["date_label"]}</time><div><h3>{esc(a["title"])}</h3><p style="margin:8px 0 0;color:var(--slate)">{esc(a["summary"])}</p></div></a></li>'
        for a in ARTICLES)
    body = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>Writing on Talent Acquisition.</h1>
    <p>Ideas and lessons on hiring, leadership and where the industry is heading. New pieces appear first in my <a href="{NEWSLETTER}">LinkedIn newsletter</a>.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><ul class="article-list">{rows}</ul></div>
</section>
<section class="section band">
  <div class="wrap split">
    <figure>{picture('simon-reading', 'Simon Valentine reading the book Mindset on a bench')}</figure>
    <div><h2>Get the newsletter</h2><div class="prose"><p>Join the Talent Acquisition leaders who read my newsletter on LinkedIn.</p></div><div class="actions"><a class="btn btn-primary" href="{NEWSLETTER}">{ICON_LINKEDIN}Subscribe on LinkedIn</a></div></div>
  </div>
</section>
"""
    page("articles/", "Articles", "Articles by Simon Valentine on Talent Acquisition, AI in recruitment and leadership.", body, current="articles/")

    for a in ARTICLES:
        body = f"""
<article>
  <header class="article-head"><div class="wrap">
    <a class="back" href="{{r}}articles/">All articles</a>
    <h1>{esc(a['title'])}</h1>
    <time datetime="{a['date']}">{a['date_label']}</time>
  </div></header>
  <div class="wrap"><div class="prose prose-article">
{article_body(a['slug'])}
  </div></div>
</article>
{closing("Want to talk about this?", "I am always happy to compare notes with Talent Acquisition leaders.")}
"""
        page(f"{a['slug']}/", a["title"], a["summary"], body, current="articles/")


def build_contact():
    body = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>Get in touch.</h1>
    <p>Whether you want to transform your Talent Acquisition function, join a community of leaders or take your career further, I would like to hear from you.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap contact-grid">
    <div class="contact-card is-primary on-dark">
      <h2>LinkedIn</h2>
      <p>The quickest way to reach me. Send a message or a connection request.</p>
      <a class="btn btn-primary" href="{LINKEDIN}">{ICON_LINKEDIN}Message me on LinkedIn</a>
    </div>
    <div class="contact-card">
      <h2>Email</h2>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <a class="btn btn-ghost" href="mailto:{EMAIL}">{ICON_MAIL}Email me</a>
    </div>
    <div class="contact-card">
      <h2>Where I work</h2>
      <ul class="places"><li>Switzerland</li><li>England</li><li>New Zealand</li></ul>
      <p>Working with clients worldwide.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">{picture('simon-lakefront', 'Simon Valentine looking out over Lake Geneva', cls='wide-photo')}</div>
</section>
"""
    page("contact/", "Contact", "Contact Simon Valentine on LinkedIn or by email.", body, current="contact/")


def build_go():
    def link(href, icon, label, sub, primary=False):
        cls = ' class="is-primary"' if primary else ""
        return f'<li><a{cls} href="{href}"><span class="icon">{icon}</span><span>{label}<small>{sub}</small></span></a></li>'
    body = f"""
<div class="go">
  <div class="go-head">
    <img src="{{r}}assets/img/simon-avatar.jpg" alt="Simon Valentine" width="112" height="112">
    <h1>Simon Valentine</h1>
    <p>Taking you to the next level</p>
  </div>
  <h2>Get in touch</h2>
  <ul class="go-links">
    {link(LINKEDIN, ICON_LINKEDIN, 'Message me on LinkedIn', '@simonvalentine', primary=True)}
    {link('mailto:' + EMAIL, ICON_MAIL, 'Send me an email', EMAIL)}
  </ul>
  <h2>Content and community</h2>
  <ul class="go-links">
    {link(NEWSLETTER, ICON_NEWS, 'Read the Talent Acquisition newsletter', 'On LinkedIn')}
    {link(PODCAST, ICON_MIC, 'Listen to the podcast', 'Your Career With Purpose, on SoundCloud')}
    {link(TA_EXCHANGE, ICON_PEOPLE, 'Join TA leaders at the TA Exchange', 'Private community for Talent Acquisition professionals, on LinkedIn')}
    {link(LEADERSHIP_PROGRAM, ICON_STAR, 'Ask about the Talent Acquisition Leadership Program', 'Your Platform. Message me on LinkedIn')}
  </ul>
  <h2>This website</h2>
  <ul class="go-links">
    {link('{r}', ICON_STAR, 'simonvalentine.com', 'About, work, ventures and articles')}
  </ul>
</div>
"""
    page("go/", "Links", "Links to Simon Valentine on LinkedIn, the newsletter, podcast and ventures.", body, chrome=False)


def build_legal():
    privacy = f"""
<section class="page-intro"><div class="wrap"><h1>Privacy</h1><p>Last updated November {YEAR}.</p></div></section>
<div class="wrap"><div class="prose legal">
<p>This website, simonvalentine.com, is run by Simon Valentine Limited. This notice explains what information is handled when you visit it.</p>
<h2>What this site collects</h2>
<p>This is a simple information website. It has no forms, accounts or shop, and it does not set its own cookies or use analytics or advertising trackers.</p>
<p>The site is hosted by GitHub Pages. Like most web hosts, GitHub may record technical information such as your IP address and browser type in server logs to keep the service secure and running. You can read <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub’s privacy statement</a>.</p>
<p>Fonts are loaded from Google Fonts, which receives your IP address when the fonts are downloaded. See <a href="https://policies.google.com/privacy">Google’s privacy policy</a>.</p>
<h2>When you contact me</h2>
<p>If you email me or message me on LinkedIn, I use what you send only to reply and to follow up on your enquiry. I do not sell or share it.</p>
<h2>Links to other sites</h2>
<p>This site links to LinkedIn, SoundCloud and my ventures’ websites. Those sites have their own privacy policies.</p>
<h2>Your rights</h2>
<p>You can ask what personal information I hold about you, and ask me to correct or delete it, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div>
"""
    page("privacy-policy/", "Privacy", "How simonvalentine.com handles your information.", privacy)
    terms = f"""
<section class="page-intro"><div class="wrap"><h1>Terms of use</h1><p>Last updated November {YEAR}.</p></div></section>
<div class="wrap"><div class="prose legal">
<p>By using simonvalentine.com you agree to these terms.</p>
<h2>Content</h2>
<p>The content on this site, including text and photographs, belongs to Simon Valentine Limited unless stated otherwise. You may share links to it and quote short extracts with credit. Please ask before reusing anything else.</p>
<h2>No professional advice</h2>
<p>Articles and other material on this site are general information. They are not advice for your specific situation.</p>
<h2>Other websites</h2>
<p>Links to other websites are provided for convenience. I am not responsible for their content.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div>
"""
    page("terms-of-service/", "Terms of use", "Terms of use for simonvalentine.com.", terms)


def build_404():
    body = """
<section class="page-intro">
  <div class="wrap">
    <h1>This page has moved or no longer exists.</h1>
    <p>The site has been rebuilt, so some old addresses have changed. Try the <a href="/">home page</a> or the <a href="/articles/">articles</a>.</p>
  </div>
</section>
"""
    page("404.html", "Page not found", "This page could not be found.", body)


def build_extras():
    urls = ["", "about/", "work/", "ventures/", "articles/", "contact/", "go/", "privacy-policy/", "terms-of-service/"] + [a["slug"] + "/" for a in ARTICLES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE_URL}/{u}</loc></url>" for u in urls]
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    # Old WordPress addresses that should still land somewhere useful
    redirects = {"resume/": "go/", "purpose/": "about/", "calendar/": "contact/"}
    for old, new in redirects.items():
        d = ROOT / old
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            f'<!doctype html><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url=../{new}"><link rel="canonical" href="{SITE_URL}/{new}">'
            f'<p><a href="../{new}">This page has moved.</a></p>\n')


if __name__ == "__main__":
    build_home()
    build_about()
    build_work()
    build_ventures()
    build_articles()
    build_contact()
    build_go()
    build_legal()
    build_404()
    build_extras()
