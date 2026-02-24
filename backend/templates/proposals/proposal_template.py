"""
Apex AI Marketing - Growth Engine Proposal Template

Full proposal template with all 10 sections. Used by the Proposal Builder
agent to generate client-facing proposals based on audit findings and
strategic recommendations.

Sections:
  1. Cover & Introduction
  2. The Challenge (Current State)
  3. The Opportunity (What We Found)
  4. Our Approach (Growth Infrastructure Model)
  5. Recommended Engine Configuration
  6. 90-Day Roadmap
  7. Team & AI Infrastructure
  8. Investment & Pricing
  9. Expected Outcomes & KPIs
  10. Next Steps & Agreement
"""

PROPOSAL_TEMPLATE = """# Growth Engine Proposal

## {{ company or client_name }}

**Prepared by:** Apex AI Marketing
**Date:** {{ date }}
**Valid until:** {{ valid_until }}
**Proposal ID:** {{ proposal_id }}

---

## 1. Introduction

Dear {{ client_name }},

{{ introduction | default("Thank you for the opportunity to present this growth engine proposal for " + (company or client_name) + ". Based on our comprehensive Growth Infrastructure Audit, we have identified significant opportunities to transform your marketing from disconnected campaigns into a predictable growth engine.") }}

This proposal outlines a customized plan to build the infrastructure that will drive predictable, measurable growth for {{ company or client_name }}.

---

## 2. The Challenge: Current State

{{ current_state_summary | default("Based on our audit findings:") }}

### Key Issues Identified
{% for issue in current_issues | default([]) %}
- **{{ issue.title }}**: {{ issue.description }}
{% endfor %}

### Impact on Business
{{ business_impact | default("These infrastructure gaps are resulting in missed opportunities, unpredictable lead flow, and inefficient marketing spend.") }}

### Current Infrastructure Score: {{ current_score | default("--") }}/100

---

## 3. The Opportunity

{{ opportunity_summary | default("Our audit uncovered substantial growth potential that can be unlocked by restructuring your marketing as integrated infrastructure.") }}

### Revenue Impact Potential
{% for opportunity in opportunities | default([]) %}
- **{{ opportunity.area }}**: {{ opportunity.potential }}
{% endfor %}

### What Changes
| From (Current) | To (With Growth Engines) |
|----------------|------------------------|
{% for shift in shifts | default([]) %}| {{ shift.current }} | {{ shift.future }} |
{% endfor %}

---

## 4. Our Approach: The Growth Infrastructure Model

### How We Work

Unlike traditional agencies that run campaigns, we build **growth infrastructure** -- marketing systems that compound over time and become more effective with every iteration.

**Three Pillars:**

1. **AI-Powered Execution** -- Claude-based agents handle research, content generation, optimization, and analysis at a speed and consistency that human teams cannot match.

2. **Structured Experimentation** -- Every action is a hypothesis. We measure, learn, and iterate weekly. No guesswork.

3. **Transparent Reporting** -- You see exactly what is happening, what is working, and why. Weekly reports, real-time dashboard, direct Telegram updates.

### The Engine Model

Each "engine" is a self-contained growth system focused on a specific outcome:
{{ engine_model_description | default("Engines run continuously, learning and improving. They are not projects with end dates -- they are infrastructure that compounds.") }}

---

## 5. Recommended Engine Configuration

Based on {{ company or client_name }}'s specific situation, we recommend:

{% for engine in recommended_engines | default([]) %}
### Engine {{ loop.index }}: {{ engine.name }}

**Purpose:** {{ engine.purpose }}
**Priority:** {{ engine.priority | default("Core") }}

**What is included:**
{% for item in engine.deliverables | default([]) %}
- {{ item }}
{% endfor %}

**Expected outcomes:**
{% for outcome in engine.outcomes | default([]) %}
- {{ outcome }}
{% endfor %}

**Monthly investment:** {{ engine.price | default("See pricing section") }}

---
{% endfor %}

## 6. 90-Day Roadmap

### Phase 1: Foundation (Days 1-30)
{% for item in phase_1 | default([]) %}
- {{ item }}
{% endfor %}
{{ phase_1_description | default("Onboarding, access setup, brand voice calibration, first deliverables, baseline metrics established.") }}

### Phase 2: Activation (Days 31-60)
{% for item in phase_2 | default([]) %}
- {{ item }}
{% endfor %}
{{ phase_2_description | default("All engines at full capacity. First experiments running. Initial performance data flowing. Optimization cycles begin.") }}

### Phase 3: Optimization (Days 61-90)
{% for item in phase_3 | default([]) %}
- {{ item }}
{% endfor %}
{{ phase_3_description | default("Data-driven refinement. Experiment learnings implemented. Growth compounding visible. First quarterly review and roadmap adjustment.") }}

### Key Milestones

| Milestone | Target Date | Success Criteria |
|-----------|------------|-----------------|
{% for milestone in milestones | default([]) %}| {{ milestone.name }} | {{ milestone.date }} | {{ milestone.criteria }} |
{% endfor %}

---

## 7. Team & AI Infrastructure

### Your Team
{{ team_description | default("You get a dedicated team combining human strategy with AI execution.") }}

- **Strategy Lead** -- Senior strategist overseeing your growth roadmap
- **AI Agent Fleet** -- Specialized Claude-based agents for each engine
- **Quality Gate** -- Every deliverable passes AI + human quality review

### AI Infrastructure
- **Claude API** -- Powers all content generation, analysis, and optimization
- **Structured Pipelines** -- Automated workflows for consistent quality
- **Real-Time Monitoring** -- Telegram notifications for important events
- **Client Portal** -- Full visibility into progress and deliverables

---

## 8. Investment & Pricing

### Engine Pricing

| Engine | Monthly Investment |
|--------|-------------------|
{% for engine in recommended_engines | default([]) %}| {{ engine.name }} | {{ engine.price | default("TBD") }} |
{% endfor %}
| **Total** | **{{ total_monthly | default("TBD") }}/month** |

### Payment Terms
{{ payment_terms | default("- Monthly billing, payable within 14 days of invoice\\n- No long-term lock-in: month-to-month after initial 90-day commitment\\n- 90-day initial commitment to allow engines to reach full effectiveness") }}

### What is NOT Included
{{ exclusions | default("- Ad spend (paid directly to platforms)\\n- Third-party tool subscriptions (recommended tools discussed during onboarding)\\n- Physical event management\\n- Print design and production") }}

---

## 9. Expected Outcomes & KPIs

### Primary KPIs

| KPI | Current Baseline | 90-Day Target | 6-Month Target |
|-----|-----------------|---------------|----------------|
{% for kpi in kpis | default([]) %}| {{ kpi.name }} | {{ kpi.baseline | default("TBD") }} | {{ kpi.target_90d | default("TBD") }} | {{ kpi.target_6m | default("TBD") }} |
{% endfor %}

### How We Measure Success
{{ measurement_approach | default("Weekly performance reports track every KPI against targets. Monthly deep-dive reviews analyze trends and adjust strategy. All metrics are accessible in your client portal 24/7.") }}

### Our Commitment
{{ commitment | default("We are committed to transparency. If engines are not performing against targets, we diagnose why and adjust. Our incentive is your growth -- retained clients are our business model.") }}

---

## 10. Next Steps

To move forward:

1. **Sign this proposal** -- Digital signature below or reply confirming
2. **Kickoff call scheduled** -- Within 48 hours of signing
3. **Access setup** -- Share platform credentials securely
4. **Engines activate** -- First deliverables within 5 business days

### Agreement

By signing below, {{ company or client_name }} agrees to engage Apex AI Marketing for the engines and terms described in this proposal.

**For {{ company or client_name }}:**

Name: _________________________
Title: _________________________
Date: _________________________
Signature: _____________________

**For Apex AI Marketing:**

Name: _________________________
Date: _________________________
Signature: _____________________

---

*Questions? Contact us at hello@apexaimarketing.pro*
*Schedule a call: [https://calendly.com/apex-ai-marketing](https://calendly.com/apex-ai-marketing)*
"""


def render_proposal(
    client_name: str,
    company: str = "",
    sections: dict = None,
    language: str = "en",
    **kwargs,
) -> str:
    """Render the proposal template with Jinja2.

    Args:
        client_name: Client contact name.
        company: Company name.
        sections: dict with proposal data.
        language: Language code.
        **kwargs: Additional template variables.

    Returns:
        Rendered markdown string.
    """
    from jinja2 import Template
    from datetime import date, timedelta
    import uuid

    sections = sections or {}
    today = date.today()

    context = {
        "client_name": client_name,
        "company": company,
        "date": today.isoformat(),
        "valid_until": (today + timedelta(days=30)).isoformat(),
        "proposal_id": f"APEX-{str(uuid.uuid4())[:8].upper()}",
        # Section data
        "introduction": sections.get("introduction"),
        "current_state_summary": sections.get("current_state_summary"),
        "current_issues": sections.get("current_issues", []),
        "business_impact": sections.get("business_impact"),
        "current_score": sections.get("current_score"),
        "opportunity_summary": sections.get("opportunity_summary"),
        "opportunities": sections.get("opportunities", []),
        "shifts": sections.get("shifts", []),
        "engine_model_description": sections.get("engine_model_description"),
        "recommended_engines": sections.get("recommended_engines", []),
        "phase_1": sections.get("phase_1", []),
        "phase_1_description": sections.get("phase_1_description"),
        "phase_2": sections.get("phase_2", []),
        "phase_2_description": sections.get("phase_2_description"),
        "phase_3": sections.get("phase_3", []),
        "phase_3_description": sections.get("phase_3_description"),
        "milestones": sections.get("milestones", []),
        "team_description": sections.get("team_description"),
        "total_monthly": sections.get("total_monthly"),
        "payment_terms": sections.get("payment_terms"),
        "exclusions": sections.get("exclusions"),
        "kpis": sections.get("kpis", []),
        "measurement_approach": sections.get("measurement_approach"),
        "commitment": sections.get("commitment"),
        **kwargs,
    }

    template = Template(PROPOSAL_TEMPLATE)
    return template.render(**context)
