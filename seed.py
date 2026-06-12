import os
import secrets
from datetime import datetime
from app import create_app, db
from app.models import (
    Page, Section, Program, TeamMember, Partnership, SponsorshipTier,
    NewsArticle, Testimonial, ImpactMetric, ContactInfo, InquiryType,
    SocialMedia, SiteSettings, Sponsor, ProgramSubContent, GalleryItem, User,
    ContentItem
)

def get_image(folder, filename):
    """Helper to return the image filename. Images are pre-generated."""
    return filename

def wipe_db():
    print("Wiping existing data...")
    db.session.query(GalleryItem).delete()
    db.session.query(ProgramSubContent).delete()
    db.session.query(Sponsor).delete()
    db.session.query(SiteSettings).delete()
    db.session.query(SocialMedia).delete()
    db.session.query(InquiryType).delete()
    db.session.query(ContactInfo).delete()
    db.session.query(ImpactMetric).delete()
    db.session.query(Testimonial).delete()
    db.session.query(NewsArticle).delete()
    db.session.query(SponsorshipTier).delete()
    db.session.query(Partnership).delete()
    db.session.query(TeamMember).delete()
    db.session.query(Program).delete()
    db.session.query(ContentItem).delete()
    db.session.query(Section).delete()
    db.session.query(Page).delete()
    db.session.commit()

def seed_pages_and_sections():
    print("Seeding Pages & Sections...")
    
    pages_data = [
        {
            "slug": "home",
            "hero_title": "Forging the Future <br> Elevating Human Potential",
            "hero_subtitle": "A Global Institute for Cybernetics, AI, and Next-Gen Technologies",
            "hero_description": "We build ecosystems that nurture innovation—from neural interface training and robotics competitions to global AI leadership summits.",
            "sections": [
                {
                    "section_key": "intro",
                    "title": "Who We Are",
                    "content": "<p>Nebula Cybernetics Academy is a premier global technology institute offering immersive training, AI competitions, neural tech certifications, and enterprise automation services.</p><p>Our work spans youth robotics empowerment, quantum computing development, AI leadership training, and industrial cybernetics partnerships.</p><p><strong>We believe the future belongs to those who build it.</strong></p><p>Our mission is to create platforms that unlock technological potential, build advanced skills, and inspire lifelong innovation — from VR classrooms to global corporate boardrooms.</p>"
                }
            ]
        },
        {
            "slug": "about",
            "hero_title": "Engineering Tomorrow. <br>Inspiring Innovators.",
            "hero_subtitle": "",
            "hero_description": "Learn about Nebula Cybernetics Academy - our mission, vision, values, leadership, and impact in global technology education.",
            "sections": [
                {
                    "section_key": "intro",
                    "title": "About Us",
                    "content": "<p>Nebula Cybernetics Academy is a Neo-Tokyo based international technology and AI organization committed to creating platforms that accelerate human evolution. We believe that technological excellence should be accessible, celebrated, and nurtured whether it appears in a VR lab, a robotics arena, or a global stage.</p><p>Our name, <strong>Nebula</strong>, reflects the heart of our mission: a birthplace of new stars and ideas, helping individuals and institutions discover, refine, and showcase their technical brilliance.</p>",
                    "image_filename": get_image("sections", "about_intro.png")
                },
                {
                    "section_key": "journey",
                    "title": "Our Journey",
                    "content": "<p>Nebula started with a simple yet profound realization: The world is full of brilliant minds — but brilliance needs the right infrastructure.</p><p>Initially rooted in fundamental coding initiatives, the organization quickly evolved as its founders saw a larger need: enterprises needed AI capacity-building, engineers needed modern neural training, innovators needed recognition, and institutions needed platforms to collaborate and innovate in cybernetics.</p>"
                },
                {
                    "section_key": "vision",
                    "title": "Our Vision",
                    "content": "To become a leading global platform for nurturing technological excellence, empowering innovators, and advancing AI and cybernetic innovation."
                },
                {
                    "section_key": "mission",
                    "title": "Our Mission",
                    "content": "To inspire minds and connect ecosystems through impactful programs, robotics competitions, immersive learning experiences, and capacity-building initiatives that elevate both individuals and technology."
                },
                {
                    "section_key": "values",
                    "title": "Our Core Values",
                    "content": "",
                    "items": [
                        {"icon": "fas fa-microchip", "title": "Innovation",
                         "content": "We embrace new ideas, AI technologies, and cybernetic methods to reimagine education and professional development."},
                        {"icon": "fas fa-network-wired", "title": "Connectivity",
                         "content": "We believe in the power of neural networks and human collaboration to solve complex global challenges."},
                        {"icon": "fas fa-shield-alt", "title": "Ethics & Integrity",
                         "content": "We operate with a strong commitment to AI safety, ethical tech development, and transparency."},
                        {"icon": "fas fa-users", "title": "Inclusion",
                         "content": "We believe every person deserves access to high-quality technological learning and recognition."},
                        {"icon": "fas fa-globe", "title": "Global Impact",
                         "content": "We build bridges across borders, enabling shared research, technological exchange, and international opportunity."}
                    ]
                }
            ]
        },
        {
            "slug": "programs",
            "hero_title": "Programs & Initiatives",
            "hero_subtitle": "Discover Our Ecosystem of Innovation",
            "hero_description": "We offer a diverse portfolio of programs designed to empower engineers, developers, professionals, and institutions globally.",
            "sections": []
        },
        {
            "slug": "digital",
            "hero_title": "Neural Interfaces & Custom Solutions",
            "hero_subtitle": "Powering the Future of Tech Education",
            "hero_description": "Beyond our flagship events, Nebula offers robust digital solutions and cybernetic services designed to help institutions and organizations modernize their technological infrastructure.",
            "sections": [
                {
                    "section_key": "intro",
                    "title": "The Nebula Holographic Platform",
                    "content": "<p>Where AI Meets Learning, Competition, and Opportunity</p><p>In a fast-evolving world, technology education must be immersive and borderless. The Nebula Holographic Platform is our innovative technological hub designed to deliver VR competitions, neural training, certification, and engagement to learners and professionals worldwide.</p>"
                },
                {
                    "section_key": "features",
                    "title": "Key Features of the Platform",
                    "content": "",
                    "items": [
                        {"title": "Virtual Competition Arena", "subtitle": "A dedicated space for:",
                         "content": "Live VR rounds\nPractice simulations and preparatory activities\nAutomated AI scoring\nHolographic stages\nRegional and international tournaments"},
                        {"title": "Neural Learning Hub", "subtitle": "A digital classroom for:",
                         "content": "Advanced cybernetics courses\nWorkshops and VR webinars\nOn-demand holographic lessons\nDownloadable AI toolkits\nCertification badges for tech leaders"},
                        {"title": "Smart Registration & Management", "subtitle": "For all programs:",
                         "content": "Tournament entry\nTraining enrollment\nEvent ticketing\nExhibitor and sponsor registration\nAmbassador onboarding"},
                        {"title": "Blockchain Credentialing", "subtitle": "Nebula issues:",
                         "content": "Immutable digital certificates\nAchievement badges\nParticipation transcripts"},
                        {"title": "Virtual Tech Expos", "subtitle": "Companies and labs can:",
                         "content": "Host digital VR booths\nShare interactive models\nEngage with attendees\nCollect leads and inquiries"},
                        {"title": "AI Leaderboards & Dashboards", "subtitle": "Students and labs can view:",
                         "content": "Tournament rankings\nPerformance analytics\nAchievement levels\nGlobal comparisons"},
                        {"title": "Partner Portals", "subtitle": "Organizations get:",
                         "content": "Exclusive dashboards\nPartnership benefits\nResource libraries\nPriority event registration\nSponsorship opportunities"}
                    ]
                },
                {
                    "section_key": "ecosystem",
                    "title": "A Global Tech Ecosystem",
                    "content": "",
                    "items": [
                        {"title": "Robotics Competitions"},
                        {"title": "AI Training & development"},
                        {"title": "Blockchain certificates"},
                        {"title": "Partner portals"},
                        {"title": "Tech Expos"},
                        {"title": "AI Leaderboards"},
                        {"title": "Neural modules"},
                        {"title": "Registration & ticketing"},
                        {"title": "Community engagement"}
                    ]
                },
                {
                    "section_key": "app_features",
                    "title": "Coming Soon: The Nebula Neural App",
                    "content": "",
                    "items": [
                        {"icon": "fas fa-bolt", "title": "Daily AI challenges"},
                        {"icon": "fas fa-gamepad", "title": "Logic and coding games"},
                        {"icon": "fas fa-bullhorn", "title": "Tournament updates"},
                        {"icon": "fas fa-chart-line", "title": "Personal skill tracking"},
                        {"icon": "fas fa-bell", "title": "Notifications and reminders"}
                    ]
                },
                {
                    "section_key": "security",
                    "title": "Data Security & Compliance",
                    "content": "",
                    "items": [
                        {"icon": "fas fa-user-shield", "title": "Quantum privacy protection"},
                        {"icon": "fas fa-credit-card", "title": "Secure blockchain processing"},
                        {"icon": "fas fa-lock", "title": "Encrypted neural data"},
                        {"icon": "fas fa-child", "title": "Safety protocols for minors"},
                        {"icon": "fas fa-file-contract", "title": "Compliance with global tech standards"}
                    ]
                }
            ]
        },
        {
            "slug": "partnerships",
            "hero_title": "Partner with Nebula",
            "hero_subtitle": "Let's Build the Future Together",
            "hero_description": "We collaborate with tech giants, universities, corporations, and governments to create scalable technological impact.",
            "sections": [
                {
                    "section_key": "partner_intro",
                    "title": "Why Partner With Us?",
                    "content": "<p>When you partner with Nebula, you join a global network committed to technological excellence. Our partners gain access to international platforms, brand visibility among key engineering demographics, and the opportunity to drive meaningful innovation.</p>"
                }
            ]
        },
        {
            "slug": "join",
            "hero_title": "Join the Nebula Community",
            "hero_subtitle": "Take Your Next Big Step in Tech",
            "hero_description": "Whether you are a student ready to build robots, an engineer looking to upskill in AI, or a corporate partner, there is a place for you here.",
            "sections": [
                {
                    "section_key": "join_options",
                    "title": "Ways to Get Involved",
                    "content": "",
                    "items": [
                        {"icon": "fas fa-school", "title": "Universities & Labs",
                         "subtitle": "Empower your researchers. Strengthen your curriculum. Elevate your institution.",
                         "content": "International robotics competitions\nProfessional AI programs\nLab leadership training\nRecognition & awards\nExclusive VR resources",
                         "link_url": "/contact?type=school", "link_text": "➡ Register Your Lab"},
                        {"icon": "fas fa-laptop-code", "title": "Engineers & Developers",
                         "subtitle": "Advance your career through world-class AI training.",
                         "content": "Professional development courses\nAI architecture training\nNext-gen cybernetics workshops\nCertified programs through the Neural Platform",
                         "link_url": "/contact?type=training", "link_text": "➡ Enroll in Training"},
                        {"icon": "fas fa-user-astronaut", "title": "Students",
                         "subtitle": "Unlock coding confidence, engineering creativity, and global exposure.",
                         "content": "Global Robotics Tournament\nNeural Interface Bootcamp\nQuantum Computing League\nYouth Tech Expos",
                         "link_url": "/contact?type=competition", "link_text": "➡ Register for Competitions"},
                        {"icon": "fas fa-handshake", "title": "Corporate Sponsors",
                         "subtitle": "Partner for impact. Build visibility. Support technology.",
                         "content": "Direct innovation impact\nBrand visibility across labs\nAssociation with excellence and AI ethics\nYear-round engagement opportunities\nNaming and branding opportunities",
                         "link_url": "/contact?type=sponsor", "link_text": "➡ Become a Sponsor"},
                        {"icon": "fas fa-globe-americas", "title": "Regional Hub Partners",
                         "subtitle": "Bring Nebula programs to your region.",
                         "content": "Hub rights\nBrand licensing\nTraining & onboarding\nRevenue-sharing models\nExclusive regional territories",
                         "link_url": "/contact?type=country", "link_text": "➡ Apply to Be a Hub Partner"}
                    ]
                }
            ]
        },
        {
            "slug": "gallery",
            "hero_title": "Our Gallery",
            "hero_subtitle": "Moments of Innovation",
            "hero_description": "Explore highlights from our recent robotics tournaments, AI summits, and tech events.",
            "sections": []
        },
        {
            "slug": "news-impact",
            "hero_title": "News & Impact",
            "hero_subtitle": "Stories of Innovation",
            "hero_description": "Stay updated on our latest tech announcements, program highlights, and the global impact of the Nebula community.",
            "sections": []
        },
        {
            "slug": "contact",
            "hero_title": "Get in Touch",
            "hero_subtitle": "We're Here to Help",
            "hero_description": "Have questions about our AI programs, partnerships, or neural solutions? Reach out to our team today.",
            "sections": []
        }
    ]

    for p_data in pages_data:
        page = Page(
            slug=p_data["slug"],
            hero_title=p_data["hero_title"],
            hero_subtitle=p_data["hero_subtitle"],
            hero_description=p_data["hero_description"]
        )
        db.session.add(page)
        db.session.commit() # Commit to get ID
        
        for order, s_data in enumerate(p_data["sections"]):
            section = Section(
                page_id=page.id,
                section_key=s_data["section_key"],
                title=s_data["title"],
                content=s_data.get("content"),
                image_filename=s_data.get("image_filename"),
                video_url=s_data.get("video_url"),
                order=order
            )
            db.session.add(section)
            db.session.commit()  # get section id for items

            for i_order, item in enumerate(s_data.get("items", [])):
                db.session.add(ContentItem(
                    section_id=section.id,
                    title=item.get("title"),
                    subtitle=item.get("subtitle"),
                    content=item.get("content"),
                    icon=item.get("icon"),
                    link_url=item.get("link_url"),
                    link_text=item.get("link_text"),
                    order=i_order
                ))

    db.session.commit()

def seed_programs():
    print("Seeding Programs...")
    programs = [
        {
            "name": "Global Robotics Tournament",
            "slug": "global-robotics-tournament",
            "excerpt": "An international platform for engineers to showcase their robotics and automation skills.",
            "description": "The Global Robotics Tournament brings together thousands of brilliant minds from around the world to compete in autonomous bot navigation, AI integration, and robotic combat. It fosters extreme engineering and prepares the next generation for an automated future.",
            "type": "competitions",
            "icon": "fas fa-robot",
            "image_filename": get_image("programs", "gycc.png"),
            "is_featured": True,
            "order": 1,
            "subcontents": [
                {"title": "Who Can Participate", "content": "Engineers and students globally."},
                {"title": "Key Dates", "content": "Registration Opens: Jan 15\nPreliminary Round: March 10\nGlobal Finals: May 20"}
            ]
        },
        {
            "name": "Neural Interface Bootcamp",
            "slug": "neural-interface-bootcamp",
            "excerpt": "Mastering the connection between the human brain and advanced digital systems.",
            "description": "Our flagship cybernetics initiative that challenges participants to develop seamless neural-computer interfaces. More than just coding, it focuses on bio-engineering, signal processing, and AI interpretation.",
            "type": "training",
            "icon": "fas fa-brain",
            "image_filename": get_image("programs", "neural_interface.png"),
            "is_featured": True,
            "order": 2,
            "subcontents": [
                {"title": "Categories", "content": "Level 1: Fundamentals\nLevel 2: Advanced Processing\nLevel 3: Full Integration"}
            ]
        },
        {
            "name": "Quantum Computing Leadership Summit",
            "slug": "quantum-summit",
            "excerpt": "Capacity building and leadership training for modern tech pioneers.",
            "description": "A comprehensive summit designed to empower tech leaders with advanced quantum algorithms, digital foresight, and infrastructure management required for next-gen data centers.",
            "type": "training",
            "icon": "fas fa-project-diagram",
            "image_filename": get_image("programs", "quantum_summit.png"),
            "is_featured": True,
            "order": 3,
            "subcontents": []
        },
        {
            "name": "Cybernetics Excellence Awards",
            "slug": "cybernetics-awards",
            "excerpt": "Recognizing outstanding contributions in AI, robotics, and cybernetic enhancement.",
            "description": "An annual gala event that honors engineers, tech institutions, and young innovators who have made significant breakthroughs in the global technology landscape.",
            "type": "awards",
            "icon": "fas fa-trophy",
            "image_filename": get_image("programs", "cyber_awards.png"),
            "is_featured": False,
            "order": 4,
            "subcontents": []
        }
    ]

    for p in programs:
        prog = Program(
            name=p["name"],
            slug=p["slug"],
            excerpt=p["excerpt"],
            description=p["description"],
            type=p["type"],
            icon=p["icon"],
            image_filename=p["image_filename"],
            is_featured=p["is_featured"],
            order=p["order"]
        )
        db.session.add(prog)
        db.session.commit()
        
        for sc in p["subcontents"]:
            sub = ProgramSubContent(
                program_id=prog.id,
                title=sc["title"],
                content=sc["content"]
            )
            db.session.add(sub)
            
    db.session.commit()

def seed_team():
    print("Seeding Team Members...")
    team = [
        {
            "name": "Dr. Aris Thorne",
            "title": "Director of AI Ethics & Board Chairperson",
            "bio": "A visionary leader with a commitment to responsible AI, Dr. Thorne brings strategic direction, governance, and a global tech perspective.",
            "image_filename": get_image("team", "director.png")
        },
        {
            "name": "Kaelen Vance",
            "title": "Head of Cybernetic Operations",
            "bio": "With extensive experience in advanced robotics and program coordination, Kaelen oversees the execution of all Nebula initiatives, ensuring flawless technical delivery.",
            "image_filename": get_image("team", "operations.png")
        },
        {
            "name": "Lyra Jensen",
            "title": "Director, Global Tech Partnerships",
            "bio": "A global communications and cybernetics professional, Lyra leads partnership development and the brand narrative of Nebula.",
            "image_filename": get_image("team", "communications.png")
        }
    ]
    for idx, t in enumerate(team):
        member = TeamMember(
            name=t["name"],
            title=t["title"],
            bio=t["bio"],
            image_filename=t["image_filename"],
            order=idx
        )
        db.session.add(member)
    db.session.commit()

def seed_partnerships():
    print("Seeding Partnerships...")
    partner = Partnership(
        type="Corporate",
        title="OmniCorp Tech",
        description="A leading cybernetics enterprise providing hardware infrastructure for our holographic and neural initiatives.",
        benefits="Brand Visibility\nAccess to Engineering Talent Pool\nVIP Tech Summit Access",
        image_filename=get_image("partners", "partner_logo.png")
    )
    db.session.add(partner)
    db.session.commit()
    
    tier = SponsorshipTier(
        partnership_id=partner.id,
        tier_name="Quantum Sponsor",
        benefits="All Quantum Benefits included"
    )
    db.session.add(tier)
    db.session.commit()

def seed_news_and_testimonials():
    print("Seeding News and Testimonials...")
    articles = [
        {
            "title": "Nebula Launches New Holographic Learning Platform",
            "category": "Announcements",
            "excerpt": "We are thrilled to announce the launch of our new comprehensive VR platform designed specifically for our global tech network.",
            "content": "<p>Following months of development, our new platform is live. It offers seamless registration, interactive 3D materials, and real-time live tournament streaming in full VR.</p>",
            "image_filename": get_image("news", "news_platform.png")
        },
        {
            "title": "Highlights from the 2026 Global Robotics Finals",
            "category": "Events",
            "excerpt": "Over 500 engineers from 20 countries participated in this year's intense autonomous bot tournament in Neo-Tokyo.",
            "content": "<p>The competition was fierce, and the level of engineering on display was extraordinary. Congratulations to all the participants and winners.</p>",
            "image_filename": get_image("news", "news_robotics.png")
        }
    ]
    for a in articles:
        db.session.add(NewsArticle(
            title=a["title"],
            category=a["category"],
            excerpt=a["excerpt"],
            content=a["content"],
            image_filename=a["image_filename"],
            date_published=datetime.utcnow()
        ))
        
    testimonials = [
        {
            "author_name": "Dr. Silas Vane",
            "author_role": "Principal, Institute of Advanced AI",
            "content": "Partnering with Nebula has completely transformed our lab's capabilities. The quality of their neural training programs is unmatched.",
            "image_filename": get_image("testimonials", "test_principal.png")
        },
        {
            "author_name": "Elara Vance",
            "author_role": "Cybernetics Student",
            "content": "My engineering skills skyrocketed after participating in the Global Robotics Tournament. It was a life-changing technological experience.",
            "image_filename": get_image("testimonials", "test_student.png")
        }
    ]
    for t in testimonials:
        db.session.add(Testimonial(**t))
        
    db.session.commit()

def seed_settings_metrics():
    print("Seeding Settings and Metrics...")
    
    db.session.add(SiteSettings(
        site_name="Nebula Cybernetics Academy",
        footer_description="Accelerating human evolution globally through innovative tech programs and AI events.",
        copyright_text="&copy; 2026 Nebula Cybernetics Academy. All Rights Reserved."
    ))
    
    metrics = [
        {"label": "Engineers Trained", "value": "100,000+", "icon": "fas fa-microchip", "order": 1},
        {"label": "Global Nodes", "value": "35+", "icon": "fas fa-network-wired", "order": 2},
        {"label": "Partner Labs", "value": "300+", "icon": "fas fa-flask", "order": 3},
        {"label": "Neural Models Deployed", "value": "10,000+", "icon": "fas fa-brain", "order": 4}
    ]
    for m in metrics:
        db.session.add(ImpactMetric(**m))
        
    db.session.add(ContactInfo(
        info_type="Headquarters",
        location_department="Neo-Tokyo, Japan",
        email="connect@nebulacybernetics.com",
        phone="+81 90 1234 5678",
        address="Sector 7G Innovation Spire\nNeo-Tokyo Tech District\nJapan",
        hours="Mon-Fri, 00:00 - 24:00 (Always Online)"
    ))
    
    socials = [
        {"platform": "LinkedIn", "url": "https://linkedin.com/company/nebula-cybernetics"},
        {"platform": "Twitter", "url": "https://twitter.com/nebulacyber"},
        {"platform": "Instagram", "url": "https://instagram.com/nebulacyber"}
    ]
    for s in socials:
        db.session.add(SocialMedia(**s))
        
    inquiry_types = ["General Inquiry", "Tech Partnership", "Tournament Registration", "Media/Press"]
    for idx, it in enumerate(inquiry_types):
        db.session.add(InquiryType(name=it, value=it.lower().replace(" ", "_"), order=idx))

    db.session.commit()

def seed_gallery():
    print("Seeding Gallery...")
    prog = Program.query.first()
    
    images = [
        {"title": "Robotics Lab Workshop", "file": "gallery_building.png"},
        {"title": "Neural Implant Testing", "file": "gallery_implants.png"},
        {"title": "AI Tournament Finals", "file": "gallery_stage.png"},
        {"title": "Class of 2026 Graduation", "file": "gallery_grad.png"}
    ]
    
    for item in images:
        db.session.add(GalleryItem(
            title=item["title"],
            category="Events",
            program_id=prog.id if prog else None,
            image_filename=item["file"]
        ))
    db.session.commit()
    
def ensure_admin():
    print("Ensuring Admin user exists...")
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD')
    if not password:
        password = secrets.token_urlsafe(16)
        print("\n" + "=" * 60)
        print("  No ADMIN_PASSWORD set. Generated a temporary password.")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print("  Save this now and change it after first login.")
        print("=" * 60 + "\n")
    admin = User.query.filter_by(username=username).first()
    if not admin:
        admin = User(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # First ensure database tables exist (create if they don't)
        db.create_all()
        
        # Then seed data
        wipe_db()
        seed_pages_and_sections()
        seed_programs()
        seed_team()
        seed_partnerships()
        seed_news_and_testimonials()
        seed_settings_metrics()
        seed_gallery()
        ensure_admin()
        print("Database seeded successfully!")
