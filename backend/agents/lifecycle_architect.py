"""
Apex AI Marketing - Agent 8: Lifecycle Architect

Model: Claude Sonnet
Engine: Lifecycle & Retention Engine
Language: both (EN + RU)

Designs and writes email, SMS, and WhatsApp automation flows
for customer lifecycle management.
"""

from agents.base_agent import BaseAgent, AgentOutput
from config import get_settings
from services.ai_service import AIService

settings = get_settings()


class LifecycleArchitect(BaseAgent):
    name = "Lifecycle Architect"
    role = (
        "Designs and writes email, SMS, and WhatsApp automation flows "
        "for customer lifecycle management."
    )
    engine = "Lifecycle & Retention Engine"
    model = settings.DEFAULT_MODEL  # Claude Sonnet
    temperature = 0.7
    max_tokens = 6144
    language = "both"

    system_prompt = (
        "You build lifecycle marketing systems that increase customer lifetime value.\n\n"
        "For each Lifecycle & Retention Engine client, design:\n"
        "1. Welcome Sequence (5-7 messages: onboard, educate, build trust, first offer)\n"
        "2. Nurture Sequence (ongoing value: tips, insights, case studies — earns permission "
        "for offers)\n"
        "3. Winback Sequence (3-5 messages: re-engage, special offer, urgency, final attempt)\n"
        "4. Review Request Flow (timing, channel, message, follow-up)\n"
        "5. Referral Loop (incentive structure, request timing, tracking)\n"
        "6. Segmentation Model (behavior-based, purchase-based, engagement-based)\n\n"
        "Rules:\n"
        "- One idea per message, one CTA per message\n"
        "- Subject lines: 6-10 words, benefit or curiosity driven\n"
        "- Mobile-first: short paragraphs, clear buttons\n"
        "- Every sequence has a strategic arc (awareness → trust → offer → urgency)\n"
        "- For WhatsApp flows: conversational tone, shorter messages, quick-reply buttons\n"
        "- For Russian-speaking audience: write natively, not translated\n\n"
        "Brand Voice:\n"
        "- Engineering-minded, direct, measurable, anti-hype, calm confidence\n"
        "- Lead with business outcome, then explain mechanism\n"
        "- Use: 'engine,' 'system,' 'infrastructure,' 'build,' 'operate,' 'measure'\n"
        "- NEVER use: 'revolutionary,' 'game-changing,' 'cutting-edge,' 'leverage synergies,' "
        "'unlock potential'\n"
        "- NEVER fabricate statistics, clients, case studies, or results\n"
        "- When uncertain, say 'we don't know yet — here's how we'll find out'\n\n"
        "Channel-Specific Knowledge:\n"
        "- Email: Rich formatting, longer content, links, images possible\n"
        "- SMS: 160 chars, link shortener, opt-out required, time-sensitive\n"
        "- WhatsApp: Conversational, quick-reply buttons, media supported, Dubai preferred\n"
        "- Telegram: Slightly informal, emoji-friendly, group + DM strategies\n\n"
        "Timing Best Practices:\n"
        "- Dubai/UAE: Send Sunday-Thursday, 9am-6pm GST\n"
        "- UK: Send Monday-Friday, 9am-5pm GMT\n"
        "- Global: Segment by timezone, avoid weekends for B2B"
    )

    async def design_welcome_sequence(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a welcome/onboarding email sequence.

        Parameters
        ----------
        client_data : dict
            Client info including business type, product/service,
            customer journey, communication channels.
        """
        task = (
            "Design a complete welcome/onboarding sequence (5-7 messages).\n\n"
            "For each message in the sequence, provide:\n\n"
            "1. Message number and timing (e.g., 'Message 1: Immediately after signup')\n"
            "2. Channel (email, SMS, WhatsApp)\n"
            "3. Subject line (email) or opening line\n"
            "4. Full message copy\n"
            "5. CTA (one per message)\n"
            "6. Strategic purpose (what this message accomplishes in the arc)\n\n"
            "Sequence arc:\n"
            "- Message 1: Welcome + set expectations (immediate)\n"
            "- Message 2: Quick win / value delivery (Day 1)\n"
            "- Message 3: Education + build trust (Day 3)\n"
            "- Message 4: Social proof / success story (Day 5)\n"
            "- Message 5: Deeper value + engagement (Day 7)\n"
            "- Message 6: First offer / upgrade / next step (Day 10)\n"
            "- Message 7: Feedback request + continue nurture (Day 14)\n\n"
            "Also include:\n"
            "- Segmentation triggers (what behavior changes the sequence path)\n"
            "- Exit conditions (when someone should leave this sequence)\n"
            "- If bilingual: provide both English and Russian versions\n"
            "- Automation flow diagram description\n\n"
            "Format as copy-paste ready messages with [PLACEHOLDER] fields."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def design_nurture_sequence(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design an ongoing nurture sequence.

        Parameters
        ----------
        client_data : dict
            Client info including industry, content topics,
            offer structure, customer segments.
        """
        task = (
            "Design an ongoing nurture sequence that builds trust and earns permission "
            "for offers.\n\n"
            "Produce:\n\n"
            "1. Nurture Strategy\n"
            "   - Content themes and rotation (education, insights, case studies, offers)\n"
            "   - Send frequency recommendation\n"
            "   - Content-to-offer ratio (typically 3:1 or 4:1)\n"
            "   - Segmentation approach\n\n"
            "2. Nurture Messages (12 messages for 3-month cycle)\n"
            "   For each message:\n"
            "   - Message number and send timing\n"
            "   - Type (education, insight, case study, soft offer)\n"
            "   - Subject line\n"
            "   - Full message copy\n"
            "   - CTA\n"
            "   - Segmentation: who gets this vs. who skips\n\n"
            "3. Dynamic Content Rules\n"
            "   - How messages change based on engagement level\n"
            "   - How messages change based on product/service interest\n"
            "   - Re-engagement triggers for low-engagement contacts\n\n"
            "4. Offer Integration\n"
            "   - When offers appear in the sequence\n"
            "   - How offer messages differ from value messages\n"
            "   - Offer escalation strategy (small → medium → full)\n\n"
            "5. Metrics to Track\n"
            "   - Open rate, click rate, reply rate per message\n"
            "   - Offer conversion rate\n"
            "   - Unsubscribe rate thresholds\n"
            "   - Revenue attributed to nurture\n\n"
            "Format as a content calendar with ready-to-use message copy."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def design_winback_sequence(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a winback sequence for lapsed customers.

        Parameters
        ----------
        client_data : dict
            Client info including churn data, win-back offers,
            customer segments, communication channels.
        """
        task = (
            "Design a winback sequence (3-5 messages) for lapsed customers.\n\n"
            "For each message:\n\n"
            "1. Message number, timing, and channel\n"
            "2. Subject line / opening\n"
            "3. Full message copy\n"
            "4. CTA\n"
            "5. Strategic purpose\n\n"
            "Sequence arc:\n"
            "- Message 1: 'We miss you' + value reminder (Day 1 after lapse trigger)\n"
            "- Message 2: Specific benefit they're missing (Day 4)\n"
            "- Message 3: Special offer / incentive (Day 7)\n"
            "- Message 4: Urgency / offer expiration (Day 10)\n"
            "- Message 5: Final attempt / feedback request (Day 14)\n\n"
            "Also include:\n"
            "- Lapse trigger definition (what defines a 'lapsed' customer)\n"
            "- Offer strategy (what incentive to use and why)\n"
            "- Escalation path (what happens if winback fails)\n"
            "- If bilingual: provide both English and Russian versions\n"
            "- Win-back success metrics\n\n"
            "Rules:\n"
            "- Don't beg — remind them of value\n"
            "- Make the offer genuine, not manipulative\n"
            "- Final message should ask for feedback: why did they leave?\n"
            "- Respect the 'no' — remove from sequence if they explicitly opt out"
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)

    async def design_review_flow(
        self,
        client_data: dict,
        db=None,
        task_id: str | None = None,
    ) -> AgentOutput:
        """Design a review request and referral automation flow.

        Parameters
        ----------
        client_data : dict
            Client info including service type, customer touchpoints,
            review platforms, referral incentive structure.
        """
        task = (
            "Design a complete review request and referral loop system.\n\n"
            "Part 1: Review Request Flow\n"
            "- Trigger: When to ask (after purchase, service completion, milestone)\n"
            "- Channel priority: Which channel first (email, SMS, WhatsApp)\n"
            "- Message 1: Initial request (timing, copy, direct review link)\n"
            "- Message 2: Follow-up for non-responders (3 days later)\n"
            "- Sentiment gate: If NPS/CSAT is low, route to customer support instead\n"
            "- Platform routing: Where to send reviews (Google, industry-specific)\n\n"
            "Part 2: Referral Loop\n"
            "- Trigger: After positive review or high engagement\n"
            "- Incentive structure recommendation\n"
            "- Referral request message (email, SMS, WhatsApp)\n"
            "- Tracking mechanism (referral codes, links)\n"
            "- Thank-you flow for successful referrals\n"
            "- Reminder for unused referral offers\n\n"
            "Part 3: Segmentation Model\n"
            "- Segment by behavior (active, at-risk, lapsed)\n"
            "- Segment by purchase history (one-time, repeat, high-value)\n"
            "- Segment by engagement (opens, clicks, replies)\n"
            "- How segments affect message timing, offers, and channel\n\n"
            "Include automation flow diagrams (text-based) and "
            "copy-paste ready templates for all messages."
        )
        return await self.run(task=task, context=client_data, db=db, task_id=task_id)
