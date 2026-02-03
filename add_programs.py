# Quick script to add programs via Django shell
from programs.models import Program

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

for p_data in programs_data:
    prog, created = Program.objects.get_or_create(title=p_data['title'], defaults=p_data)
    if created:
        print(f"Created: {prog.title} (ID: {prog.id})")
    else:
        print(f"Exists: {prog.title} (ID: {prog.id})")

print(f"\nTotal programs: {Program.objects.count()}")
for p in Program.objects.all():
    print(f"  - ID {p.id}: {p.title}")
