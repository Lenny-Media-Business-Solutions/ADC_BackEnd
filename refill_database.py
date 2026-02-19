import os
import django
import json
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from programs.models import Program
from projects.models import Project
from gallery.models import Gallery
from blog.models import News
from impact.models import ImpactStory
from users.models import User

def refill_data():
    print("--- Refilling Database with Original MySQL Data ---")

    # Load original data if available
    original_data = {}
    if os.path.exists('original_data.json'):
        with open('original_data.json', 'r') as f:
            original_data = json.load(f)
        print("[*] Loaded original data from original_data.json")
    else:
        print("[!] original_data.json not found. Falling back to basics.")
        return

    # 1. Create Admin User if not exists
    if not User.objects.filter(email='admin@adc.org').exists():
        User.objects.create_superuser(
            email='admin@adc.org',
            password='password123',
            full_name='ADC Administrator'
        )
        print("[+] Created Superuser: admin@adc.org (password: password123)")
    else:
        print("[-] Superuser already exists.")

    # Clear existing data to avoid duplicates/confusion
    print("[*] Clearing existing records from PostgreSQL...")
    ImpactStory.objects.all().delete()
    News.objects.all().delete()
    Project.objects.all().delete()
    Program.objects.all().delete()
    Gallery.objects.all().delete()

    # 2. Programs Data
    program_map = {}
    for p_data in original_data.get("programs", []):
        prog = Program.objects.create(
            id=p_data['id'], # Keep original ID
            title=p_data['title'],
            description=p_data['description'],
            objectives=p_data['objectives'],
            status=p_data['status']
        )
        program_map[p_data['id']] = prog
        print(f"[+] Restored program: {prog.title}")

    # 3. Projects Data
    for pr_data in original_data.get("projects", []):
        prog = program_map.get(pr_data["program_id"])
        if prog:
            proj = Project.objects.create(
                id=pr_data['id'],
                title=pr_data['title'],
                description=pr_data['description'],
                location=pr_data['location'],
                status=pr_data['status'],
                program=prog,
                image=pr_data['image']
            )
            print(f"[+] Restored project: {proj.title} (Image: {proj.image})")

    # 4. Gallery Data
    for g_data in original_data.get("gallery", []):
        gal = Gallery.objects.create(
            id=g_data['id'],
            title=g_data['title'],
            image=g_data['image'],
            caption=g_data['caption'],
            category=g_data['category']
        )
        print(f"[+] Restored gallery item: {gal.title}")

    # 5. News Data
    for n_data in original_data.get("news", []):
        item = News.objects.create(
            id=n_data['id'],
            title=n_data['title'],
            slug=n_data['slug'],
            summary=n_data['summary'],
            content=n_data['content'],
            image=n_data['image'],
            is_published=n_data['is_published']
        )
        print(f"[+] Restored news: {item.title}")

    # 6. Impact Stories
    for i_data in original_data.get("impact", []):
        story = ImpactStory.objects.create(
            id=i_data['id'],
            title=i_data['title'],
            slug=i_data['slug'],
            summary=i_data['summary'],
            content=i_data['content'],
            image=i_data['image'],
            is_featured=i_data['is_featured']
        )
        print(f"[+] Restored impact story: {story.title}")

    print("\n--- Restoration Complete ---")

if __name__ == "__main__":
    refill_data()
