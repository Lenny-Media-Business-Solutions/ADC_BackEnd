"""
Script to populate the database with initial programs from the frontend constants.
Run this with: python populate_programs.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from programs.models import Program

# Define the programs (from Front_End/constants.tsx)
programs_data = [
    {
        "title": "Peacebuilding & Conflict Resolution",
        "description": "Ensuring peaceful coexistence among agro-pastoralist communities in South Sudan through inter-community meetings and dialogues under trees. We focus on mitigating resource-based conflicts stemming from inadequate water and pastures.",
        "objectives": "Ensure peaceful coexistence among agro-pastoralists communities.\nFacilitate inter-community meetings and dialogues.\nMediate resource-based conflicts over water and pastures.",
        "status": "active"
    },
    {
        "title": "Sustainable Livelihoods",
        "description": "Improving livelihoods in South Sudan through oxen plowing, technical training, and livestock health services to enhance production and income generation for rural communities.",
        "objectives": "Improve rural household livelihoods.\nEnhance production through oxen plowing and modern farming.\nSupport income generation via livestock health and markets.",
        "status": "active"
    },
    {
        "title": "DRR & Resilience",
        "description": "Building resilience in South Sudan through food preservation techniques like hanging maize/corn for drying and environmental conservation to respond to climate disasters.",
        "objectives": "Train communities in disaster preparedness.\nBuild resilience via traditional maize drying and preservation.\nStrengthen community response to climate shocks.",
        "status": "active"
    },
    {
        "title": "Good Governance & Accountability",
        "description": "Capacity building in South Sudan through indoor workshops for community leaders to lead in a fair, transparent, and rights-based manner.",
        "objectives": "Promote fair and transparent leadership.\nStrengthen community-level accountability.\nBuild capacity for local community leaders.",
        "status": "active"
    }
]

def populate_programs():
    """Create programs in the database if they don't exist"""
    created_count = 0
    
    for program_data in programs_data:
        # Check if program already exists by title
        program, created = Program.objects.get_or_create(
            title=program_data["title"],
            defaults={
                "description": program_data["description"],
                "objectives": program_data["objectives"],
                "status": program_data["status"]
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created program: {program.title} (ID: {program.id})")
        else:
            print(f"- Program already exists: {program.title} (ID: {program.id})")
    
    print(f"\n{'=' * 50}")
    print(f"Summary: {created_count} new program(s) created")
    print(f"Total programs in database: {Program.objects.count()}")
    print(f"{'=' * 50}\n")
    
    # Display all programs
    print("All programs in database:")
    for program in Program.objects.all():
        print(f"  ID {program.id}: {program.title}")

if __name__ == "__main__":
    print("Populating programs...")
    populate_programs()
    print("\nDone! You can now create projects in the Admin Dashboard.")
