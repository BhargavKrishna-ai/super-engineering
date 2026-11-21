"""Render the programme pages as independent static HTML documents."""
import html
import json
import re
from pathlib import Path
from textwrap import indent
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent
DIST = PROJECT / "dist"
COURSE_ART_SIZES = (
    "(max-width: 355px) calc(100vw - 26px), "
    "(max-width: 540px) calc(100vw - 36px), "
    "(max-width: 690px) 46vw, (max-width: 1390px) 44vw, 600px"
)
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
IMAGE_DESCRIPTIONS = {
    "about.webp": "A cutaway architectural model of a robotics lab and project workshop",
    "admissions-detail.webp": "A bright corridor opening onto an engineering classroom",
    "aiml-detail.webp": "Model training and validation curves above a field of data points",
    "courses-overview.webp": "An engineering workbench with a gantry, a sensor enclosure and silicon samples",
    "ece-detail.webp": "An open measuring instrument with a circuit board being calibrated",
    "founders-detail.webp": "Three iterations of an air-quality monitor prototype",
    "how-teach.webp": "A mounted circuit board and tools on an electronics test bench",
    "management-detail.webp": "A product mock-up presented with packaging and material samples",
    "outcomes-detail.webp": "A finished spectrometer and its test samples in a presentation case",
    "parents.webp": "A display robot in a light-filled engineering demonstration lab",
    "partners-detail.webp": "A pilot manufacturing cell with a conveyor and an inspection station",
    "robotics-detail.webp": "A Cartesian gantry robot positioning its tool head over a target",
    "vlsi-detail.webp": "A patterned lithography reticle held above a semiconductor die layout",
}
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
    artwork = data["image"]
    return f'''
<section class="detail-banner" aria-labelledby="page-title">
  <div class="wrap">
    {breadcrumb(root, route)}
    <div class="split detail-grid">
      <div><p class="eyebrow"><span></span> {ESC(data["eyebrow"])}</p>
      <h1 id="page-title">{ESC(data["title"])}</h1>
      <p class="section-lead">{ESC(data["lead"])}</p>
      {link(root, cta["href"], cta["label"], "button primary")}</div>
      <figure class="detail-image"><img src="{root}assets/{ESC(artwork)}" width="1536" height="1024" alt="{ESC(IMAGE_DESCRIPTIONS[artwork])}" fetchpriority="high"><figcaption>Concept illustration</figcaption></figure>
    </div>
  </div>
</section>'''


def section_id(record):
    return record.get("id") or re.sub(r"[^a-z0-9]+", "-", record["title"].lower()).strip("-")


def programme_summary(facts):
    entries = "".join(
        f'<div><dt>{ESC(fact["label"])}</dt><dd>{ESC(fact["value"])}</dd></div>'
        for fact in facts
    )
    return f'<div class="programme-summary"><dl class="wrap">{entries}</dl></div>'


def detail_navigation(anchors):
    entries = "".join(f'<li>{link("", "#" + target, label)}</li>' for label, target in anchors)
    return f'''
<nav class="detail-subnav" aria-label="On this page">
  <div class="wrap"><p class="detail-subnav-label" aria-hidden="true">On this page</p><ul>{entries}</ul></div>
</nav>'''


def section(root, record):
    title = record["title"]
    slug = section_id(record)
    layout = record.get("layout")
    css = "detail-section"
    if layout == "gallery":
        css += " detail-gallery-section"
    elif layout == "projects":
        css += " detail-projects"
    intro = f'<p class="section-lead">{ESC(record["intro"])}</p>' if record.get("intro") else ""
    body = "".join(f"<p>{ESC(paragraph)}</p>" for paragraph in record.get("body", []))
    items = record.get("items", [])
    links = record.get("links", [])
    cards = ""
    if layout == "gallery":
        gallery = []
        for item, entry in zip(items, links, strict=True):
            thumb = root + "assets/" + item["image"]
            full = thumb.removesuffix("-thumb.webp") + ".webp"
            gallery.append(f'''
<a class="course-card" href="{url(root, entry['href'])}">
  <div class="course-plate"><img src="{ESC(thumb)}" srcset="{ESC(thumb)} 768w, {ESC(full)} 1536w" sizes="{COURSE_ART_SIZES}"
    width="768" height="512" alt="" loading="lazy"></div>
  <div class="course-info"><p class="tag">{ESC(item['layer'])}</p><h3>{ESC(item['title'])}</h3>
  <p>{ESC(item['text'])}</p><span class="text-link">{ESC(entry['label'])}</span></div>
</a>''')
        cards = f'<div class="course-grid detail-course-grid programme-gallery">{"".join(gallery)}</div>'
    elif items:
        articles = []
        item_tag = "li" if layout == "projects" else "article"
        for item in items:
            heading = ESC(item["title"])
            period, _, project = item["title"].partition(" · ")
            if layout == "projects" and project and re.fullmatch(r"(?:Year|Semester|Step) \d+", period):
                heading = f'<span class="project-period">{ESC(period)}</span> {ESC(project)}'
            articles.append(f'<{item_tag} class="detail-card"><h3>{heading}</h3><p>{ESC(item["text"])}</p></{item_tag}>')
        if layout == "projects":
            cards = f'<ol class="detail-card-grid" role="list">{"".join(articles)}</ol>'
        else:
            cards = f'<div class="detail-card-grid">{"".join(articles)}</div>'
    links_html = ""
    if links and layout != "gallery":
        links_html = '<div class="detail-links">' + "".join(link(root, x["href"], x["label"], "text-link") for x in links) + "</div>"
    body_html = f'<div class="detail-body">{body}</div>' if body else ""
    details = "\n".join(fragment for fragment in (body_html, cards, links_html) if fragment)
    return f'''
<section class="{css}" id="{ESC(slug)}">
  <div class="wrap detail-section-inner">
    <div class="detail-section-intro"><h2>{ESC(title)}</h2>{intro}</div>
    <div class="detail-section-content">
{indent(details, '      ')}
    </div>
  </div>
</section>'''


def faq(records):
    entries = "".join(
        f'<details><summary>{ESC(item["question"])}</summary><p>{ESC(item["answer"])}</p></details>'
        for item in records
    )
    return f'''<section class="detail-section" id="questions">
  <div class="wrap detail-section-inner">
    <div class="detail-section-intro"><h2>Common questions</h2></div>
    <div class="detail-section-content faq-list">{entries}</div>
  </div>
</section>'''


def detail_content(root, route, data):
    cta = data.get("cta") or {"href": "admissions#visit", "label": "Book a campus visit"}
    content = banner(root, route, data)
    sections = data["sections"]
    questions = data.get("faq")
    if data.get("summary"):
        content += programme_summary(data["summary"])
    anchors = [(record.get("nav", record["title"]), section_id(record)) for record in sections[:4]]
    if questions:
        anchors.append(("Common questions", "questions"))
    content += detail_navigation(anchors)
    content += "".join(section(root, info) for info in sections)
    if questions:
        content += faq(questions)
    closing = data.get("closing") or {
        "title": "See the workshop in person.",
        "text": "Ask to see the equipment, project work and practical tests that shape the programme.",
    }
    return content + f'''
<section class="detail-end"><div class="wrap">
  <div class="detail-end-copy"><h2>{ESC(closing["title"])}</h2><p>{ESC(closing["text"])}</p></div>
  {link(root, cta["href"], cta["label"], "button primary")}
</div></section>'''


def admissions(root):
    return banner(root, "admissions", {
        "eyebrow": "Admissions", "title": "Plan your application.",
        "lead": "Choose a programme, check which requirements apply to you and speak to an adviser about fees or a campus visit.",
        "image": "admissions-detail.webp", "cta": {"href": "#apply", "label": "Apply now"},
    }) + detail_navigation([
        ("How to apply", "how-to-apply"), ("Programme facts", "programme-facts"),
        ("Application enquiry", "apply"), ("Campus visit", "visit"),
    ]) + section(root, {
        "title": "How to apply",
        "layout": "projects",
        "items": [
            {"title": "Step 1 · Explore the programme", "text": "Visit with your family and ask what you can build in the course you’re considering."},
            {"title": "Step 2 · Contact admissions", "text": "Tell the team what you’d like to study and ask for the formal application instructions."},
            {"title": "Step 3 · Check eligibility", "text": "Check the marks, entrance scores and documents required for your chosen programme."},
            {"title": "Step 4 · Review your offer", "text": "Review the formal offer and fees before accepting a seat."},
        ],
    }) + '''
<section class="detail-section" id="programme-facts"><div class="wrap detail-section-inner">
  <div class="detail-section-intro"><h2>Programme facts</h2>
  <p class="section-lead">Ask admissions about entry requirements, accepted exams, seats, fees and funding options.</p></div>
  <div class="detail-section-content table-shell"><table class="comparison">
    <caption class="sr-only">Programme durations</caption>
    <thead><tr><th scope="col">Programme</th><th scope="col">Duration outlined in the programme plan</th></tr></thead>
    <tbody><tr><th scope="row">B.Tech</th><td>4 years</td></tr><tr><th scope="row">BBA</th><td>Confirm the degree structure with admissions</td></tr><tr><th scope="row">MBA</th><td>2 years</td></tr></tbody>
  </table></div>
</div></section>''' + f'''
<section class="detail-section" id="apply"><div class="wrap split contact-grid">
  <div><p class="eyebrow"><span></span> Application enquiries</p><h2>Apply for a programme.</h2><p class="section-lead">Tell the team what you’d like to study. You’ll send your enquiry in WhatsApp and can ask for the formal application link.</p>{contact_links(root)}</div>{form("apply")}
</div></section>
<section class="detail-section" id="contact"><div class="wrap detail-section-inner">
  <div class="detail-section-intro"><h2>Talk to an adviser.</h2></div>
  <div class="detail-section-content"><p class="section-lead">Ask about admissions, campus visits, partnerships or careers. For partnerships and careers, mention what you’re interested in so the team can direct your enquiry.</p>{contact_links(root)}</div>
</div></section>''' + visit_section(root)


def page(route, title, description, content):
    root = "../" * len(route.split("/")) if route else "./"
    editorial = f'\n  <link rel="stylesheet" href="{root}editorial.css">' if route in {"", "courses"} else ""
    main_class = ' class="home-content"' if not route else ""
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
  <link rel="preload" href="{root}assets/inter-tight.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}styles.css">{editorial}
  <script defer src="{root}site.js"></script>
</head>
<body>
  {header(root, route)}
  <main id="main"{main_class}>{content}</main>
  {footer(root)}
</body>
</html>
''', encoding="utf-8")


def main():
    home = (PROJECT / "home.html").read_text(encoding="utf-8")
    home = home.replace("{{assets}}", "./assets/").replace("{{root}}", "./")
    home = home.replace("{{courseSizes}}", COURSE_ART_SIZES).replace("{{visit}}", visit_section("./"))
    page("", "Super Engineering | Build what AI runs on", "Explore B.Tech and management programmes built around practical work, engineering projects and AI.", home)
    for filename in ("course-pages.json", "audience-pages.json"):
        data = json.loads((PROJECT / filename).read_text(encoding="utf-8"))
        for route, entry in data.items():
            root = "../" * len(route.split("/"))
            page(route, PAGE_NAMES[route] + " | Super Engineering", entry["lead"], detail_content(root, route, entry))
    page("admissions", "Admissions | Super Engineering", "Talk to admissions about B.Tech, BBA and MBA programmes, or request a campus visit.", admissions("../"))


if __name__ == "__main__":
    main()
