# APEX AI Marketing

AI-powered growth infrastructure agency deployed at apexaimarketing.pro

## Quick Start for Claude Code

```bash
# 1. Connect to VPS
ssh root@72.62.64.166
# Password: K0msom9l/643

# 2. Existing code locations:
# - Website: /opt/apex-new/
# - Backend: /opt/apex-digital/backend/
# - Telegram bot: /opt/apex-digital/backend/main.py

# 3. Read BUILD_PROMPT.md for full specification
# 4. Build the complete system per Phase 1-7
```

## Project Structure

```
apex-ai-marketing/
├── BUILD_PROMPT.md          # Full system specification (READ THIS FIRST)
├── backend/                 # FastAPI + AI agents
├── frontend/                # React website
├── admin/                   # Admin panel
├── scripts/                 # Setup and deployment
└── README.md               # This file
```

## VPS Details

- **IP**: 72.62.64.166
- **Domain**: apexaimarketing.pro (SSL configured)
- **Email**: artaches@apexaimarketing.pro
- **Telegram Bot**: @LifeOsApex_bot

## Database

- PostgreSQL: apex_ai_marketing
- Redis: localhost:6379

## Build Phases

See BUILD_PROMPT.md for complete Phase 1-7 checklist.

## Notes

- Keep existing website design from /opt/apex-new/
- Preserve working Telegram bot integration
- Use Claude Sonnet for most agents, Opus for strategy/complex tasks
- Support both English and Russian languages
