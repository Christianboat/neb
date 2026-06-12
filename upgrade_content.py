"""
Non-destructive content upgrade.

Adds the new *editable* card sections (Core Values, Key Features, Ways to Get
Involved, ecosystem / app / security lists) to an EXISTING database without
wiping anything. Safe to run repeatedly — it only creates what is missing.

    python upgrade_content.py
"""
from app import create_app, db
from app.models import Page, Section, ContentItem


# section data: page_slug -> (section_key, title, order, [items])
# Each item is a dict with any of: icon, title, subtitle, content,
# link_url, link_text.
CONTENT = [
    ("about", "values", "Our Core Values", 4, [
        {"icon": "fas fa-star", "title": "Excellence",
         "content": "We strive for quality in every program, leaning into the "
                    "belief that excellence is a journey that grows with "
                    "opportunity."},
        {"icon": "fas fa-lightbulb", "title": "Innovation",
         "content": "We embrace new ideas, technologies, and methods to "
                    "reimagine education, events, and professional "
                    "development."},
        {"icon": "fas fa-balance-scale", "title": "Integrity",
         "content": "We operate with transparency, fairness, and respect in "
                    "every partnership and engagement."},
        {"icon": "fas fa-users", "title": "Inclusion",
         "content": "We believe every person deserves access to high-quality "
                    "learning and recognition."},
        {"icon": "fas fa-globe", "title": "Global Collaboration",
         "content": "We build bridges across borders, enabling shared "
                    "learning, cultural exchange, and international "
                    "opportunity."},
    ]),
    ("digital", "features", "Key Features of the Platform", 1, [
        {"title": "Online Competition Portal", "subtitle": "A dedicated space for:",
         "content": "Live online rounds\nPractice quizzes\nAutomated scoring\n"
                    "Virtual stages\nRegional and international competitions"},
        {"title": "Learning & Training Hub", "subtitle": "A digital classroom for:",
         "content": "Professional development courses\nWorkshops and webinars\n"
                    "On-demand video lessons\nDownloadable toolkits\n"
                    "Certification badges"},
        {"title": "Smart Registration & Management", "subtitle": "For all programs:",
         "content": "Competition entry\nTraining enrollment\nEvent ticketing\n"
                    "Exhibitor and sponsor registration\nSchool onboarding"},
        {"title": "Digital Credentialing", "subtitle": "Nebula issues:",
         "content": "Digital certificates\nAchievement badges\n"
                    "Participation transcripts"},
        {"title": "Virtual Exhibitions & Trade Fairs",
         "subtitle": "Schools and companies can:",
         "content": "Host digital booths\nShare videos and brochures\n"
                    "Engage with attendees\nCollect leads"},
        {"title": "Leaderboards & Dashboards", "subtitle": "Students and schools view:",
         "content": "Competition rankings\nPerformance analytics\n"
                    "Achievement levels\nRegional comparisons"},
        {"title": "Partner & Ambassador Portals", "subtitle": "Organizations get:",
         "content": "Exclusive dashboards\nPartnership benefits\n"
                    "Resource libraries\nPriority registration"},
    ]),
    ("digital", "ecosystem", "A Global Learning & Event Ecosystem", 2, [
        {"title": t} for t in [
            "Competitions", "Training & professional development",
            "Digital certificates", "Partner portals", "Exhibitions & expos",
            "Leaderboards", "Learning modules", "Registration & ticketing",
            "Community engagement"]
    ]),
    ("digital", "app_features", "Coming Soon: The Nebula App", 3, [
        {"icon": "fas fa-bolt", "title": "Daily quizzes"},
        {"icon": "fas fa-gamepad", "title": "Vocabulary and math games"},
        {"icon": "fas fa-bullhorn", "title": "Event updates"},
        {"icon": "fas fa-chart-line", "title": "Personal progress tracking"},
        {"icon": "fas fa-bell", "title": "Notifications and reminders"},
    ]),
    ("digital", "security", "Data Security & Compliance", 4, [
        {"icon": "fas fa-user-shield", "title": "Privacy protection"},
        {"icon": "fas fa-credit-card", "title": "Secure payment processing"},
        {"icon": "fas fa-lock", "title": "Encrypted user data"},
        {"icon": "fas fa-child", "title": "Child safety protocols for minors"},
        {"icon": "fas fa-file-contract",
         "title": "Compliance with UAE, EU (GDPR), and global standards"},
    ]),
    ("join", "join_options", "Ways to Get Involved", 0, [
        {"icon": "fas fa-school", "title": "Schools",
         "subtitle": "Empower your students. Strengthen your teachers.",
         "content": "International competitions\nProfessional development\n"
                    "School leadership training\nRecognition & awards\n"
                    "Ambassador School status",
         "link_url": "/contact?type=school", "link_text": "➡ Register Your School"},
        {"icon": "fas fa-chalkboard-user", "title": "Educators & Professionals",
         "subtitle": "Advance your career through world-class training.",
         "content": "Professional development courses\nLeadership training\n"
                    "Teaching workshops\nCertified digital programs",
         "link_url": "/contact?type=training", "link_text": "➡ Enroll in Training"},
        {"icon": "fas fa-user-graduate", "title": "Students & Parents",
         "subtitle": "Unlock confidence, creativity, and global exposure.",
         "content": "Global Spell Bee\nMath Master Challenge\n"
                    "Debate & Communication League\nSustainability Olympiad\n"
                    "Youth expos and festivals",
         "link_url": "/contact?type=competition", "link_text": "➡ Register"},
        {"icon": "fas fa-handshake", "title": "Corporate Sponsors & CSR Partners",
         "subtitle": "Partner for impact. Build visibility.",
         "content": "Direct community impact\nBrand visibility across schools\n"
                    "CSR alignment\nYear-round engagement\nNaming opportunities",
         "link_url": "/contact?type=sponsor", "link_text": "➡ Become a Sponsor"},
        {"icon": "fas fa-landmark", "title": "Embassies & Cultural Missions",
         "subtitle": "Promote culture, language, and collaboration.",
         "content": "Co-branded competitions\nCultural events\n"
                    "Teacher exchange\nLeadership training\nEducation fairs",
         "link_url": "/contact?type=embassy", "link_text": "➡ Collaborate"},
        {"icon": "fas fa-globe-americas", "title": "Country Coordinator",
         "subtitle": "Bring Nebula programs to your country.",
         "content": "Chapter rights\nBrand licensing\nTraining & onboarding\n"
                    "Revenue-sharing models\nExclusive territories",
         "link_url": "/contact?type=country", "link_text": "➡ Apply"},
        {"icon": "fas fa-hands-helping", "title": "Volunteers & Interns",
         "subtitle": "Shape events. Learn. Grow.",
         "content": "Event logistics\nSocial media\nTraining support\n"
                    "Digital content\nCommunity outreach",
         "link_url": "/contact?type=volunteer", "link_text": "➡ Join"},
    ]),
]


def ensure_card_section(page_slug, key, title, order, items):
    page = Page.query.filter_by(slug=page_slug).first()
    if not page:
        print(f"  - page '{page_slug}' not found, skipping {key}")
        return
    section = Section.query.filter_by(
        page_id=page.id, section_key=key).first()
    if section and section.items.count():
        print(f"  - {page_slug}/{key} already populated, skipping")
        return
    if not section:
        section = Section(page_id=page.id, section_key=key,
                          title=title, content="", order=order)
        db.session.add(section)
        db.session.commit()
    for i, item in enumerate(items):
        db.session.add(ContentItem(
            section_id=section.id,
            icon=item.get("icon"),
            title=item.get("title"),
            subtitle=item.get("subtitle"),
            content=item.get("content"),
            link_url=item.get("link_url"),
            link_text=item.get("link_text"),
            order=i))
    db.session.commit()
    print(f"  + added {page_slug}/{key} with {len(items)} items")


def main():
    app = create_app()
    with app.app_context():
        print("Upgrading editable content...")
        for page_slug, key, title, order, items in CONTENT:
            ensure_card_section(page_slug, key, title, order, items)

        # Remove the old placeholder/Rickroll video from the home intro.
        home = Page.query.filter_by(slug="home").first()
        if home:
            intro = Section.query.filter_by(
                page_id=home.id, section_key="intro").first()
            if intro and intro.video_url and "dQw4w9WgXcQ" in intro.video_url:
                intro.video_url = None
                db.session.commit()
                print("  + removed placeholder video from home intro")

        print("Done.")


if __name__ == "__main__":
    main()
