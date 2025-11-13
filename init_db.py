"""
Database initialization script
Populates the database with initial portfolio data and creates default admin user
"""
from app import app
from models import db, User, Profile, Skill, Project, ProjectTag, SocialLink


def init_database():
    """Initialize database with portfolio data"""
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        # Create default admin user
        print("Creating default admin user...")
        admin = User(
            username='admin',
            email='admin@hersel.it'
        )
        admin.set_password('admin123')  # CHANGE THIS PASSWORD AFTER FIRST LOGIN!
        db.session.add(admin)

        # Create profile information
        print("Adding profile information...")
        profile = Profile(
            title="Il ponte tra sistemi e sviluppo web",
            lead_text="Con oltre 7 Anni di esperienza nello sviluppo di applicazioni web con Python Flask, offro soluzioni complete end-to-end.",
            description_1="La mia doppia specializzazione mi permette di comprendere a fondo l'intero ciclo di vita delle applicazioni, dall'architettura del server fino all'implementazione e al deployment.",
            description_2="Mi piace risolvere problemi complessi e creare soluzioni che siano robuste, scalabili e facili da mantenere.",
            years_experience=7,
            profile_image='img/personal.webp'
        )
        db.session.add(profile)

        # Create skills
        print("Adding skills...")
        skills_data = [
            {"name": "Linux", "icon_class": "fab fa-linux", "category": "OS", "display_order": 1},
            {"name": "Windows", "icon_class": "fab fa-windows", "category": "OS", "display_order": 2},
            {"name": "Python", "icon_class": "fab fa-python", "category": "Language", "display_order": 3},
            {"name": "Flask", "icon_class": "fas fa-flask", "category": "Framework", "display_order": 4},
            {"name": "Database", "icon_class": "fas fa-database", "category": "Tool", "display_order": 5},
            {"name": "Docker", "icon_class": "fab fa-docker", "category": "Tool", "display_order": 6},
            {"name": "Server", "icon_class": "fas fa-server", "category": "Infrastructure", "display_order": 7},
            {"name": "Networking", "icon_class": "fas fa-network-wired", "category": "Infrastructure", "display_order": 8},
        ]

        for skill_data in skills_data:
            skill = Skill(**skill_data)
            db.session.add(skill)

        # Create projects
        print("Adding projects...")

        # Project 1: Database Backup Script
        project1 = Project(
            title="Script di Backup Database (MariaDB/MySQL)",
            description="Script in Bash per sistemi Linux che permette l'automazione dei backup database",
            image_url="img/bash.webp",
            github_url="https://github.com/BluLupo/server-script/tree/main/db_bash_backup-main",
            display_order=1,
            animation_delay="0s"
        )
        db.session.add(project1)
        db.session.flush()  # Get project1.id

        # Project 1 tags
        project1_tags = [
            ProjectTag(project_id=project1.id, name="Bash", color_class="bg-primary", display_order=1),
            ProjectTag(project_id=project1.id, name="Linux", color_class="bg-info", display_order=2),
        ]
        db.session.add_all(project1_tags)

        # Project 2: ByteStash
        project2 = Project(
            title="Personal ByteStash",
            description="Ho realizzato un repository personale di snippet sfruttando Bytestash, ottimizzando la gestione del codice riutilizzabile e migliorando la produttività nello sviluppo di progetti software.",
            image_url="img/byte.webp",
            demo_url="https://bytestash.gwserver.it/public/snippets",
            display_order=2,
            animation_delay="0.2s"
        )
        db.session.add(project2)
        db.session.flush()

        # Project 2 tags
        project2_tags = [
            ProjectTag(project_id=project2.id, name="LXC", color_class="bg-warning text-dark", display_order=1),
            ProjectTag(project_id=project2.id, name="Proxmox", color_class="bg-dark", display_order=2),
            ProjectTag(project_id=project2.id, name="Nginx", color_class="bg-info", display_order=3),
            ProjectTag(project_id=project2.id, name="Reverse Proxy", color_class="bg-secondary", display_order=4),
            ProjectTag(project_id=project2.id, name="Linux", color_class="bg-primary", display_order=5),
            ProjectTag(project_id=project2.id, name="Self-hosted", color_class="bg-primary", display_order=6),
        ]
        db.session.add_all(project2_tags)

        # Project 3: Nextcloud
        project3 = Project(
            title="Nextcloud Personale",
            description="Installazione di Nextcloud su container LXC con database PostgreSQL e caching Redis, integrato in una rete privata con gestione IP tramite server DHCP.",
            image_url="img/next.webp",
            demo_url="https://cloud.gwserver.it",
            display_order=3,
            animation_delay="0.4s"
        )
        db.session.add(project3)
        db.session.flush()

        # Project 3 tags
        project3_tags = [
            ProjectTag(project_id=project3.id, name="Nextcloud", color_class="bg-primary", display_order=1),
            ProjectTag(project_id=project3.id, name="PostgreSQL", color_class="bg-secondary", display_order=2),
            ProjectTag(project_id=project3.id, name="Redis", color_class="bg-info", display_order=3),
            ProjectTag(project_id=project3.id, name="LXC", color_class="bg-warning text-dark", display_order=4),
            ProjectTag(project_id=project3.id, name="Proxmox", color_class="bg-dark", display_order=5),
            ProjectTag(project_id=project3.id, name="Rete Privata", color_class="bg-success", display_order=6),
            ProjectTag(project_id=project3.id, name="DHCP Server", color_class="bg-secondary", display_order=7),
        ]
        db.session.add_all(project3_tags)

        # Create social links
        print("Adding social links...")
        social_links_data = [
            {
                "platform_name": "LinkedIn",
                "url": "https://linkedin.com/in/hersel",
                "icon_class": "fab fa-linkedin",
                "display_order": 1,
                "animation_delay": "0.1s"
            },
            {
                "platform_name": "GitHub",
                "url": "https://github.com/blulupo",
                "icon_class": "fab fa-github",
                "display_order": 2,
                "animation_delay": "0.2s"
            },
            {
                "platform_name": "Stack Overflow",
                "url": "https://stackoverflow.com/users/11765177/hersel-giannella",
                "icon_class": "fab fa-stack-overflow",
                "display_order": 3,
                "animation_delay": "0.3s"
            },
            {
                "platform_name": "CodeWars",
                "url": "https://www.codewars.com/users/BluLupo",
                "icon_class": "fas fa-code",
                "display_order": 4,
                "animation_delay": "0.4s"
            },
            {
                "platform_name": "Blog",
                "url": "https://blog.hersel.it",
                "icon_class": "fas fa-blog",
                "display_order": 5,
                "animation_delay": "0.5s"
            },
            {
                "platform_name": "Email",
                "url": "mailto:info@hersel.it",
                "icon_class": "fas fa-envelope",
                "display_order": 6,
                "animation_delay": "0.6s"
            },
        ]

        for link_data in social_links_data:
            social_link = SocialLink(**link_data)
            db.session.add(social_link)

        # Commit all changes
        print("Committing changes to database...")
        db.session.commit()

        print("\n✅ Database initialized successfully!")
        print(f"   - Admin User: 1 record")
        print(f"   - Profile: 1 record")
        print(f"   - Skills: {len(skills_data)} records")
        print(f"   - Projects: 3 records")
        print(f"   - Project Tags: {len(project1_tags) + len(project2_tags) + len(project3_tags)} records")
        print(f"   - Social Links: {len(social_links_data)} records")
        print("\n" + "="*60)
        print("🔐 DEFAULT ADMIN CREDENTIALS")
        print("="*60)
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY AFTER FIRST LOGIN!")
        print("="*60)


if __name__ == '__main__':
    init_database()
