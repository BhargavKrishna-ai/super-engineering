"""Render the programme pages as independent static HTML documents."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent
DIST = PROJECT / "dist"
PHONE = "tel:+914045307444"
WHATSAPP = "https://wa.me/919000719444?text=Hello%2C%20I%20would%20like%20to%20know%20more%20about%20Super%20Engineering."
NAV = [
    ("Courses", "courses"), ("How We Teach", "how-we-teach"),
    ("Outcomes", "outcomes"), ("Founders", "founders"),
    ("For Parents", "parents"), ("Partners", "partners"), ("About", "about"),
]
COURSES = [
    ("VLSI Design & Technology", "courses/vlsi"),
    ("Electronics & Computer Engineering", "courses/electronics-computer-engineering"),
    ("Robotics & Artificial Intelligence", "courses/robotics-ai"),
    ("CSE (AI & Machine Learning)", "courses/cse-ai-ml"),
    ("BBA & MBA", "courses/management"),
]
PAGE_NAMES = {route: name for name, route in NAV + COURSES}
PAGE_NAMES["admissions"] = "Admissions"
ESC = html.escape


def url(root, value):
    if urlsplit(value).scheme or value.startswith("#"):
        return ESC(value)
    path, separator, anchor = value.partition("#")
    target = root + path.strip("/") + "/" if path.strip("/") else root
    return ESC(target + separator + anchor)


def link(root, href, label, css=""):
    style = f' class="{css}"' if css else ""
    return f'<a{style} href="{url(root, href)}">{ESC(label)}</a>'


def brand(root):
    return f'''<a class="brand" href="{root}" aria-label="Super Engineering home">
      <span class="brand-symbol" aria-hidden="true"></span>
      <span class="brand-text"><span>Super</span><span>Engineering</span></span>
    </a>'''


def header(root, route):
    links = []
    for name, path in NAV:
        current = ""
        if route == path:
            current = ' aria-current="page"'
        elif route.startswith(path + "/"):
            current = ' aria-current="location"'
        links.append(f'<li><a href="{url(root, path)}"{current}>{ESC(name)}</a></li>')
    return f'''
<a class="skip" href="#main">Skip to content</a>
<div class="topline"><div class="wrap"><p>Admissions enquiries</p><a href="{PHONE}">Call 040 45307444</a></div></div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main navigation">
    {brand(root)}
    <ul class="nav-links" id="primary-links">{"".join(links)}</ul>
    <div class="nav-action"><span class="nav-apply">{link(root, "admissions#apply", "Apply now", "button primary")}</span><button type="button" class="menu-toggle" aria-controls="primary-links" aria-expanded="false">Menu</button></div>
  </nav>
</header>'''


def footer(root):
    groups = [
        ("Courses", COURSES),
        ("Learn more", NAV[1:5]),
        ("Work with us", NAV[5:] + [("Careers enquiries", "admissions#contact")]),
        ("Contact", [("040 45307444", PHONE), ("WhatsApp 9000719444", WHATSAPP), ("Admissions", "admissions"), ("Book a campus visit", "admissions#visit")]),
    ]
    columns = "".join(
        f'<div><h2>{ESC(title)}</h2>{"".join(link(root, path, name) for name, path in entries)}</div>'
        for title, entries in groups
    )
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid"><div class="footer-brand">{brand(root)}<p>Build what AI runs on.</p></div>{columns}</div>
    <div class="footer-legal"><p>Super Engineering is the academic delivery partner. Ask admissions which university awards your degree.</p><p>Images are concept illustrations.</p></div>
  </div>
</footer>
<nav class="mobile-actions" aria-label="Contact admissions">
  {link(root, PHONE, "Call")}{link(root, WHATSAPP, "WhatsApp")}{link(root, "admissions#visit", "Book a visit")}
</nav>'''


def form(kind):
    visit = kind == "visit"
    title = "Request a visit on WhatsApp" if visit else "Start on WhatsApp"
    message = "Hello, I would like to request a Super Engineering campus visit." if visit else "Hello, I would like to apply to Super Engineering. Could you share the next steps?"
    date = '<label class="field">Preferred date<input id="visit-date" type="date" name="date" required></label>' if visit else ""
    options = "".join(f'<option value="{ESC(name)}">{ESC(name)}</option>' for name, _ in COURSES)
    explanation = "Send your preferred date to admissions in WhatsApp. An adviser will confirm availability."
    if not visit:
        explanation = "Send an enquiry in WhatsApp. An adviser can confirm eligibility and share application instructions."
    return f'''
<form class="visit-form" data-message="{ESC(message)}" hidden>
  <label class="field">Full name<input type="text" name="name" autocomplete="name" required maxlength="90"></label>
  <label class="field">Phone number<input type="tel" name="phone" autocomplete="tel" required maxlength="25"></label>
  <label class="field">I am a<select name="role" required><option value="">Select one</option><option>Student</option><option>Parent or guardian</option><option>Other</option></select></label>
  <label class="field">Programme<select name="course" required><option value="">Select programme</option>{options}<option>Still deciding</option></select></label>
  {date}
  <p class="form-note form-wide">{explanation} Share your number for admissions follow-up.</p>
  <div class="form-wide"><button type="submit" class="button primary">{title}</button></div>
  <p class="form-message form-wide" role="status"></p>
</form>'''


def contact_links(root):
    return f'<div class="phone-links">{link(root, PHONE, "Call 040 45307444")}{link(root, WHATSAPP, "Chat with an adviser")}</div>'


def visit_section(root):
    return f'''
<section class="section contact-section" id="visit">
  <div class="wrap split contact-grid">
    <div><p class="eyebrow"><span></span> Campus visits</p><h2>Come and <em>see for yourself.</em></h2>
    <p class="section-lead">Bring your parents. Ask to see the Factory, meet the faculty and get answers about the programme you’re considering.</p>
    {contact_links(root)}</div>
    {form("visit")}
  </div>
</section>'''


def breadcrumb(root, route):
    parts = [link(root, "", "Home")]
    if "/" in route:
        parts.append(link(root, "courses", "Courses"))
    parts.append(f'<span aria-current="page">{ESC(PAGE_NAMES[route])}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'


def banner(root, route, data):
    cta = data.get("cta") or {"href": "admissions#visit", "label": "Book a campus visit"}
    return f'''
<section class="detail-banner" aria-labelledby="page-title">
  <div class="wrap">
    {breadcrumb(root, route)}
    <div class="split detail-grid">
      <div><p class="eyebrow"><span></span> {ESC(data["eyebrow"])}</p>
      <h1 id="page-title">{ESC(data["title"])}</h1>
      <p class="section-lead">{ESC(data["lead"])}</p>
      {link(root, cta["href"], cta["label"], "button primary")}</div>
      <figure class="detail-image"><img src="{root}assets/{ESC(data["image"])}" width="1536" height="1024" alt="" fetchpriority="high"><figcaption>Concept illustration</figcaption></figure>
    </div>
  </div>
</section>'''


def section(root, record):
    title = record["title"]
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if title == "Our reporting pledge":
        slug = "reporting-pledge"
    intro = f'<p class="section-lead">{ESC(record["intro"])}</p>' if record.get("intro") else ""
    body = "".join(f"<p>{ESC(paragraph)}</p>" for paragraph in record.get("body", []))
    items = record.get("items", [])
    links = record.get("links", [])
    cards = ""
    if items and record.get("link_each_item"):
        gallery = "".join(f'''
<a class="course-card" href="{url(root, entry['href'])}">
  <img src="{root}assets/{ESC(item['image'])}" width="768" height="512" alt="" loading="lazy">
  <div class="course-info"><p class="tag">{ESC(item['layer'])}</p><h3>{ESC(item['title'])}</h3>
  <p>{ESC(item['text'])}</p><span class="text-link">See the course</span></div>
</a>''' for item, entry in zip(items, links, strict=True))
        cards = f'<div class="course-grid detail-course-grid">{gallery}</div>'
    elif items:
        articles = "".join(f'<article class="detail-card"><h3>{ESC(item["title"])}</h3><p>{ESC(item["text"])}</p></article>' for item in items)
        cards = f'<div class="detail-card-grid">{articles}</div>'
    links_html = ""
    if links and not record.get("link_each_item"):
        links_html = '<div class="detail-links">' + "".join(link(root, x["href"], x["label"], "text-link") for x in links) + "</div>"
    return f'''
<section class="detail-section" id="{slug}"><div class="wrap"><h2>{ESC(title)}</h2>{intro}
  {f'<div class="detail-body">{body}</div>' if body else ""}
  {cards}
  {links_html}
</div></section>'''


def faq(records):
    entries = "".join(
        f'<details><summary>{ESC(item["question"])}</summary><p>{ESC(item["answer"])}</p></details>'
        for item in records
    )
    return f'<section class="detail-section" id="questions"><div class="wrap"><h2>Common questions</h2><div class="faq-list">{entries}</div></div></section>'


def detail_content(root, route, data):
    cta = data.get("cta") or {"href": "admissions#visit", "label": "Book a campus visit"}
    content = banner(root, route, data)
    contents = data["sections"]
    if route == "courses" and len(contents[0].get("links", [])) == len(contents[0].get("items", [])):
        contents[0]["link_each_item"] = True
    content += "".join(section(root, info) for info in contents)
    if data.get("faq"):
        content += faq(data["faq"])
    return content + f'<section class="detail-end"><div class="wrap"><h2>Ready to take the next step?</h2>{link(root, cta["href"], cta["label"], "button primary")}</div></section>'


def admissions(root):
    return banner(root, "admissions", {
        "eyebrow": "Admissions", "title": "Join the founding batch.",
        "lead": "Explore the programmes, visit the campus and talk through eligibility and fees with an adviser before you apply.",
        "image": "lab.webp", "cta": {"href": "#apply", "label": "Apply now"},
    }) + section(root, {
        "title": "How to apply",
        "items": [
            {"title": "Talk to us or visit", "text": "Bring your parents, see what students will build and ask about your chosen programme."},
            {"title": "Start your application", "text": "Share your interest with the admissions team and get instructions for the formal application."},
            {"title": "Check eligibility", "text": "Admissions will explain the marks, entrance scores and documents required for your chosen programme."},
            {"title": "Confirm your seat", "text": "Review the formal offer and fee schedule before accepting a seat."},
        ],
    }) + '''
<section class="detail-section" id="programme-facts"><div class="wrap">
  <h2>Programme facts</h2>
  <p class="section-lead">Ask admissions for the duration and entry requirements for your intake, accepted exams, seats, fees and any scholarship or loan options.</p>
  <div class="table-shell"><table class="comparison">
    <caption class="sr-only">Programme durations</caption>
    <thead><tr><th scope="col">Programme</th><th scope="col">Duration outlined in the programme plan</th></tr></thead>
    <tbody><tr><th scope="row">B.Tech</th><td>4 years</td></tr><tr><th scope="row">BBA</th><td>Confirm the degree structure with admissions</td></tr><tr><th scope="row">MBA</th><td>2 years</td></tr></tbody>
  </table></div>
</div></section>''' + f'''
<section class="detail-section" id="apply"><div class="wrap split contact-grid">
  <div><p class="eyebrow"><span></span> Application enquiries</p><h2>Apply for a programme.</h2><p class="section-lead">Tell the team what you’d like to study. You’ll send your enquiry in WhatsApp and can ask for the formal application link.</p>{contact_links(root)}</div>{form("apply")}
</div></section>
<section class="detail-section" id="contact"><div class="wrap"><h2>Talk to a person.</h2>
  <p class="section-lead">Ask about admissions, campus visits, partnerships or careers. For partnerships and careers, mention what you’re interested in so the team can direct your enquiry.</p>{contact_links(root)}
</div></section>''' + visit_section(root)


def page(route, title, description, content):
    root = "../" * len(route.split("/")) if route else "./"
    output = DIST / route / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f'''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#eef5fc">
  <title>{ESC(title)}</title>
  <meta name="description" content="{ESC(description)}">
  <link rel="icon" href="{root}assets/favicon.png" type="image/png">
  <link rel="stylesheet" href="{root}styles.css">
  <script defer src="{root}site.js"></script>
</head>
<body>
  {header(root, route)}
  <main id="main">{content}</main>
  {footer(root)}
</body>
</html>
''', encoding="utf-8")


def main():
    home = (PROJECT / "home.html").read_text(encoding="utf-8")
    home = home.replace("{{assets}}", "./assets/").replace("{{root}}", "./").replace("{{visit}}", visit_section("./"))
    page("", "Super Engineering | Build what AI runs on", "Explore B.Tech and management programmes built around practical work, engineering projects and AI.", home)
    for filename in ("course-pages.json", "audience-pages.json"):
        data = json.loads((PROJECT / filename).read_text(encoding="utf-8"))
        for route, entry in data.items():
            root = "../" * len(route.split("/"))
            page(route, PAGE_NAMES[route] + " | Super Engineering", entry["lead"], detail_content(root, route, entry))
    page("admissions", "Admissions | Super Engineering", "Talk to admissions about B.Tech, BBA and MBA programmes, or request a campus visit.", admissions("../"))


if __name__ == "__main__":
    main()
