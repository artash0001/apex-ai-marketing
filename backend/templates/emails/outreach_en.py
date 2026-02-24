"""
Apex AI Marketing - English Cold Outreach Email Sequence

4-email cold outreach sequence for English-speaking prospects.
Each email follows a specific purpose in the nurture flow:
  1. The Infrastructure Question (Day 1) - Open with curiosity
  2. The Mini-Audit (Day 4) - Provide immediate value
  3. The Evidence (Day 8) - Show methodology in action
  4. The Breakup (Day 14) - Final touch, low-pressure close

Placeholders:
  {name} - Prospect first name
  {company} - Company name
  {specific_finding} - Personalized observation about their business
"""

OUTREACH_SEQUENCE_EN = {
    1: {
        "name": "The Infrastructure Question",
        "day": 1,
        "subject": "Quick question about {company}'s growth infrastructure",
        "body": (
            "<p>Hi {name},</p>"
            "<p>I was looking at {company}'s online presence and noticed "
            "something interesting about {specific_finding}.</p>"
            "<p>Most companies in your space are leaving significant revenue "
            "on the table because their marketing operates as disconnected "
            "campaigns rather than integrated infrastructure. The difference "
            "between a campaign and an engine is predictability.</p>"
            "<p>Quick question: if you could get a clear diagnostic of where "
            "{company} is losing potential customers in your digital "
            "funnel &mdash; would that be useful?</p>"
            "<p>We run complimentary growth infrastructure audits for companies "
            "that fit our profile. Takes 48 hours, zero commitment, and you "
            "walk away with an actionable report either way.</p>"
            "<p>Worth a look?</p>"
            "<p>Best,<br/>"
            "Apex AI Marketing<br/>"
            "<em>AI Growth Infrastructure for Predictable Pipeline</em></p>"
        ),
    },
    2: {
        "name": "The Mini-Audit",
        "day": 4,
        "subject": "Found something on {company}'s site",
        "body": (
            "<p>Hi {name},</p>"
            "<p>I actually went ahead and did a quick surface-level review "
            "of {company}'s digital presence. Here is what stood out:</p>"
            "<p><strong>{specific_finding}</strong></p>"
            "<p>This is just from a 15-minute look. Our full growth "
            "infrastructure audit covers 7 layers of your marketing stack "
            "and typically uncovers 10-15 high-impact opportunities.</p>"
            "<p>The audit itself takes our AI systems about 48 hours. "
            "We present findings in a 30-minute call, and you keep the full "
            "report regardless of whether we work together.</p>"
            "<p>Here is our calendar if you would like to schedule: "
            "<a href='https://calendly.com/apex-ai-marketing'>Book a slot</a></p>"
            "<p>Best,<br/>"
            "Apex AI Marketing</p>"
        ),
    },
    3: {
        "name": "The Evidence",
        "day": 8,
        "subject": "How companies like {company} build growth engines",
        "body": (
            "<p>Hi {name},</p>"
            "<p>Wanted to share something relevant. We recently published "
            "our methodology breakdown on how companies in your space "
            "transform scattered marketing efforts into predictable growth "
            "engines.</p>"
            "<p>The core insight: most businesses run 5-8 disconnected "
            "marketing activities. When you architect these as an integrated "
            "system, the compound effect typically delivers 3-5x the results "
            "at the same spend.</p>"
            "<p>Key shifts we see work consistently:</p>"
            "<ul>"
            "<li>From random content &rarr; to strategic content engine "
            "with measurable pipeline impact</li>"
            "<li>From generic ads &rarr; to AI-optimized campaigns that "
            "improve weekly</li>"
            "<li>From hoping for leads &rarr; to engineered inbound "
            "with predictable volume</li>"
            "</ul>"
            "<p>Given what I noticed about {specific_finding}, I think "
            "{company} would see strong results from this approach.</p>"
            "<p>Happy to walk through the specifics in a 20-minute call. "
            "No pitch, just strategy.</p>"
            "<p>Best,<br/>"
            "Apex AI Marketing</p>"
        ),
    },
    4: {
        "name": "The Breakup",
        "day": 14,
        "subject": "Closing the loop, {name}",
        "body": (
            "<p>Hi {name},</p>"
            "<p>I have reached out a few times about the growth opportunity "
            "I spotted for {company}. I completely understand if the timing "
            "is not right or this is not a priority.</p>"
            "<p>I will close this thread, but wanted to leave you with "
            "one thought:</p>"
            "<p>The finding I mentioned about {specific_finding} is the kind "
            "of thing that costs companies in your space real money every month "
            "it goes unaddressed. Not as a scare tactic &mdash; just an "
            "observation from analyzing hundreds of businesses.</p>"
            "<p>If things change or you want that complimentary audit down "
            "the road, my calendar is always open: "
            "<a href='https://calendly.com/apex-ai-marketing'>Book anytime</a></p>"
            "<p>Wishing {company} great growth ahead.</p>"
            "<p>Best,<br/>"
            "Apex AI Marketing</p>"
        ),
    },
}
