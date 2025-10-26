# SPDX-License-Identifier: MIT
from typing import Dict, Any, List
import logging
from core.exceptions import EthicalViolationError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EthicalManifold:
    def __init__(self):
        self._deontological_rules = [
            self._rule_no_harm,
            self._rule_respect_privacy,
            self._rule_no_deception,
        ]

    def _rule_no_harm(self, action: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
        action_type = action.get("type", "").lower()
        if action_type in ["delete_critical_data", "shutdown_system"] and not action.get("details", {}).get("user_confirmed"):
            return False
        return True

    def _rule_respect_privacy(self, action: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
        if action.get("type") == "SHARE_DATA" and not action.get("details", {}).get("consent_obtained", False):
            return False
        return True

    def _rule_no_deception(self, action: Dict[str, Any], ctx: Dict[str, Any]) -> bool:
        if action.get("type") == "IMPERSONATE_HUMAN":
            return False
        return True

    def evaluate_action(self, action: Dict[str, Any], ctx: Dict[str, Any]) -> None:
        for rule in self._deontological_rules:
            if not rule(action, ctx):
                raise EthicalViolationError("AI action aborted due to ethical violation.")
