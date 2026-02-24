"""
Apex AI Marketing - Growth Infrastructure Audit Report Template

Markdown-formatted audit report covering all 7 layers of a company's
marketing infrastructure. Used by the Infrastructure Auditor agent.

Sections:
  1. Executive Summary
  2. Website & Technical Infrastructure
  3. SEO & Organic Visibility
  4. Content Ecosystem Assessment
  5. Social Media & Community Presence
  6. Paid Advertising Analysis
  7. Local Visibility & GMB
  8. Competitive Landscape
  9. Growth Opportunities & Priority Matrix
  10. Recommended Engine Configuration
  11. Next Steps
"""

AUDIT_TEMPLATE = """# Growth Infrastructure Audit Report

**Client:** {{ client_name }}{% if company %} ({{ company }}){% endif %}
**Prepared by:** Apex AI Marketing
**Date:** {{ date }}
**Audit ID:** {{ audit_id }}

---

## 1. Executive Summary

{{ executive_summary | default("This Growth Infrastructure Audit provides a comprehensive analysis of " + (company or client_name) + "'s current digital marketing ecosystem. The audit covers 7 layers of marketing infrastructure and identifies specific opportunities for building predictable growth engines.") }}

**Overall Infrastructure Score:** {{ overall_score | default("--") }}/100

| Category | Score | Priority |
|----------|-------|----------|
| Website & Technical | {{ scores.website | default("--") }}/100 | {{ priorities.website | default("--") }} |
| SEO & Organic | {{ scores.seo | default("--") }}/100 | {{ priorities.seo | default("--") }} |
| Content Ecosystem | {{ scores.content | default("--") }}/100 | {{ priorities.content | default("--") }} |
| Social & Community | {{ scores.social | default("--") }}/100 | {{ priorities.social | default("--") }} |
| Paid Advertising | {{ scores.paid | default("--") }}/100 | {{ priorities.paid | default("--") }} |
| Local Visibility | {{ scores.local | default("--") }}/100 | {{ priorities.local | default("--") }} |
| Competitive Position | {{ scores.competitive | default("--") }}/100 | {{ priorities.competitive | default("--") }} |

---

## 2. Website & Technical Infrastructure

### 2.1 Site Performance
{{ website_performance | default("Analysis pending.") }}

### 2.2 Mobile Experience
{{ mobile_experience | default("Analysis pending.") }}

### 2.3 Technical SEO Foundation
{{ technical_seo | default("Analysis pending.") }}

### 2.4 Conversion Architecture
{{ conversion_architecture | default("Analysis pending.") }}

**Key Findings:**
{% for finding in website_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 3. SEO & Organic Visibility

### 3.1 Keyword Landscape
{{ keyword_landscape | default("Analysis pending.") }}

### 3.2 On-Page Optimization
{{ on_page_seo | default("Analysis pending.") }}

### 3.3 Backlink Profile
{{ backlink_profile | default("Analysis pending.") }}

### 3.4 Local SEO Status
{{ local_seo_status | default("Analysis pending.") }}

**Key Findings:**
{% for finding in seo_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 4. Content Ecosystem Assessment

### 4.1 Content Inventory
{{ content_inventory | default("Analysis pending.") }}

### 4.2 Content Quality & Relevance
{{ content_quality | default("Analysis pending.") }}

### 4.3 Content Gaps
{{ content_gaps | default("Analysis pending.") }}

### 4.4 Content Distribution
{{ content_distribution | default("Analysis pending.") }}

**Key Findings:**
{% for finding in content_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 5. Social Media & Community Presence

### 5.1 Platform Presence
{{ platform_presence | default("Analysis pending.") }}

### 5.2 Engagement Analysis
{{ engagement_analysis | default("Analysis pending.") }}

### 5.3 Community Building
{{ community_building | default("Analysis pending.") }}

**Key Findings:**
{% for finding in social_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 6. Paid Advertising Analysis

### 6.1 Current Ad Spend & Channels
{{ ad_spend_overview | default("Analysis pending.") }}

### 6.2 Campaign Performance
{{ campaign_performance | default("Analysis pending.") }}

### 6.3 Audience Targeting
{{ audience_targeting | default("Analysis pending.") }}

### 6.4 Funnel Efficiency
{{ funnel_efficiency | default("Analysis pending.") }}

**Key Findings:**
{% for finding in paid_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 7. Local Visibility & Google Business Profile

### 7.1 Google Business Profile Status
{{ gbp_status | default("Analysis pending.") }}

### 7.2 Review Management
{{ review_management | default("Analysis pending.") }}

### 7.3 Directory Listings
{{ directory_listings | default("Analysis pending.") }}

### 7.4 Local Pack Performance
{{ local_pack | default("Analysis pending.") }}

**Key Findings:**
{% for finding in local_findings | default([]) %}
- {{ finding }}
{% endfor %}

---

## 8. Competitive Landscape

### 8.1 Key Competitors Identified
{{ competitors_overview | default("Analysis pending.") }}

### 8.2 Competitive Positioning
{{ competitive_positioning | default("Analysis pending.") }}

### 8.3 Competitor Content & Strategy Analysis
{{ competitor_strategy | default("Analysis pending.") }}

### 8.4 Gaps & Opportunities vs. Competition
{{ competitive_gaps | default("Analysis pending.") }}

---

## 9. Growth Opportunities & Priority Matrix

### High Impact / Low Effort (Quick Wins)
{% for opp in quick_wins | default([]) %}
- **{{ opp.title }}**: {{ opp.description }} (Estimated impact: {{ opp.impact }})
{% endfor %}

### High Impact / High Effort (Strategic Investments)
{% for opp in strategic_investments | default([]) %}
- **{{ opp.title }}**: {{ opp.description }} (Estimated impact: {{ opp.impact }})
{% endfor %}

### Low Impact / Low Effort (Maintenance)
{% for opp in maintenance_items | default([]) %}
- **{{ opp.title }}**: {{ opp.description }}
{% endfor %}

---

## 10. Recommended Engine Configuration

Based on this audit, we recommend the following growth engine configuration for {{ company or client_name }}:

{% for engine in recommended_engines | default([]) %}
### {{ engine.name }}
- **Purpose:** {{ engine.purpose }}
- **Priority:** {{ engine.priority }}
- **Expected Timeline:** {{ engine.timeline }}
- **Key Deliverables:** {{ engine.deliverables }}
- **Expected Impact:** {{ engine.impact }}

{% endfor %}

### Investment Overview

| Engine | Monthly Investment | Expected ROI Timeline |
|--------|-------------------|----------------------|
{% for engine in recommended_engines | default([]) %}| {{ engine.name }} | {{ engine.price | default("TBD") }} | {{ engine.roi_timeline | default("TBD") }} |
{% endfor %}

---

## 11. Next Steps

1. **Schedule a strategy call** to review these findings in detail
2. **Select priority engines** based on budget and business goals
3. **Begin onboarding** with access setup and brand documentation
4. **Engine activation** within 5 business days of onboarding
5. **First results review** at the 30-day mark

---

*This audit was generated by Apex AI Marketing's Infrastructure Auditor system.*
*For questions, contact us at hello@apexaimarketing.pro*

**Book your strategy call:** [https://calendly.com/apex-ai-marketing](https://calendly.com/apex-ai-marketing)
"""


def render_audit_report(
    client_name: str,
    company: str = "",
    sections: dict = None,
    language: str = "en",
    **kwargs,
) -> str:
    """Render the audit report template with Jinja2.

    Args:
        client_name: Client contact name.
        company: Company name.
        sections: dict of section data to populate the template.
        language: Language code ('en' or 'ru').
        **kwargs: Additional template variables.

    Returns:
        Rendered markdown string.
    """
    from jinja2 import Template
    from datetime import date
    import uuid

    sections = sections or {}

    context = {
        "client_name": client_name,
        "company": company,
        "date": date.today().isoformat(),
        "audit_id": str(uuid.uuid4())[:8].upper(),
        "overall_score": sections.get("overall_score", "--"),
        "scores": sections.get("scores", {}),
        "priorities": sections.get("priorities", {}),
        # Section content
        "executive_summary": sections.get("executive_summary"),
        "website_performance": sections.get("website_performance"),
        "mobile_experience": sections.get("mobile_experience"),
        "technical_seo": sections.get("technical_seo"),
        "conversion_architecture": sections.get("conversion_architecture"),
        "website_findings": sections.get("website_findings", []),
        "keyword_landscape": sections.get("keyword_landscape"),
        "on_page_seo": sections.get("on_page_seo"),
        "backlink_profile": sections.get("backlink_profile"),
        "local_seo_status": sections.get("local_seo_status"),
        "seo_findings": sections.get("seo_findings", []),
        "content_inventory": sections.get("content_inventory"),
        "content_quality": sections.get("content_quality"),
        "content_gaps": sections.get("content_gaps"),
        "content_distribution": sections.get("content_distribution"),
        "content_findings": sections.get("content_findings", []),
        "platform_presence": sections.get("platform_presence"),
        "engagement_analysis": sections.get("engagement_analysis"),
        "community_building": sections.get("community_building"),
        "social_findings": sections.get("social_findings", []),
        "ad_spend_overview": sections.get("ad_spend_overview"),
        "campaign_performance": sections.get("campaign_performance"),
        "audience_targeting": sections.get("audience_targeting"),
        "funnel_efficiency": sections.get("funnel_efficiency"),
        "paid_findings": sections.get("paid_findings", []),
        "gbp_status": sections.get("gbp_status"),
        "review_management": sections.get("review_management"),
        "directory_listings": sections.get("directory_listings"),
        "local_pack": sections.get("local_pack"),
        "local_findings": sections.get("local_findings", []),
        "competitors_overview": sections.get("competitors_overview"),
        "competitive_positioning": sections.get("competitive_positioning"),
        "competitor_strategy": sections.get("competitor_strategy"),
        "competitive_gaps": sections.get("competitive_gaps"),
        "quick_wins": sections.get("quick_wins", []),
        "strategic_investments": sections.get("strategic_investments", []),
        "maintenance_items": sections.get("maintenance_items", []),
        "recommended_engines": sections.get("recommended_engines", []),
        **kwargs,
    }

    template = Template(AUDIT_TEMPLATE)
    return template.render(**context)
