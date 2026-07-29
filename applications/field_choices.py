"""Resource requirement choices, taken from the TOSCA profile.

A requirement constrains a capability property of a capacity - 'host.num-cpus'
and the like. Those names come from the profile, so the database stores them as
plain text and cannot say what is valid. SAT Builder resolves the profile, so it
is asked instead, and the answers become dropdowns.
"""
import logging
import os
from typing import Any, Dict, List, Tuple

import requests
from django.core.cache import cache

from editor.field_choices import register_field_choices
from postgrest.api_configs.base_config import build_api_url
from postgrest.table_names import TableNames

logger = logging.getLogger(__name__)

TARGETS_PATH = "application/node-filter/targets"
CACHE_KEY = "application_node_filter_targets"
# The profile changes rarely and a stale dropdown is worse than a slow one only
# briefly, so this is short enough to pick a profile change up within a page or
# two of navigation.
CACHE_SECONDS = 300

# How each operator reads to someone who has never seen TOSCA.
OPERATOR_LABELS = {
    "$greater_or_equal": "at least",
    "$greater_than": "more than",
    "$less_or_equal": "at most",
    "$less_than": "less than",
    "$in_range": "between (inclusive)",
    "$equal": "exactly",
    "$has_any_entry": "includes any of",
}


def fetch_targets() -> List[Dict[str, Any]]:
    """Every capability property a requirement may constrain."""
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    response = requests.get(
        build_api_url(
            os.environ.get("SAT_BUILDER_API_URL"),
            TARGETS_PATH,
            env_var_name="SAT_BUILDER_API_URL",
        ),
        timeout=10,
    )
    response.raise_for_status()
    targets = response.json().get("targets") or []
    cache.set(CACHE_KEY, targets, CACHE_SECONDS)
    return targets


def target_choices() -> List[Tuple[str, str]]:
    """Capability properties, labelled so the capability is obvious."""
    return [
        (target["target"], _target_label(target))
        for target in fetch_targets()
    ]


def operator_choices() -> List[Tuple[str, str]]:
    """Every operator any target accepts.

    Which ones apply to the chosen target is narrowed in the browser, from the
    same data; this is the full set so the field is valid whatever is picked.
    """
    seen: Dict[str, str] = {}
    for target in fetch_targets():
        for operator in target.get("operators") or []:
            seen.setdefault(operator, OPERATOR_LABELS.get(operator, operator))
    return sorted(seen.items(), key=lambda pair: pair[1])


def operators_by_target() -> Dict[str, List[str]]:
    """Which operators each target accepts, for narrowing the choice."""
    return {t["target"]: t.get("operators") or [] for t in fetch_targets()}


def _target_label(target: Dict[str, Any]) -> str:
    capability = target.get("capability", "").replace("_", " ")
    prop = target.get("property", "").replace("-", " ").replace("_", " ")
    return f"{capability.title()}: {prop}"


def register() -> None:
    """Wire the requirement columns up to the profile's answers."""
    register_field_choices(TableNames.APPLICATION_NODE_FILTER, "target", target_choices)
    register_field_choices(TableNames.APPLICATION_NODE_FILTER, "operator", operator_choices)
