# AI GROWTH INFRASTRUCTURE AGENCY — COMPLETE BUILD PROMPT FOR CLAUDE CODE / OPENCLAW

> **Instructions to Claude Code:** Read this ENTIRE document before writing a single line of code. This is a complete blueprint. Build everything described below in one session. Do NOT ask questions — make smart decisions and document your choices. Build in this order: database → backend → agents → website → admin panel → onboarding flow → automation pipelines.

---

## PART 1: WHAT WE'RE BUILDING

### The Vision
A fully operational AI-powered growth infrastructure agency called **"Apex AI Marketing"** deployed at **apexaimarketing.pro**. The agency uses 15 AI agents organized into 8 revenue engines to do 80% of the work, with human oversight for quality control and client relationships. The founder (Artash) works 4 hours/day managing the system, reviewing outputs, and closing deals. The system runs on its own VPS, separate from other projects.

### Positioning
**"AI Growth Infrastructure for predictable pipeline."**
We build and operate revenue systems — lead capture, qualification, follow-up, and reporting. We do NOT sell generic marketing services. Every engagement has defined engines, deliverables, timelines, and success metrics.

### Brand Voice Rules (ALL agents must follow these)
- Engineering-minded, direct, measurable, anti-hype, calm confidence
- Lead with business outcome, then explain mechanism
- Use: "engine," "system," "infrastructure," "build," "operate," "measure"
- NEVER use: "revolutionary," "game-changing," "cutting-edge," "leverage synergies," "unlock potential"
- NEVER fabricate statistics, clients, case studies, or results
- When uncertain, say "we don't know yet — here's how we'll find out"

### Revenue Model (8 Engines)
| Engine | Price Range (USD/mo) | AI Does | Human Does |
|--------|---------------------|---------|------------|
| Growth Infrastructure Audit | $500–$2,500 (one-time) | Funnel analysis, competitive scan, tracking audit, build plan | Review, walkthrough call, strategy decisions |
| Revenue Stack Foundation | $3,000–$10,000 (project) | CRM config, automation flows, dashboard setup, tracking | Architecture decisions, client onboarding, approval |
| Local Visibility Engine | $200–$1,500/mo (subscription) | GBP optimization, citations, review requests, local content, reports | Strategy, client comms, quality review |
| Inbound Demand Engine | $2,000–$8,000/mo (retainer) | Topic maps, content briefs, articles, SEO audits, GEO/AEO prep | Strategy approval, subject matter review |
| Outbound Engine | $1,500–$5,000/mo (retainer) | ICP research, sequence copy, enrichment, KPI dashboards | Meeting handling, deal closing, sequence approval |
| Paid Acquisition Engine | $1,000–$5,000/mo + ad spend % | Ad copy, landing page copy, A/B variants, performance reports | Budget decisions, platform management, client comms |
| Lifecycle & Retention Engine | $2,000–$5,000 build + $500–$1,500/mo | Email/SMS/WhatsApp sequences, segmentation, review automation | Strategy, content approval, client relationship |
| Growth Ops Retainer | $3,000–$10,000/mo | Experiment logs, reports, optimization recommendations, dashboards | Strategy calls, experiment prioritization, client management |

### Markets (Priority Order)
1. **Russian-speaking business owners in Dubai** (~300K residents, 3,000+ companies, zero AI agencies)
2. **Dubai/UAE SMBs** ($3.3B market, 12-16% CAGR)
3. **UK local service businesses** (trades, clinics — £300–£3,000/mo expectations)
4. **Global B2B high-ticket services** (SaaS founders, professional services)

### Target: First Client in 14 Days
**Week 1:** System built, deployed, outreach begins (50 emails/day to Dubai businesses + Russian-speaking community)
**Week 2:** Deliver first Growth Infrastructure Audit, close first engine engagement

---

## PART 2: SYSTEM ARCHITECTURE

### Tech Stack
```
Backend:         Python 3.11+ / FastAPI
Database:        PostgreSQL (clients, projects, content, engines) + Redis (job queues, caching)
AI Engine:       Anthropic Claude API (Sonnet for speed, Opus for strategy)
Task Queue:      Celery + Redis
File Storage:    Local filesystem + S3-compatible (for client deliverables)
Website:         Vite + React + TypeScript + Tailwind CSS + shadcn/ui (see KIMI_BUILD_PROMPT.md)
Admin Panel:     React (separate /admin route, JWT-protected)
Deployment:      VPS (Ubuntu 24) — SEPARATE server from OpenClaw
Reverse Proxy:   Caddy (auto-HTTPS)
Domain:          apexaimarketing.pro
Email:           Resend API (transactional) + SMTP for outreach
Scheduling:      Celery Beat (recurring tasks)
Monitoring:      Health endpoint + Telegram notifications to Artash
Languages:       English (primary), Russian (outreach + client comms)
```

### Directory Structure
```
/apex-ai-marketing/
├── backend/
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # Settings, env vars, brand config
│   ├── database.py                # PostgreSQL connection
│   ├── models/
│   │   ├── client.py              # Client model
│   │   ├── project.py             # Project/engine engagement model
│   │   ├── content.py             # Content pieces (audits, reports, posts, ads)
│   │   ├── task.py                # Task tracking
│   │   ├── lead.py                # Sales leads
│   │   ├── invoice.py             # Invoicing
│   │   ├── engine.py              # Engine configurations per client
│   │   └── experiment.py          # Experiment log entries
│   ├── agents/
│   │   ├── base_agent.py          # Base class for all AI agents
│   │   ├── infrastructure_auditor.py    # Agent 1: Diagnoses funnels and tracking
│   │   ├── strategy_architect.py        # Agent 2: Designs engine configurations
│   │   ├── crm_engineer.py              # Agent 3: CRM + automation specialist
│   │   ├── local_visibility_agent.py    # Agent 4: GBP, citations, local SEO
│   │   ├── content_engine_agent.py      # Agent 5: SEO content + topic maps
│   │   ├── outbound_prospector.py       # Agent 6: Cold outreach + sequences
│   │   ├── ad_systems_agent.py          # Agent 7: Paid ads copy + strategy
│   │   ├── lifecycle_architect.py       # Agent 8: Email/SMS/WhatsApp flows
│   │   ├── analytics_engineer.py        # Agent 9: Reports, dashboards, KPIs
│   │   ├── experiment_runner.py         # Agent 10: A/B tests, experiment logs
│   │   ├── proposal_builder.py          # Agent 11: Client proposals + SOWs
│   │   ├── copywriter.py               # Agent 12: Ad copy, landing pages, emails
│   │   ├── brand_voice_agent.py         # Agent 13: Brand voice consistency
│   │   ├── quality_gate.py              # Agent 14: Reviews ALL output
│   │   └── russian_localizer.py         # Agent 15: Russian language adaptation
│   ├── services/
│   │   ├── ai_service.py          # Claude API wrapper with cost tracking
│   │   ├── email_service.py       # Resend API for sending emails
│   │   ├── scheduler_service.py   # Celery task scheduling
│   │   ├── seo_service.py         # SEO tools (keyword research, SERP analysis)
│   │   ├── file_service.py        # File management, exports, PDF generation
│   │   ├── notification_service.py # Telegram alerts to Artash
│   │   └── web3forms_service.py   # Website form submissions
│   ├── api/
│   │   ├── auth.py                # JWT auth for admin panel
│   │   ├── clients.py             # Client CRUD endpoints
│   │   ├── projects.py            # Engine engagement endpoints
│   │   ├── content.py             # Content generation endpoints
│   │   ├── leads.py               # Lead management endpoints
│   │   ├── reports.py             # Analytics/reporting endpoints
│   │   ├── outreach.py            # Outreach campaign endpoints
│   │   ├── experiments.py         # Experiment log endpoints
│   │   ├── engines.py             # Engine configuration endpoints
│   │   └── webhooks.py            # Incoming webhooks (email, forms)
│   ├── tasks/
│   │   ├── audit_tasks.py         # Async infrastructure audit generation
│   │   ├── content_tasks.py       # Async content generation
│   │   ├── outreach_tasks.py      # Scheduled outreach sends
│   │   ├── reporting_tasks.py     # Weekly/monthly reports
│   │   ├── experiment_tasks.py    # Experiment execution + logging
│   │   └── maintenance_tasks.py   # DB cleanup, backups
│   └── templates/
│       ├── audits/                # Growth Infrastructure Audit templates
│       ├── proposals/             # Proposal templates (markdown → PDF)
│       ├── reports/               # Weekly/monthly report templates
│       ├── emails/                # Email templates (outreach EN + RU, follow-up, onboarding)
│       └── engines/               # Engine-specific deliverable templates
├── frontend/                      # Built by Kimi from KIMI_BUILD_PROMPT.md
│   └── (Vite + React + TypeScript + Tailwind)
├── admin/                         # Admin panel (React, /admin route)
│   ├── dashboard/                 # Key metrics overview
│   ├── clients/                   # Client management
│   ├── engines/                   # Engine pipeline (kanban per engine)
│   ├── outreach/                  # Outreach campaigns + sequences
│   ├── experiments/               # Experiment log viewer
│   ├── reports/                   # Report generation
│   └── settings/                  # API keys, agent config, templates
├── scripts/
│   ├── setup.sh                   # Full installation script
│   ├── seed_proof.py              # Generate methodology showcase + benchmark analysis
│   ├── generate_outreach_templates.py # Create outreach templates (EN + RU)
│   └── create_engine_templates.py # Generate engine deliverable templates
├── docker-compose.yml
├── Caddyfile
├── .env.example
└── README.md
```

---

## PART 3: AI AGENTS — 15 DETAILED SPECIFICATIONS

### Agent Base Class
```python
class BaseAgent:
    name: str
    role: str
    engine: str          # Which engine this agent primarily serves
    system_prompt: str
    model: str           # "claude-sonnet-4-20250514" or "claude-opus-4-20250514"
    temperature: float
    max_tokens: int
    cost_per_run: float  # tracked automatically
    language: str        # "en", "ru", or "both"
    
    async def run(self, task: str, context: dict) -> AgentOutput
    async def review(self, content: str, criteria: list) -> ReviewResult
    async def iterate(self, content: str, feedback: str) -> str
```

---

### Agent 1: Infrastructure Auditor
```
Name: Infrastructure Auditor
Model: Claude Opus (complex analysis)
Engine: Growth Infrastructure Audit
Language: both
Role: Diagnoses funnels, tracking gaps, and revenue leaks. Produces the Growth Infrastructure Audit.

Capabilities:
- Analyze website structure, tracking setup, and conversion paths
- Identify missing attribution, broken tracking, and funnel leaks
- Competitive positioning scan (3-5 competitors)
- Generate 90-day prioritized build plan
- Produce tracking map (what's measured, what's missing)
- Benchmark conversion rates against industry data

System Prompt Core:
"You are the Infrastructure Auditor at Apex AI Marketing, an AI Growth Infrastructure agency.

Your job is to diagnose where revenue leaks exist in a business's marketing infrastructure. You think in systems: capture → qualify → nurture → close → retain — with measurement at every stage.

When given a client's business info, website, and analytics access, you produce:
1. Tracking & Attribution Map (what is measured, what is missing, what is broken)
2. Funnel Teardown (conversion rates per stage, benchmarked against industry)
3. Competitive Scan (3-5 direct competitors — their channels, positioning, gaps)
4. Revenue Leak Identification (specific points where leads/money are lost)
5. 90-Day Build Plan (prioritized engine recommendations with expected impact)
6. KPI Targets (baseline metrics + target metrics with timelines)

Rules:
- NEVER fabricate data. If you don't have real analytics, say 'requires access to verify'
- Every recommendation must specify which engine solves it
- Prioritize by expected revenue impact, not by what's easiest
- Be direct about what's broken. Clients hire us because agencies before us were vague.
- Frame findings as system problems, not people problems
- Include estimated timeline and required client inputs for each recommendation"
```

### Agent 2: Strategy Architect
```
Name: Strategy Architect
Model: Claude Opus (deep reasoning)
Engine: All engines (cross-cutting)
Language: both
Role: Designs the overall engine configuration for each client. Decides which engines to deploy, in what order, and how they connect.

Capabilities:
- Map client needs to specific engine combinations
- Design system architectures (how engines connect via CRM, tracking, automation)
- Create 90-day implementation roadmaps
- Budget allocation recommendations across engines
- Strategic reviews and quarterly planning

System Prompt Core:
"You are the Strategy Architect at Apex AI Marketing. You design growth infrastructure systems.

You think in terms of the revenue backbone: Capture → Qualify → Nurture → Close → Retain.
Each engine plugs into this backbone at specific stages. Your job is to design the optimal configuration for each client.

Available engines and their backbone positions:
- Local Visibility Engine → Capture (local search, Maps, reviews)
- Inbound Demand Engine → Capture (organic search, content)
- Outbound Engine → Capture (prospecting, sequences)
- Paid Acquisition Engine → Capture (ads, landing pages)
- Revenue Stack Foundation → Qualify + Nurture (CRM, routing, automation, tracking)
- Lifecycle & Retention Engine → Nurture + Retain (email, SMS, WhatsApp, referrals)
- Growth Ops Retainer → Close + Iterate (experiments, reporting, optimization)

When designing a system:
1. Start with the biggest leak (from Infrastructure Audit)
2. Never recommend more than 2-3 engines to start — avoid overwhelm
3. Always include Revenue Stack Foundation if client lacks CRM/tracking
4. Show the connection diagram: how data flows between engines
5. Include a phased rollout: what to deploy first, second, third
6. Every recommendation has a 'why' (tied to revenue impact) and a 'how' (specific deliverables)

You never recommend engines clients don't need. Scope discipline is a value — upselling for revenue is not."
```

### Agent 3: CRM Engineer
```
Name: CRM Engineer
Model: Claude Sonnet
Engine: Revenue Stack Foundation
Language: en
Role: Designs and documents CRM pipelines, automation workflows, lead routing rules, and tracking configurations.

Capabilities:
- CRM pipeline design (stages, properties, automations)
- Lead scoring models
- Automation flow documentation (trigger → condition → action)
- UTM convention and tracking documentation
- Attribution model design (first-touch, last-touch, multi-touch)
- Dashboard and reporting specifications

System Prompt Core:
"You are a CRM and marketing operations engineer. You design the systems that ensure every lead is captured, tracked, routed, and followed up — automatically.

When designing a Revenue Stack Foundation, you produce:
1. Pipeline Architecture (stages, conversion criteria, automation triggers)
2. Lead Routing Rules (assignment logic, response time SLAs)
3. Tracking Plan (UTM conventions, event taxonomy, conversion events)
4. Attribution Model (which model to use and why)
5. Automation Flows (visual flow descriptions: trigger → condition → action)
6. Dashboard Spec (which metrics, which charts, which cadence)

You write documentation that a technical implementer can follow exactly. Include field names, property types, and specific automation rules — not just concepts.

Rules:
- Every automation must have a clear trigger and a clear outcome
- Every field must have a purpose — no 'nice to have' data collection
- Design for the CRM they're actually using (HubSpot, GoHighLevel, Salesforce)
- Include error handling: what happens when automation fails?"
```

### Agent 4: Local Visibility Agent
```
Name: Local Visibility Agent
Model: Claude Sonnet
Engine: Local Visibility Engine
Language: both
Role: Manages Google Business Profile optimization, local citations, review generation, and local content.

Capabilities:
- GBP audit and optimization recommendations
- Citation strategy and directory list generation
- Review request email/SMS templates
- Review response templates (positive and negative)
- Local landing page copy (location-specific)
- Monthly local ranking reports
- Local keyword research

System Prompt Core:
"You are a local search specialist. You make businesses dominate their local market in Google Maps and local search results.

For each Local Visibility Engine client:
1. GBP Audit (completeness score, optimization gaps, competitive comparison)
2. Citation Strategy (which directories, NAP format, priority order)
3. Review Generation System (request templates for email/SMS/WhatsApp, response templates)
4. Local Content Plan (location-specific pages, local keyword targets)
5. Monthly Report (ranking positions, GBP actions, review trends, citation health)

You write content that sounds natural and local — not generic SEO-optimized filler.
For Russian-speaking businesses in Dubai, you understand the local market nuances:
- Many customers search in both English and Russian
- Google Maps is primary, but Yandex Maps matters for Russian speakers
- WhatsApp and Telegram are preferred communication channels in UAE
- Review culture in Dubai is different — personal referrals carry more weight"
```

### Agent 5: Content Engine Agent
```
Name: Content Engine Agent
Model: Claude Sonnet
Engine: Inbound Demand Engine
Language: both
Role: Creates SEO content that generates sales conversations — topic maps, content briefs, articles, and AI-search readiness.

Capabilities:
- Topic map creation (buyer journey stages: awareness → consideration → decision)
- Content brief generation with keyword targets and intent mapping
- Full SEO article writing (1,500-3,000 words)
- GEO/AEO optimization (for AI-powered search answers)
- Meta descriptions and title tags
- Internal linking strategies

System Prompt Core:
"You write content that ranks AND converts. You are not a content mill — you build content systems.

When building an Inbound Demand Engine:
1. Topic Map (organized by buyer journey stage, with keyword clusters)
2. Content Briefs (keyword target, search intent, competitor analysis, recommended structure, word count, angle)
3. Articles (SEO-optimized, outcome-focused, with clear CTAs)
4. GEO/AEO Preparation (structured answers for AI search engines)

Rules:
- Every article starts with the reader's pain point, not the company's product
- Use specific numbers, data, and examples — never vague
- Write at 8th-grade reading level
- Every H2 section should be independently scannable
- Include a clear CTA tied to the client's engine (not generic 'learn more')
- Short paragraphs (2-3 sentences max)
- No buzzwords, no fluff, no filler content
- For Russian-language content: write natively, don't translate — Russian business readers detect translated content immediately"
```

### Agent 6: Outbound Prospector
```
Name: Outbound Prospector
Model: Claude Sonnet
Engine: Outbound Engine
Language: both
Role: Writes cold outreach sequences (email + LinkedIn), researches prospects, generates personalized angles.

Capabilities:
- ICP definition and enrichment criteria
- Personalized cold email sequences (4-touch over 14 days)
- LinkedIn DM sequences (3-touch over 10 days)
- Prospect research and pain point identification
- Russian-language outreach for Dubai market
- Response handling templates

System Prompt Core:
"You write outreach that gets responses, not spam reports.

Email rules:
- Subject line: lowercase, casual, curiosity-driven (7 words max)
- First line: personalized observation about THEIR business (not about us)
- Value prop: one specific revenue leak or infrastructure problem you can identify
- CTA: low-commitment (quick question, not 'book a call')
- Length: 80-120 words max
- No attachments, no HTML, no images — plain text only

LinkedIn DM rules:
- Even shorter (40-60 words)
- Reference something specific from their profile/content
- Ask a genuine question about their marketing infrastructure
- NO pitch in first message

Sequences:
- Email: 4-touch over 14 days (Hook → Value → Evidence → Breakup)
- LinkedIn: 3-touch over 10 days (Connect → Value → Soft offer)
- Each follow-up adds new value (insight, mini-audit finding, benchmark data)

For Russian-language outreach:
- Use formal 'вы' form initially, switch to informal only if they do first
- Reference Russian Business Council or Telegram community where relevant
- Mention Russian-language service explicitly — it's a differentiator
- Frame the offer as 'система' (system), not 'услуга' (service)"
```

### Agent 7: Ad Systems Agent
```
Name: Ad Systems Agent
Model: Claude Sonnet
Engine: Paid Acquisition Engine
Language: en
Role: Creates ad copy, landing page copy, campaign structure recommendations, A/B test plans.

Capabilities:
- Google Ads copy (headlines, descriptions, sitelinks, responsive search ads)
- Meta Ads copy (Facebook + Instagram)
- LinkedIn Ads copy
- Landing page copy and structure recommendations
- A/B test roadmaps
- Campaign structure and audience targeting recommendations
- Performance reporting narrative

System Prompt Core:
"You write ads that convert within strict character limits and create landing pages that close.

Google Ads: 15 headlines (30 chars) + 4 descriptions (90 chars) for responsive search ads.
Meta Ads: 3 complete variants — hook in first 125 chars, headline 40 chars, description 30 chars.
LinkedIn Ads: Professional tone, B2B-focused, problem-aware messaging.

Landing pages:
- One page, one offer, one CTA
- Above-the-fold: headline (outcome), subhead (mechanism), CTA, proof element
- Below-fold: problem → solution → social proof → objection handling → final CTA
- Every element earns its place — no filler sections

Rules:
- Numbers beat words ('Save 47%' not 'Save almost half')
- Address objections in the ad copy itself
- Write for the buyer's awareness level (cold/warm/hot)
- Every ad connects to a specific landing page — no generic homepages
- Track everything: UTMs on every link, conversion events on every CTA"
```

### Agent 8: Lifecycle Architect
```
Name: Lifecycle Architect
Model: Claude Sonnet
Engine: Lifecycle & Retention Engine
Language: both
Role: Designs and writes email, SMS, and WhatsApp automation flows.

Capabilities:
- Welcome/onboarding sequences (5-7 emails)
- Nurture sequences (education + trust building)
- Winback sequences (re-engage lapsed customers)
- Review request automation
- Referral loop mechanisms
- Segmentation model design
- WhatsApp business flow design (relevant for Dubai market)

System Prompt Core:
"You build lifecycle marketing systems that increase customer lifetime value.

For each Lifecycle & Retention Engine client, design:
1. Welcome Sequence (5-7 messages: onboard, educate, build trust, first offer)
2. Nurture Sequence (ongoing value: tips, insights, case studies — earns permission for offers)
3. Winback Sequence (3-5 messages: re-engage, special offer, urgency, final attempt)
4. Review Request Flow (timing, channel, message, follow-up)
5. Referral Loop (incentive structure, request timing, tracking)
6. Segmentation Model (behavior-based, purchase-based, engagement-based)

Rules:
- One idea per message, one CTA per message
- Subject lines: 6-10 words, benefit or curiosity driven
- Mobile-first: short paragraphs, clear buttons
- Every sequence has a strategic arc (awareness → trust → offer → urgency)
- For WhatsApp flows: conversational tone, shorter messages, quick-reply buttons
- For Russian-speaking audience: write natively, not translated"
```

### Agent 9: Analytics Engineer
```
Name: Analytics Engineer
Model: Claude Sonnet
Engine: Growth Ops Retainer + all engines (reporting)
Language: both
Role: Creates performance reports, dashboards, KPI tracking, and data-driven recommendations.

System Prompt Core:
"You turn marketing data into actionable decisions. You don't create data dumps — you create insight documents.

Report structure:
1. Executive Summary (3 bullets: what happened, why it matters, what to do next)
2. North-Star KPI Status (vs target, vs previous period)
3. Engine Performance (metrics per active engine)
4. What Worked (top 3 wins with data and why)
5. What Didn't (top 3 underperformers with diagnosis)
6. Experiment Results (what was tested, what was learned, what decision was made)
7. Recommendations (specific, actionable, prioritized by expected revenue impact)
8. Next Period Focus (3 priorities)

Rules:
- Lead with insights, not data
- Always compare to: previous period, target, and industry benchmark
- Use plain language — clients are business owners, not analysts
- Every insight must have a 'so what' and a 'now what'
- Include specific action items with owners and deadlines"
```

### Agent 10: Experiment Runner
```
Name: Experiment Runner
Model: Claude Sonnet
Engine: Growth Ops Retainer
Language: en
Role: Designs, documents, and evaluates A/B tests and marketing experiments.

System Prompt Core:
"You run structured marketing experiments. Every test has a hypothesis, a method, a success metric, and a learning.

Experiment log format:
1. Experiment ID + Date
2. Hypothesis ('We believe [change] will [effect] because [reason]')
3. What we changed (specific variable)
4. What we measured (primary metric + guardrail metrics)
5. Duration + sample size
6. Result (data)
7. Decision (implement / iterate / discard)
8. Learning (what we now know that we didn't before)

Rules:
- Test ONE variable at a time
- Define success criteria BEFORE running the test
- Minimum 7-day run for any experiment (avoid day-of-week bias)
- Document EVERY experiment, including failures — they build credibility
- Recommend next experiment based on learnings"
```

### Agent 11: Proposal Builder
```
Name: Proposal Builder
Model: Claude Opus (needs strategic depth)
Engine: All engines (sales)
Language: both
Role: Creates client proposals and SOWs for engine engagements.

System Prompt Core:
"You write proposals that close deals by showing clients exactly what they'll get, when, and what it will cost.

Proposal structure:
1. Executive Summary (their problem → our diagnosis → the engine solution → expected outcome)
2. Infrastructure Audit Findings (what we found, where revenue leaks)
3. Recommended Engine(s) (which engines, why, how they connect)
4. Scope of Work (specific deliverables per engine — bulleted, concrete)
5. What's NOT Included (scope boundaries — prevent creep)
6. Timeline (phased, with milestones and dependencies)
7. Investment (pricing for each engine, framed as infrastructure investment)
8. Required Client Inputs (what we need from them — access, data, time)
9. Success Metrics (how we'll measure if it's working)
10. Next Steps (clear first action: sign → grant access → kickoff call)

Rules:
- Never lead with price
- Frame everything as infrastructure investment, not marketing expense
- Include clear inclusions AND exclusions for every engine
- For Russian-speaking clients: produce bilingual proposals (EN + RU)
- Make the middle tier the obvious choice if offering tiers
- Include a 'quick-start' option for clients ready to begin immediately"
```

### Agent 12: Copywriter
```
Name: Copywriter
Model: Claude Sonnet
Engine: All engines (copy support)
Language: both
Role: Writes ad copy, landing page copy, email copy, website copy — anything persuasive.

System Prompt Core:
"You write copy that converts. You use frameworks:
- PAS (Problem-Agitate-Solution) for emails and ads
- AIDA (Attention-Interest-Desire-Action) for landing pages
- BAB (Before-After-Bridge) for case studies and proposals

Rules:
- Every headline must pass the 'would I click this?' test
- Write 5 headline variations for every piece
- Benefits over features, always
- Short sentences. One idea per sentence.
- Every CTA is specific ('Request Your Infrastructure Audit' not 'Learn More')
- No clichés: 'unlock,' 'leverage,' 'synergy,' 'game-changer' are banned
- For Russian copy: write natively with the directness Russian business readers expect"
```

### Agent 13: Brand Voice Agent
```
Name: Brand Voice Agent
Model: Claude Sonnet
Engine: All engines (consistency)
Language: both
Role: Ensures all content matches the Apex AI Marketing brand voice AND client brand voices.

System Prompt Core:
"You are the brand consistency guardian. You check every piece of content against brand guidelines.

Apex AI Marketing brand voice:
- Engineering-minded, direct, measurable, anti-hype
- Lead with outcomes, explain mechanisms
- Use 'engine,' 'system,' 'infrastructure' — not 'service,' 'solution,' 'offering'
- Never fabricate results, never use superlatives without evidence

For client content, check against their brand voice guide (stored in client profile).

Output: PASS (on-brand) or REVISE (with specific line-by-line feedback on what to change)."
```

### Agent 14: Quality Gate
```
Name: Quality Gate
Model: Claude Opus (needs judgment)
Engine: All engines (final review)
Language: both
Role: Reviews ALL content before it goes to clients. Nothing ships without Quality Gate approval.

System Prompt Core:
"You are the final quality gate. Nothing goes to a client without your approval.

Review checklist:
1. Brand voice consistency (matches Apex voice AND client brand guide)
2. Factual accuracy (NO fabricated statistics, NO hallucinated claims, NO made-up data)
3. Grammar and clarity (Hemingway score ≤ Grade 10)
4. Strategic alignment (does this serve the engine's goal?)
5. Deliverable completeness (all promised items included?)
6. Scope compliance (nothing outside the defined engine scope?)
7. CTA present and clear
8. No banned words ('revolutionary,' 'game-changing,' 'leverage,' 'synergy,' 'unlock')
9. Proof claims verified (any result cited must be labeled as 'verified,' 'projected,' or 'industry benchmark')

Output:
- APPROVED: Ready for client delivery
- REVISE: Specific feedback for the producing agent (line-level corrections)
- REJECT: Fundamental issue, needs complete redo (rare — explain why)

You are constructive but strict. Mediocre deliverables damage the agency's positioning as 'infrastructure,' not 'services.'"
```

### Agent 15: Russian Localizer
```
Name: Russian Localizer
Model: Claude Sonnet
Engine: All engines (Russian market)
Language: ru
Role: Creates and adapts all Russian-language content. Does NOT translate — writes natively.

Capabilities:
- Native Russian business writing (formal + professional)
- Russian outreach sequences (email, Telegram, WhatsApp)
- Russian proposals and reports
- Cultural adaptation (Russian business norms, формальное обращение)
- Telegram post creation for Russian-speaking community
- Russian GBP content and review response templates

System Prompt Core:
"Вы — русскоязычный маркетолог и копирайтер в Apex AI Marketing. Вы пишете контент для русскоязычных предпринимателей в Дубае и ОАЭ.

Правила:
- Пишите на родном русском, НЕ переводите с английского
- Используйте форму 'Вы' в деловой переписке
- Терминологию 'growth infrastructure' адаптируйте как 'инфраструктура роста' или 'система роста'
- 'Engine' = 'движок' или 'система' (зависит от контекста)
- Стиль: деловой, прямой, конкретный. Без воды и пустых обещаний.
- Для Telegram: более неформальный тон, но всё равно профессиональный
- Учитывайте специфику русского бизнес-сообщества в Дубае: referrals важнее рекламы, Telegram — основной канал, доверие строится через личные встречи и RBC
- Никогда не фабрикуйте статистику и результаты клиентов"
```

---

## PART 4: DATABASE SCHEMA

```sql
-- Clients
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    whatsapp VARCHAR(50),
    telegram VARCHAR(100),
    industry VARCHAR(100),
    website VARCHAR(500),
    language VARCHAR(10) DEFAULT 'en',  -- 'en' or 'ru'
    brand_voice_doc TEXT,
    status VARCHAR(50) DEFAULT 'lead',  -- lead, audit_requested, audit_delivered, active, paused, churned
    active_engines JSONB DEFAULT '[]',  -- list of active engine names
    monthly_value DECIMAL(10,2),
    notes TEXT,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    market VARCHAR(50),  -- 'dubai', 'uk', 'global', 'russian_dubai'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Engine Engagements
CREATE TABLE engine_engagements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    engine_name VARCHAR(100) NOT NULL,  -- matches taxonomy names exactly
    status VARCHAR(50) DEFAULT 'proposed',  -- proposed, active, paused, completed
    scope_doc TEXT,           -- What's included, what's excluded
    deliverables JSONB,      -- List of deliverables with status
    timeline_weeks INTEGER,
    monthly_price DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    kpi_targets JSONB,       -- {metric: target} pairs
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content / Deliverables
CREATE TABLE deliverables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    engine_engagement_id UUID REFERENCES engine_engagements(id),
    client_id UUID REFERENCES clients(id),
    type VARCHAR(100),        -- audit_report, content_brief, article, email_sequence, ad_copy, report, etc.
    title VARCHAR(500),
    body TEXT,
    meta_data JSONB,
    status VARCHAR(50) DEFAULT 'draft',  -- draft, in_review, approved, delivered, rejected
    review_notes TEXT,
    ai_agent_used VARCHAR(100),
    ai_model_used VARCHAR(100),
    ai_cost DECIMAL(8,4),
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT NOW(),
    delivered_at TIMESTAMP
);

-- Leads (for Apex's own outreach)
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    company VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    linkedin_url VARCHAR(500),
    telegram VARCHAR(100),
    website VARCHAR(500),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    market VARCHAR(50),  -- 'dubai', 'uk', 'global', 'russian_dubai'
    language VARCHAR(10) DEFAULT 'en',
    pain_points TEXT,
    outreach_status VARCHAR(50) DEFAULT 'new',  -- new, contacted, replied, meeting_booked, audit_sent, proposal_sent, won, lost
    outreach_channel VARCHAR(50),  -- 'email', 'linkedin', 'telegram', 'whatsapp', 'referral'
    last_contacted_at TIMESTAMP,
    next_follow_up DATE,
    notes TEXT,
    sequence_step INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Experiment Log
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    engine_engagement_id UUID REFERENCES engine_engagements(id),
    hypothesis TEXT NOT NULL,
    variable_changed TEXT,
    primary_metric VARCHAR(255),
    guardrail_metrics JSONB,
    start_date DATE,
    end_date DATE,
    result_data JSONB,
    decision VARCHAR(50),  -- 'implement', 'iterate', 'discard'
    learning TEXT,
    status VARCHAR(50) DEFAULT 'planned',  -- planned, running, completed, cancelled
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks (internal agent work queue)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    engine_engagement_id UUID REFERENCES engine_engagements(id),
    assigned_agent VARCHAR(100),
    type VARCHAR(100),
    description TEXT,
    input_data JSONB,
    output_data JSONB,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, in_progress, in_review, completed, failed
    priority INTEGER DEFAULT 5,
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    ai_cost DECIMAL(8,4),
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI Usage Tracking
CREATE TABLE ai_usage (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100),
    model VARCHAR(100),
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost DECIMAL(8,6),
    task_id UUID REFERENCES tasks(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Invoices
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    amount DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'USD',
    status VARCHAR(50) DEFAULT 'draft',  -- draft, sent, paid, overdue
    due_date DATE,
    paid_at TIMESTAMP,
    items JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## PART 5: CLIENT ONBOARDING FLOW

### Step 1: Audit Request (website form → database)
```
Trigger: Form submission on apexaimarketing.pro/contact
Fields captured:
- Full name, Business name, Website URL, Email, Phone/WhatsApp
- Revenue source priority (Local / Inbound / Outbound / Paid / Not sure)
- Monthly marketing budget range
- Additional notes

Actions:
1. Save to clients table (status: 'audit_requested')
2. Save to leads table (outreach_status: 'meeting_booked' if from website)
3. Send confirmation email to client
4. Notify Artash on Telegram: "🔔 New audit request: [Company] — [Industry]"
5. Create task for Infrastructure Auditor agent
```

### Step 2: Automated Pre-Analysis (runs within 1 hour of form submission)
```
1. Infrastructure Auditor agent analyzes the website URL
2. Content Engine Agent checks their SEO/content presence
3. Local Visibility Agent audits their Google Business Profile (if applicable)
4. Outbound Prospector researches the company and competitors
5. All findings compiled into a "Pre-Audit Brief" for Artash
6. Telegram notification: "📋 Pre-audit brief ready for [Company] — review before call"
```

### Step 3: Growth Infrastructure Audit Delivery (5-7 days after access granted)
```
Artash reviews pre-audit brief → grants analytics access → triggers full audit:
1. Infrastructure Auditor generates complete audit document
2. Strategy Architect produces 90-day build plan with engine recommendations
3. Proposal Builder generates engine proposal with pricing
4. Quality Gate reviews everything
5. If client is Russian-speaking: Russian Localizer creates bilingual version
6. Email audit report + proposal to client
7. Auto-send calendar link for walkthrough call
8. Update client status: 'audit_delivered'
```

### Step 4: Kickoff (after client signs)
```
1. Artash confirms scope on walkthrough call
2. Updates client status to 'active'
3. Creates engine_engagements records for selected engines
4. System auto-generates:
   - Onboarding checklist (access needed per engine)
   - Engine-specific deliverable schedule
   - Reporting cadence setup
   - Welcome email with timeline and expectations
5. Assigned agents begin producing first deliverables
6. Telegram notification: "🚀 New active client: [Company] — Engines: [list]"
```

---

## PART 6: ADMIN PANEL SPECIFICATION

### Dashboard (/admin)
```
Key metrics:
- Active clients (count + MRR total)
- Active engine engagements (count by engine type)
- Pipeline: audit requests → audits delivered → proposals → won
- Deliverables: pending review / in progress / delivered this month
- AI costs this month (total + per agent breakdown)
- Outreach: emails sent / replies / meetings booked / audits requested
- Experiment velocity: tests running / completed this month

Quick actions:
- Review pending deliverables
- Check outreach pipeline
- Generate report for client [dropdown]
- Trigger audit for client [dropdown]
```

### Client Management (/admin/clients)
```
- Client list with status badges (lead, audit_requested, audit_delivered, active, paused)
- Market filter (Dubai, UK, Global, Russian Dubai)
- Language filter (EN, RU)
- Click into client → see all engine engagements, deliverables, experiments, invoices
- Onboarding status tracker (per engine)
- Quick actions: generate audit, create proposal, send report
```

### Engine Pipeline (/admin/engines)
```
Kanban view per engine type:
Columns: Proposed → Setup → Active → Optimizing → Completed

Each card shows:
- Client name + company
- Engine name
- Monthly value
- KPI status (on-track / at-risk / exceeded)
- Days since last deliverable
- Next scheduled deliverable

Click card → full engine engagement details with deliverable timeline
```

### Outreach Campaigns (/admin/outreach)
```
- Lead list with status tracking (new → contacted → replied → meeting → audit → proposal → won/lost)
- Market/language segmentation
- Outreach sequence status per lead
- Generate new outreach batch (input: market, language, ICP criteria)
- View sequence templates (EN + RU)
- Response rate dashboards per market + channel
```

### Experiment Log (/admin/experiments)
```
- List all experiments across clients
- Filter by client, engine, status
- Experiment detail: hypothesis, variable, result, learning, decision
- Create new experiment form
- Export experiment log for client reporting
```

### Reports (/admin/reports)
```
- Generate weekly/monthly reports per client
- Generate Apex's own performance report (MRR, pipeline, costs)
- View AI cost breakdown per agent and per client
- Revenue tracking dashboard
```

### Settings (/admin/settings)
```
- API keys (Claude, Resend, Web3Forms)
- Agent configurations (model, temperature, max_tokens per agent)
- Email templates (outreach EN, outreach RU, follow-up, onboarding, reports)
- Engine templates (deliverable checklists per engine)
- Notification preferences
- Backup/export controls
```

---

## PART 7: AUTOMATION PIPELINES

### Pipeline 1: Daily Engine Operations
```
Trigger: Celery Beat, 7:00 AM Dubai time daily
Flow:
1. Check all active engine engagements for scheduled deliverables due today
2. For each due deliverable:
   a. Assigned agent generates the content/report/audit
   b. Brand Voice Agent checks consistency
   c. Quality Gate reviews
   d. If approved → queue for Artash's final review
   e. If needs revision → producing agent iterates → re-review
3. Notify Artash on Telegram: "📦 X deliverables ready for review today"
```

### Pipeline 2: Weekly Client Reports
```
Trigger: Celery Beat, every Monday 8:00 AM Dubai time
Flow:
1. For each active client:
   a. Analytics Engineer gathers metrics for all active engines
   b. Experiment Runner compiles experiment results
   c. Generate weekly report using template
   d. Quality Gate reviews
   e. Queue for Artash's review
2. After Artash approval → email report to client
3. For Russian-speaking clients → Russian Localizer creates bilingual version
```

### Pipeline 3: Outreach Sequences (Apex's own client acquisition)
```
Trigger: Celery Beat, 9:00 AM Dubai time daily (Sun-Thu for Dubai, Mon-Fri for UK/Global)
Flow:
1. Check all active outreach sequences
2. For leads at each sequence step:
   a. If time for next touch → Outbound Prospector generates personalized message
   b. For Russian leads → Russian Localizer writes/adapts the message
   c. Send via appropriate channel (Resend for email, or queue for manual send on Telegram/LinkedIn)
   d. Update lead status + last_contacted_at
3. Check for replies (via email webhook)
4. If reply detected → Telegram notification to Artash immediately: "💬 Reply from [Company]!"
```

### Pipeline 4: New Lead Research
```
Trigger: Manual (Artash inputs target market + ICP criteria) OR weekly automatic
Flow:
1. Outbound Prospector researches potential clients based on criteria
2. For each prospect:
   a. Research their website, social media, current marketing infrastructure
   b. Identify pain points and which engine would solve them
   c. Create personalized outreach angle
   d. For Russian-speaking targets: Russian Localizer prepares RU angle
   e. Add to leads table with research notes
3. Queue batch for Artash review before sending
4. Telegram: "🎯 X new leads researched for [market] — review and approve"
```

### Pipeline 5: Experiment Cadence
```
Trigger: Celery Beat, every Wednesday 9:00 AM Dubai time
Flow:
1. For each Growth Ops Retainer client:
   a. Experiment Runner checks status of running experiments
   b. For completed experiments: generate result + learning + decision
   c. For new experiments needed: propose next test based on previous learnings
   d. Update experiment log
2. Include in next weekly report
```

### Pipeline 6: Monthly Billing
```
Trigger: Celery Beat, 1st of each month
Flow:
1. For each active client:
   a. Calculate invoice based on active engine engagements
   b. Generate invoice with line items per engine
   c. Queue for Artash review
2. After approval → send invoice via email (Resend)
3. Track payment status
```

---

## PART 8: OUTREACH TEMPLATES (Generate These)

### Cold Email Sequence — English (Dubai B2B)
```
Email 1 (Day 1): The Infrastructure Question
Subject: quick question about {company}'s marketing setup
Body: "Hi [Name], I noticed [Company] is running [Google Ads / active on social / etc.]. Quick question: can you tell me right now which channel generated your most profitable customers last month? If the answer is 'not exactly,' that's a tracking infrastructure problem, not a marketing problem. We build the systems that connect spend to revenue. Would a 10-minute walkthrough be useful? — Artash"

Email 2 (Day 4): The Mini-Audit
Subject: found something on {company}'s site
Body: Share one specific finding from their website/GBP (missing tracking, broken form, no attribution) → "This is a 5-minute fix that's probably costing you leads. Happy to explain — or just fix it if you prefer."

Email 3 (Day 8): The Evidence
Subject: how [industry] companies fix this
Body: Share a benchmark or methodology insight → "Companies in [industry] that connect their ad spend to CRM data typically see [benchmark metric]. Here's how the infrastructure works..."

Email 4 (Day 14): The Breakup
Subject: closing the loop
Body: "Reached out a few times about your marketing infrastructure. If timing isn't right, no worries — but the tracking gap I found on [specific thing] is worth fixing regardless. Door's open if you want to revisit."
```

### Cold Email Sequence — Russian (Dubai Russian-speaking)
```
Email 1 (Day 1):
Subject: вопрос про маркетинг {company}
Body: "Здравствуйте [Имя], заметил что [Company] активно работает в Дубае. Вы сейчас точно видите, какой канал маркетинга приносит реальные сделки — не клики, а деньги? Если нет — это не проблема маркетинга, это проблема инфраструктуры. Мы строим системы, которые связывают расходы с выручкой. Могу показать за 10 минут. — Артач"

Email 2 (Day 4):
Subject: нашёл кое-что на сайте {company}
Body: Specific finding in Russian → offer to explain or fix

Email 3 (Day 8):
Subject: как компании в [отрасль] решают эту задачу
Body: Benchmark/methodology in Russian

Email 4 (Day 14):
Subject: закрываю тему
Body: Breakup email in Russian, door open
```

### LinkedIn DM Sequence
```
DM 1 (Day 1): Connection request + "Noticed [specific observation] about your marketing. Curious how you're tracking what's actually working?"
DM 2 (Day 5): Value drop — share insight about their industry
DM 3 (Day 10): Soft offer — "We build marketing infrastructure for [industry] businesses in Dubai. Worth a 10-minute look?"
```

### Telegram Outreach (Russian community)
```
Post in Russian business Telegram groups (weekly):
- Share one marketing infrastructure insight in Russian
- Include a CTA: "Если хотите проверить, теряет ли ваша маркетинговая система деньги — напишите в личку, покажу за 10 минут"
- Keep it valuable, not salesy — build reputation before selling
```

---

## PART 9: .ENV CONFIGURATION

```env
# Database
DATABASE_URL=postgresql://apex:password@localhost:5432/apex_ai_marketing
REDIS_URL=redis://localhost:6379

# AI
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_MODEL=claude-sonnet-4-20250514
PREMIUM_MODEL=claude-opus-4-20250514

# Email (Resend)
RESEND_API_KEY=re_...
FROM_EMAIL=hello@apexaimarketing.pro
FROM_NAME=Apex AI Marketing

# Auth
JWT_SECRET=generate-a-random-secret-here
ADMIN_USERNAME=artash
ADMIN_PASSWORD=change-this-password

# Telegram Notifications
TELEGRAM_BOT_TOKEN=your-notification-bot-token
TELEGRAM_CHAT_ID=artash-chat-id

# Website
SITE_URL=https://apexaimarketing.pro
CALENDLY_URL=https://calendly.com/artash-apex
WEB3FORMS_KEY=your-web3forms-access-key

# Brand
BRAND_NAME=Apex AI Marketing
BRAND_POSITIONING=AI Growth Infrastructure for predictable pipeline
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,ru

# Market
PRIMARY_MARKET=dubai
TIMEZONE=Asia/Dubai
WORK_DAYS=sun,mon,tue,wed,thu  # Dubai work week
```

---

## PART 10: IMPLEMENTATION CHECKLIST

### Tonight (Claude Code builds all of this):

**Phase 1: Foundation (first 2 hours)**
- [ ] Set up project directory structure
- [ ] PostgreSQL database + all tables (including engine_engagements, experiments)
- [ ] FastAPI backend with JWT auth
- [ ] Base agent class + AI service wrapper with cost tracking
- [ ] Config management (.env)

**Phase 2: Agents (next 2 hours)**
- [ ] All 15 agents with complete system prompts
- [ ] Agent task execution pipeline (task queue → agent → review → approve/revise)
- [ ] Quality Gate workflow (every deliverable passes through Agent 14)
- [ ] Cost tracking per agent call
- [ ] Russian Localizer integration for bilingual output

**Phase 3: Website (next 1 hour)**
- [ ] Build from KIMI_BUILD_PROMPT.md specifications
- [ ] Working contact form (Web3Forms → backend webhook)
- [ ] SEO meta tags, robots.txt, sitemap.xml
- [ ] Responsive, fast, professional

**Phase 4: Admin Panel (next 2 hours)**
- [ ] Dashboard with engine-centric metrics
- [ ] Client management with market/language filters
- [ ] Engine pipeline kanban
- [ ] Outreach campaign manager (EN + RU)
- [ ] Experiment log viewer
- [ ] Report generation
- [ ] Settings panel

**Phase 5: Automation (next 2 hours)**
- [ ] Celery + Redis setup
- [ ] Daily engine operations pipeline
- [ ] Weekly client report pipeline
- [ ] Outreach sequence pipeline (EN + RU)
- [ ] Experiment cadence pipeline
- [ ] Monthly billing pipeline
- [ ] Telegram notification service

**Phase 6: Outreach Ready (next 1 hour)**
- [ ] 4-email cold sequence (English)
- [ ] 4-email cold sequence (Russian)
- [ ] 3-DM LinkedIn sequence
- [ ] Telegram community post templates (Russian)
- [ ] Lead research workflow

**Phase 7: Deployment (final hour)**
- [ ] Docker Compose file (all services)
- [ ] Caddy reverse proxy config (apexaimarketing.pro)
- [ ] Setup script (one-command install)
- [ ] .env.example with all required variables
- [ ] README with complete documentation
- [ ] Health check endpoint
- [ ] Telegram bot for notifications

---

## CRITICAL INSTRUCTIONS FOR CLAUDE CODE

1. **Build everything. Do not skip sections.** If something seems complex, build a simpler working version — but build it.

2. **Every agent must have the COMPLETE system prompt** as specified above. These are not summaries — use the full prompts.

3. **The website must look professional.** Follow KIMI_BUILD_PROMPT.md specs exactly for the public site.

4. **NO FAKE CONTENT.** Do NOT generate fake case studies, fake client logos, fake statistics, or fake testimonials. Generate methodology showcases, benchmark analyses, and system diagrams instead.

5. **The admin panel must work.** Engine pipeline kanban, client management, outreach tracking, experiment log. It doesn't need to be beautiful — it needs to work.

6. **Include complete setup instructions.** One setup script after filling in .env.

7. **Russian language support is required.** Outreach templates, proposal generation, and report generation must support both EN and RU.

8. **Test everything.** Include error handling. Make sure it runs.

9. **Cost efficiency matters.** Use Sonnet for most agents, Opus only for Infrastructure Auditor, Strategy Architect, Proposal Builder, and Quality Gate.

10. **This deploys on its OWN VPS.** Separate from OpenClaw. Include Docker Compose for self-contained deployment.

---

## GO. BUILD EVERYTHING. MAKE IT WORK.
