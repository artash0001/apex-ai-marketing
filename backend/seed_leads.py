#!/usr/bin/env python3
"""
Generate 50 sample leads for Dubai real estate outreach
Run: python3 seed_leads.py
"""
import json
import uuid
from datetime import datetime

# Target personas for Dubai real estate
LEAD_TEMPLATES = [
    {
        'industry': 'Real Estate',
        'pain_points': 'No digital presence, relying only on referrals and property portals',
        'observation': 'active on Property Finder but weak social media presence',
        'result_example': '50 qualified leads per month and 3x revenue growth in 4 months'
    },
    {
        'industry': 'Real Estate Development',
        'pain_points': 'High competition in Dubai market, need to differentiate from other developers',
        'observation': 'launching new projects but marketing feels generic',
        'result_example': 'sold out 40% of units through digital marketing before launch'
    },
    {
        'industry': 'Luxury Real Estate',
        'pain_points': 'Struggling to reach international buyers, high-value properties sitting unsold',
        'observation': 'amazing properties but Instagram content looks amateur',
        'result_example': 'closed 3 luxury deals worth $15M+ from LinkedIn outreach'
    },
    {
        'industry': 'Property Management',
        'pain_points': 'High tenant turnover, difficulty attracting quality tenants',
        'observation': 'great reviews from current clients but no marketing to new ones',
        'result_example': 'reduced vacancy rate from 25% to 8% in 6 months'
    },
    {
        'industry': 'Commercial Real Estate',
        'pain_points': 'Long sales cycles, decision makers hard to reach',
        'observation': 'relying on brokers but no direct digital lead generation',
        'result_example': 'shortened sales cycle from 9 months to 4 months'
    }
]

def generate_leads():
    leads = []
    
    companies = [
        'Golden Sands Realty', 'Dubai Elite Properties', 'Palm View Developers',
        'Luxury Living Dubai', 'Prime Location Real Estate', 'Emirates Property Group',
        'Skyline Investments', 'Marina Bay Residences', 'Desert Rose Properties',
        'Oasis Homes Dubai', 'Burj Realty', 'Downtown Dubai Properties',
        'Jumeirah Estates', 'Arabian Ranches Agency', 'Dubai Hills Realtor',
        'Palm Jumeirah Experts', 'Business Bay Properties', 'DIFC Realty',
        'Al Barari Homes', 'Emirates Hills Luxury', 'Bluewaters Residences',
        'City Walk Properties', 'Port De La Mer', 'Emaar Specialist Agency',
        'Damac Preferred Agent', 'Meraas Partner Agency', 'Ellington Properties',
        'Sobha Realty Partner', 'Nakheel Premier Agent', 'Aldar Exclusive',
        'Bloom Properties', 'District One Residences', 'Mohammed Bin Rashid City',
        'Tilal Al Ghaf Specialist', 'Arabian Ranches III', 'Dubai South Properties',
        'Emaar Beachfront', 'Dubai Creek Harbour', 'Meydan Heights',
        'Jumeirah Golf Estates', 'Victory Heights', 'The Villa Dubai',
        'Damac Hills', 'Akoya Oxygen', 'Trump Estates Dubai',
        'Paramount Hotel Residences', 'The Address Residences', 'Vida Dubai',
        'Rove Hotels Dubai', 'FIVE Palm Jumeirah Residences', 'Atlantis The Royal'
    ]
    
    for i, company in enumerate(companies[:50], 1):
        template = LEAD_TEMPLATES[i % len(LEAD_TEMPLATES)]
        
        lead = {
            'id': str(uuid.uuid4()),
            'name': f'Contact {i}',
            'company': company,
            'email': f'info@{company.lower().replace(" ", "-")}.ae',
            'industry': template['industry'],
            'website': f'https://www.{company.lower().replace(" ", "-")}.ae',
            'pain_points': template['pain_points'],
            'observation': template['observation'],
            'result_example': template['result_example'],
            'outreach_status': 'new',
            'sequence_step': 0,
            'created_at': datetime.now().isoformat(),
            'source': 'seed_dubai_real_estate'
        }
        leads.append(lead)
    
    return leads

if __name__ == '__main__':
    leads = generate_leads()
    
    with open('/opt/apex-digital/backend/dubai_leads.json', 'w') as f:
        json.dump(leads, f, indent=2)
    
    print(f'✅ Generated {len(leads)} leads for Dubai real estate outreach')
    print(f'📁 Saved to: /opt/apex-digital/backend/dubai_leads.json')
    print(f'\nSample lead:')
    print(json.dumps(leads[0], indent=2))