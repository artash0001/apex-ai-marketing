"""
Apex AI Marketing - Monthly Report Template

Comprehensive monthly performance report with billing summary.
Delivered on the 1st of each month for the previous month.

Sections:
  1. Executive Summary & Month in Review
  2. KPI Performance vs. Targets
  3. Engine-by-Engine Performance
  4. Content & Deliverables Summary
  5. Experiment Results & Learnings
  6. ROI Analysis
  7. Competitive Landscape Update
  8. Next Month Strategy & Priorities
  9. Billing Summary
"""

MONTHLY_REPORT_TEMPLATE = """# Monthly Growth Report

**Client:** {{ client_name }}{% if company %} ({{ company }}){% endif %}
**Period:** {{ month_start }} to {{ month_end }}
**Report Date:** {{ report_date }}

---

## 1. Executive Summary

{{ executive_summary | default("Monthly performance review for " + (company or client_name) + ".") }}

### Month at a Glance

| Metric | This Month | Last Month | Change | Target |
|--------|-----------|------------|--------|--------|
{% for metric in monthly_summary | default([]) %}| {{ metric.name }} | {{ metric.current }} | {{ metric.previous }} | {{ metric.change }} | {{ metric.target | default("--") }} |
{% endfor %}

**Overall Health Score:** {{ health_score | default("--") }}/100

---

## 2. KPI Performance vs. Targets

| KPI | Monthly Target | Actual | Achievement | YTD Progress |
|-----|---------------|--------|-------------|--------------|
{% for kpi in kpis | default([]) %}| {{ kpi.name }} | {{ kpi.target }} | {{ kpi.actual }} | {{ kpi.achievement }} | {{ kpi.ytd | default("--") }} |
{% endfor %}

### Traffic Analysis
{{ traffic_analysis | default("Pending analytics integration.") }}

### Conversion Funnel
{{ conversion_funnel | default("Pending analytics integration.") }}

### Lead Quality Assessment
{{ lead_quality | default("Pending data collection.") }}

---

## 3. Engine-by-Engine Performance

{% for engine in engines | default([]) %}
### {{ engine.engine_name }}

**Status:** {{ engine.status | default("Active") }}
**Monthly Investment:** {{ engine.monthly_price | default("--") }}

{{ engine.summary | default("Performance details pending.") }}

**Key Metrics:**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
{% for m in engine.metrics | default([]) %}| {{ m.name }} | {{ m.target }} | {{ m.actual }} | {{ m.status }} |
{% endfor %}

**Deliverables Produced:** {{ engine.deliverables_count | default("--") }}
**Notable Achievements:** {{ engine.achievements | default("--") }}

---
{% endfor %}

## 4. Content & Deliverables Summary

### Deliverables Completed This Month

| # | Deliverable | Type | Engine | Quality Score |
|---|-------------|------|--------|--------------|
{% for d in deliverables | default([]) %}| {{ loop.index }} | {{ d.title }} | {{ d.type }} | {{ d.engine | default("--") }} | {{ d.quality_score | default("--") }}/10 |
{% endfor %}

**Total deliverables:** {{ total_deliverables | default("--") }}
**Average quality score:** {{ avg_quality_score | default("--") }}/10

### Content Performance
{{ content_performance | default("Content performance tracking pending integration.") }}

---

## 5. Experiment Results & Learnings

### Experiments Completed This Month

{% for exp in completed_experiments | default([]) %}
#### {{ exp.hypothesis | truncate(120) }}
- **Variable Changed:** {{ exp.variable }}
- **Primary Metric:** {{ exp.metric }}
- **Result:** {{ exp.result }}
- **Decision:** {{ exp.decision }}
- **Learning:** {{ exp.learning }}
{% endfor %}

### Cumulative Learnings
{{ cumulative_learnings | default("Learnings database building as experiments conclude.") }}

### Experiments in Progress
{% for exp in active_experiments | default([]) %}
- {{ exp.hypothesis | truncate(100) }} ({{ exp.days_remaining }} days remaining)
{% endfor %}

---

## 6. ROI Analysis

### Investment vs. Return

| Category | Investment | Measurable Return | ROI |
|----------|-----------|-------------------|-----|
{% for row in roi_table | default([]) %}| {{ row.category }} | {{ row.investment }} | {{ row.return_value }} | {{ row.roi }} |
{% endfor %}

### Cost per Acquisition Trends
{{ cpa_trends | default("CPA tracking will begin once conversion data flows in.") }}

### Lifetime Value Indicators
{{ ltv_indicators | default("LTV tracking pending sufficient data collection.") }}

---

## 7. Competitive Landscape Update

{{ competitive_summary | default("Monthly competitive analysis pending.") }}

### Market Position Changes
{% for change in market_changes | default([]) %}
- {{ change }}
{% endfor %}

### Competitor Activity Highlights
{% for activity in competitor_activities | default([]) %}
- **{{ activity.competitor }}:** {{ activity.action }}
{% endfor %}

---

## 8. Next Month Strategy & Priorities

### Strategic Priorities
{% for priority in next_month_priorities | default([]) %}
{{ loop.index }}. **{{ priority.title }}**: {{ priority.description }}
{% endfor %}

### Planned Experiments
{% for exp in planned_experiments | default([]) %}
- {{ exp.hypothesis | truncate(100) }}
{% endfor %}

### Key Milestones
{% for milestone in next_milestones | default([]) %}
- {{ milestone.date }}: {{ milestone.description }}
{% endfor %}

### Recommendations
{{ recommendations | default("Strategic recommendations will be developed based on this month's data.") }}

---

## 9. Billing Summary

### Invoice for {{ month_name | default("the period") }}

| Engine | Monthly Rate |
|--------|-------------|
{% for engine in engines | default([]) %}| {{ engine.engine_name }} | {{ engine.monthly_price | default("--") }} |
{% endfor %}
| **Total** | **{{ total_billing | default("--") }}** |

**Payment terms:** Due within 14 days of invoice date
**Currency:** {{ currency | default("USD") }}

---

*Report generated by Apex AI Marketing's Reporting Engine.*
*Schedule a review call: [https://calendly.com/apex-ai-marketing](https://calendly.com/apex-ai-marketing)*
"""


def render_monthly_report(
    client_name: str,
    company: str = "",
    month_start: str = "",
    month_end: str = "",
    engagements: list = None,
    metrics: dict = None,
    language: str = "en",
    **kwargs,
) -> str:
    """Render the monthly report template.

    Args:
        client_name: Client contact name.
        company: Company name.
        month_start: Start date of the reporting month.
        month_end: End date of the reporting month.
        engagements: List of engine engagement dicts.
        metrics: Metrics data gathered for the period.
        language: Language code.
        **kwargs: Additional template variables.

    Returns:
        Rendered markdown string.
    """
    from jinja2 import Template
    from datetime import date, datetime

    engagements = engagements or []
    metrics = metrics or {}

    # Calculate total billing
    total_billing = sum(
        float(e.get("monthly_price", 0)) for e in engagements
    )

    # Parse month name
    month_name = ""
    if month_start:
        try:
            month_name = datetime.fromisoformat(month_start).strftime("%B %Y")
        except (ValueError, TypeError):
            month_name = month_start

    context = {
        "client_name": client_name,
        "company": company,
        "month_start": month_start,
        "month_end": month_end,
        "report_date": date.today().isoformat(),
        "month_name": month_name,
        # Engines
        "engines": engagements,
        "total_billing": f"${total_billing:,.2f}" if total_billing else "--",
        "currency": "USD",
        # Summary metrics
        "executive_summary": metrics.get("executive_summary"),
        "monthly_summary": metrics.get("monthly_summary", []),
        "health_score": metrics.get("health_score"),
        # KPIs
        "kpis": metrics.get("kpis", []),
        "traffic_analysis": metrics.get("traffic_analysis"),
        "conversion_funnel": metrics.get("conversion_funnel"),
        "lead_quality": metrics.get("lead_quality"),
        # Deliverables
        "deliverables": metrics.get("deliverables", []),
        "total_deliverables": metrics.get("deliverables_produced", "--"),
        "avg_quality_score": metrics.get("avg_quality_score"),
        "content_performance": metrics.get("content_performance"),
        # Experiments
        "completed_experiments": metrics.get("completed_experiments", []),
        "active_experiments": metrics.get("active_experiments", []),
        "cumulative_learnings": metrics.get("cumulative_learnings"),
        # ROI
        "roi_table": metrics.get("roi_table", []),
        "cpa_trends": metrics.get("cpa_trends"),
        "ltv_indicators": metrics.get("ltv_indicators"),
        # Competitive
        "competitive_summary": metrics.get("competitive_summary"),
        "market_changes": metrics.get("market_changes", []),
        "competitor_activities": metrics.get("competitor_activities", []),
        # Next month
        "next_month_priorities": metrics.get("next_month_priorities", []),
        "planned_experiments": metrics.get("planned_experiments", []),
        "next_milestones": metrics.get("next_milestones", []),
        "recommendations": metrics.get("recommendations"),
        **kwargs,
    }

    template = Template(MONTHLY_REPORT_TEMPLATE)
    return template.render(**context)
