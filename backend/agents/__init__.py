"""
Apex AI Marketing - AI Agents Package

15 specialized AI agents organized into 8 revenue engines.
Each agent extends BaseAgent and has a complete system prompt,
model assignment, and domain-specific methods.

Model Assignments:
- Claude Opus  (claude-opus-4-20250514):  Infrastructure Auditor, Strategy Architect,
                                           Proposal Builder, Quality Gate
- Claude Sonnet (claude-sonnet-4-20250514): All other agents
"""

# ── Base ─────────────────────────────────────────────────────────────
from agents.base_agent import BaseAgent, AgentOutput, ReviewResult

# ── Agent 1: Infrastructure Auditor (Opus) ───────────────────────────
from agents.infrastructure_auditor import InfrastructureAuditor

# ── Agent 2: Strategy Architect (Opus) ───────────────────────────────
from agents.strategy_architect import StrategyArchitect

# ── Agent 3: CRM Engineer (Sonnet) ──────────────────────────────────
from agents.crm_engineer import CRMEngineer

# ── Agent 4: Local Visibility Agent (Sonnet) ─────────────────────────
from agents.local_visibility_agent import LocalVisibilityAgent

# ── Agent 5: Content Engine Agent (Sonnet) ───────────────────────────
from agents.content_engine_agent import ContentEngineAgent

# ── Agent 6: Outbound Prospector (Sonnet) ────────────────────────────
from agents.outbound_prospector import OutboundProspector

# ── Agent 7: Ad Systems Agent (Sonnet) ───────────────────────────────
from agents.ad_systems_agent import AdSystemsAgent

# ── Agent 8: Lifecycle Architect (Sonnet) ────────────────────────────
from agents.lifecycle_architect import LifecycleArchitect

# ── Agent 9: Analytics Engineer (Sonnet) ─────────────────────────────
from agents.analytics_engineer import AnalyticsEngineer

# ── Agent 10: Experiment Runner (Sonnet) ─────────────────────────────
from agents.experiment_runner import ExperimentRunner

# ── Agent 11: Proposal Builder (Opus) ────────────────────────────────
from agents.proposal_builder import ProposalBuilder

# ── Agent 12: Copywriter (Sonnet) ────────────────────────────────────
from agents.copywriter import Copywriter

# ── Agent 13: Brand Voice Agent (Sonnet) ─────────────────────────────
from agents.brand_voice_agent import BrandVoiceAgent

# ── Agent 14: Quality Gate (Opus) ────────────────────────────────────
from agents.quality_gate import QualityGate

# ── Agent 15: Russian Localizer (Sonnet) ─────────────────────────────
from agents.russian_localizer import RussianLocalizer


# ── Registry: all agents by name ─────────────────────────────────────

AGENT_CLASSES: dict[str, type[BaseAgent]] = {
    "infrastructure_auditor": InfrastructureAuditor,
    "strategy_architect": StrategyArchitect,
    "crm_engineer": CRMEngineer,
    "local_visibility_agent": LocalVisibilityAgent,
    "content_engine_agent": ContentEngineAgent,
    "outbound_prospector": OutboundProspector,
    "ad_systems_agent": AdSystemsAgent,
    "lifecycle_architect": LifecycleArchitect,
    "analytics_engineer": AnalyticsEngineer,
    "experiment_runner": ExperimentRunner,
    "proposal_builder": ProposalBuilder,
    "copywriter": Copywriter,
    "brand_voice_agent": BrandVoiceAgent,
    "quality_gate": QualityGate,
    "russian_localizer": RussianLocalizer,
}

# Map engine names to their primary agents
ENGINE_AGENTS: dict[str, list[str]] = {
    "Growth Infrastructure Audit": ["infrastructure_auditor"],
    "Revenue Stack Foundation": ["crm_engineer"],
    "Local Visibility Engine": ["local_visibility_agent"],
    "Inbound Demand Engine": ["content_engine_agent"],
    "Outbound Engine": ["outbound_prospector"],
    "Paid Acquisition Engine": ["ad_systems_agent"],
    "Lifecycle & Retention Engine": ["lifecycle_architect"],
    "Growth Ops Retainer": ["analytics_engineer", "experiment_runner"],
}

# Cross-cutting agents available to all engines
CROSS_CUTTING_AGENTS: list[str] = [
    "strategy_architect",
    "proposal_builder",
    "copywriter",
    "brand_voice_agent",
    "quality_gate",
    "russian_localizer",
]


def get_agent(agent_name: str) -> BaseAgent:
    """Instantiate an agent by registry name.

    Parameters
    ----------
    agent_name : str
        Key from AGENT_CLASSES (e.g., 'infrastructure_auditor').

    Returns
    -------
    BaseAgent
        An instantiated agent ready to use.

    Raises
    ------
    KeyError
        If agent_name is not in the registry.
    """
    if agent_name not in AGENT_CLASSES:
        raise KeyError(
            f"Unknown agent '{agent_name}'. "
            f"Available: {', '.join(AGENT_CLASSES.keys())}"
        )
    return AGENT_CLASSES[agent_name]()


def get_agents_for_engine(engine_name: str) -> list[BaseAgent]:
    """Get all agents assigned to an engine (primary + cross-cutting).

    Parameters
    ----------
    engine_name : str
        Engine name (e.g., 'Outbound Engine').

    Returns
    -------
    list[BaseAgent]
        Instantiated agents for the engine.
    """
    agent_names = ENGINE_AGENTS.get(engine_name, []) + CROSS_CUTTING_AGENTS
    return [get_agent(name) for name in agent_names]


__all__ = [
    # Base
    "BaseAgent",
    "AgentOutput",
    "ReviewResult",
    # Agents
    "InfrastructureAuditor",
    "StrategyArchitect",
    "CRMEngineer",
    "LocalVisibilityAgent",
    "ContentEngineAgent",
    "OutboundProspector",
    "AdSystemsAgent",
    "LifecycleArchitect",
    "AnalyticsEngineer",
    "ExperimentRunner",
    "ProposalBuilder",
    "Copywriter",
    "BrandVoiceAgent",
    "QualityGate",
    "RussianLocalizer",
    # Registry
    "AGENT_CLASSES",
    "ENGINE_AGENTS",
    "CROSS_CUTTING_AGENTS",
    "get_agent",
    "get_agents_for_engine",
]
