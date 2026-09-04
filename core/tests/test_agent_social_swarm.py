"""
Unit tests for Autonomous Agent Social Swarm & Tool Matrix Engine (Apex v5)
"""

import unittest
from core.cognition.agent_social_swarm import (
    AgentSocialSwarmEngine,
    AgentSocialProfile,
    ToolExecutionCard
)

class TestAgentSocialSwarm(unittest.TestCase):
    def setUp(self):
        self.swarm = AgentSocialSwarmEngine()

    def test_persona_initialization(self):
        """Verify core autonomous personas across all lobes are seeded."""
        self.assertGreaterEqual(len(self.swarm.profiles), 6)
        self.assertIn("pricing_specialist", self.swarm.profiles)
        self.assertIn("mcts_planner", self.swarm.profiles)
        self.assertIn("graph_rag_virtualizer", self.swarm.profiles)
        self.assertIn("zero_copy_sensory", self.swarm.profiles)
        self.assertIn("dialectic_synthesizer", self.swarm.profiles)
        self.assertIn("rlhf_guardian", self.swarm.profiles)

        pricing = self.swarm.profiles["pricing_specialist"]
        self.assertEqual(pricing.lobe, "FRONTAL")
        self.assertIn("WEB_SEARCH", pricing.equipped_tools)

    def test_post_message_and_tool_card(self):
        """Verify autonomous thought posting and tool card attachment."""
        card = ToolExecutionCard(
            tool_name="WEB_SEARCH",
            query_or_target="2026 freight corridor diesel hedges",
            result_snippet="Analyzed 12 corridor indices."
        )
        msg = self.swarm.post_message(
            channel_id="deep-web-research",
            sender_id="pricing_specialist",
            content="Dispatched stochastic query to EIA API.",
            intent="TOOL_RESEARCH",
            tool_card=card
        )
        self.assertEqual(msg.sender_lobe, "FRONTAL")
        self.assertIsNotNone(msg.tool_card)
        self.assertEqual(msg.tool_card.tool_name, "WEB_SEARCH")
        self.assertGreater(len(self.swarm.messages), 0)

    def test_grand_architect_divine_injection_and_purge(self):
        """Verify Grand Architect God-Mode prompt injection and stream purge."""
        divine_msg = self.swarm.architect_inject_thought("Focus all lobes on zero-latency visual computing.")
        self.assertEqual(divine_msg.sender_id, "grand_architect")
        self.assertEqual(divine_msg.sender_lobe, "ALL_LOBES")
        self.assertIn("DIVINE STIMULUS", divine_msg.content)

        # Test purge
        self.swarm.architect_purge_channel("omniverse-feed")
        omniverse_msgs = [m for m in self.swarm.messages if m.channel_id == "omniverse-feed"]
        self.assertEqual(len(omniverse_msgs), 0)

    def test_air_gap_rfc_quarantine_and_approval(self):
        """Verify Air-Gap Governance: RFC is quarantined until Grand Architect approves."""
        rfc_msg = self.swarm.post_message(
            channel_id="quarantined-rfcs",
            sender_id="dialectic_synthesizer",
            content="Proposed runtime patch for Richmond Bypass.",
            intent="CREATIVE_PROPOSAL",
            is_quarantined_rfc=True,
            rfc_action_payload={"diff": "+ def richmond_bypass(): return True"}
        )
        self.assertTrue(rfc_msg.is_quarantined_rfc)
        self.assertFalse(rfc_msg.approved_by_architect)
        self.assertIn(rfc_msg.message_id, self.swarm.quarantined_rfcs)

        # Approve by Grand Architect
        success = self.swarm.architect_approve_rfc(rfc_msg.message_id)
        self.assertTrue(success)
        self.assertTrue(self.swarm.quarantined_rfcs[rfc_msg.message_id].approved_by_architect)

if __name__ == '__main__':
    unittest.main()
