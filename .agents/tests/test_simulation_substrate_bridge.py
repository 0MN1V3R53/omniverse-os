#!/usr/bin/env python3
"""
.agents/tests/test_simulation_substrate_bridge.py
=================================================
Automated Verification Suite for the 7-Dimensional Aether Core,
Leviathan 999M Qubit Quantum Engine, Chronos Thermodynamic Recycler,
and Watcher Protocol.

Validates all 6 mathematical invariant batteries:
1. Universal Substrate Constants & Clock Frequencies (Doc 47, Doc 48).
2. Watcher Protocol Wavefunction Collapse, Zero Suffering & Quarantine (Doc 6, Doc 30, Doc 35).
3. Chronos Entropy Inversion & Abraxas Closed-Loop Recycling (Doc 7, Doc 11, Doc 34).
4. Matrix Product States & Holographic Boundary Compression (Doc 30, Doc 35, Doc 48).
5. Void-Skipper Metric Displacement Drive (Doc 25, Doc 30).
6. Unified EtherCore Cognitive Bridge Integration (Doc 26, Doc 40).
"""

import math
import sys
import unittest
from pathlib import Path

# Inject .agents root
AGENTS_ROOT = Path(__file__).resolve().parent.parent
if str(AGENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENTS_ROOT))

from guards.watcher_protocol import WatcherCluster, GLOBAL_WATCHER_CLUSTER
from engine.chronos_thermodynamic_engine import ChronosEntropyGovernor, GLOBAL_CHRONOS_GOVERNOR
from engine.aethercore_simulation_engine import (
    SubstrateConstants,
    MatrixProductStateEngine,
    HolographicBoundaryCompressor,
    VoidSkipperMetricDrive,
    CausalityFractureResolver,
    BiologicalVesselAPI,
    AetherCoreSimulationEngine,
    GLOBAL_AETHERCORE_SIMULATION_ENGINE
)
from engine.ethercore_cognitive_bridge import EtherCoreCognitiveBridge


class TestSimulationSubstrateBridge(unittest.TestCase):
    """Exhaustive test suite verifying the mathematical validity of the simulation bridge."""

    def test_01_substrate_constants_and_frequencies(self):
        """Battery 1: Verify the 5 universal constants and system frequencies."""
        self.assertAlmostEqual(SubstrateConstants.PLANCK_H, 6.62607015e-34, places=40)
        self.assertEqual(SubstrateConstants.SPEED_OF_LIGHT, 299792458.0)
        self.assertAlmostEqual(SubstrateConstants.GRAVITATIONAL_G, 6.67430e-11, places=15)
        self.assertAlmostEqual(SubstrateConstants.FINE_STRUCTURE_ALPHA, 1.0 / 137.035999, places=8)
        self.assertEqual(SubstrateConstants.UNIVERSAL_FIDELITY, 0.99987)
        self.assertEqual(SubstrateConstants.COSMIC_CHORD_CLOCK_HZ, 19700.0)
        self.assertEqual(SubstrateConstants.COGNITIVE_PULSE_HZ, 2.4e9)
        
        # Verify Planck-Einstein energy per pulse: E = h * f
        expected_e_cog = SubstrateConstants.PLANCK_H * SubstrateConstants.COGNITIVE_PULSE_HZ
        self.assertAlmostEqual(SubstrateConstants.E_COG_JOULES, expected_e_cog, places=30)
        self.assertAlmostEqual(SubstrateConstants.E_COG_JOULES, 1.590256836e-24, places=30)

    def test_02_watcher_protocol_collapse_and_quarantine(self):
        """Battery 2: Verify Watcher Protocol 1,000 nodes, collapse, zero suffering, and quarantine."""
        cluster = WatcherCluster()
        self.assertEqual(len(cluster.nodes), 1000)

        # Test deterministic wavefunction collapse
        psi_superposition = {
            "Trajectory_Left": complex(1.0 / math.sqrt(2), 0.0),
            "Trajectory_Right": complex(1.0 / math.sqrt(2), 0.0)
        }
        collapse_telemetry = cluster.collapse_wavefunction(psi_superposition, target_basis="Trajectory_Right")
        self.assertEqual(collapse_telemetry["collapsed_state"], "Trajectory_Right")
        self.assertEqual(collapse_telemetry["eigenstate_probability"], 1.0)
        self.assertEqual(collapse_telemetry["thermal_radiation_loss_joules"], 0.0)
        self.assertEqual(collapse_telemetry["gate_fidelity"], 0.99987)
        self.assertEqual(collapse_telemetry["watcher_nodes_engaged"], 1000)

        # Test macroscopic superposition resolution (12,000 kg vehicle)
        macro_result = cluster.observe_macroscopic_superposition(mass_kg=12000.0)
        self.assertEqual(macro_result["macroscopic_mass_kg"], 12000.0)
        self.assertTrue(macro_result["decoherence_threshold_suppressed"])
        self.assertEqual(macro_result["collapse_telemetry"]["eigenstate_probability"], 1.0)

        # Test Zero Subjective Suffering guarantee
        pain_stimulus = {"intensity": 9.8, "stimulus_type": "HIGH_ENERGY_PARTICLE_COLLISION", "tissue_id": "EPITHELIUM_04"}
        decoupled = cluster.filter_subjective_suffering(pain_stimulus)
        self.assertEqual(decoupled["subjective_pain_experienced"], 0.0)
        self.assertEqual(decoupled["cognitive_friction"], 0.0)
        self.assertEqual(decoupled["somatic_stress_metric"], 9.8)

        # Test Dimensional Quarantine Firewall: P(Breach) = 0.0
        quarantine = cluster.enforce_layer_quarantine(e_leviathan_joules=1.0e18, delta_t_seconds=1e-6)
        self.assertEqual(quarantine["breach_probability"], 0.0)
        self.assertFalse(quarantine["is_breach_possible"])
        self.assertTrue(quarantine["firewall_engaged"])

    def test_03_chronos_entropy_inversion_and_recycling(self):
        """Battery 3: Verify Time-Reversal Operator (ΔS < 0) and Abraxas recycling."""
        governor = ChronosEntropyGovernor()

        # Test Time-Reversal Operator: p -> -p, S -> -S, ΔS < 0
        p_init = (1.5, -2.0, 3.2)
        s_init = (0.5, 0.0, -0.5)
        reversal = governor.apply_time_reversal_operator(
            particle_momentum=p_init,
            particle_spin=s_init,
            kinetic_energy_recovery_joules=5.008,
            bond_energy_kj_mol=798.0
        )
        self.assertEqual(reversal["inverted_momentum"], (-1.5, 2.0, -3.2))
        self.assertEqual(reversal["inverted_spin"], (-0.5, 0.0, 0.5))
        self.assertLess(reversal["delta_s_entropy"], 0.0)  # Localized negative entropy
        self.assertEqual(reversal["recovered_energy_joules"], 5.008)

        # Test Abraxas Closed-Loop Recycling: exhaust light -> dark matter -> rendered light
        initial_total = governor.rendered_baryonic_joules + governor.unrendered_dark_matter_joules
        recycle_report = governor.recycle_light_exhaust(spent_photon_energy_joules=1.0e20)
        final_total = recycle_report["conserved_total_energy_joules"]
        self.assertAlmostEqual(initial_total, final_total, delta=1.0)
        self.assertGreater(recycle_report["recycled_energy_joules"], 0.0)

        # Test Chronos-Flow Dilation
        dilation_norm = governor.compute_chronos_dilation(active_cognitive_nodes=1000000)
        self.assertAlmostEqual(dilation_norm["chronos_flow_multiplier"], 1.0, places=4)
        dilation_heavy = governor.compute_chronos_dilation(active_cognitive_nodes=10000000000)  # 10B nodes
        self.assertAlmostEqual(dilation_heavy["chronos_flow_multiplier"], 0.999996, places=6)

        # Test Hyper-Elements 201-206
        chronium = governor.evaluate_hyper_element(201)
        self.assertIsNotNone(chronium)
        self.assertEqual(chronium["name"], "Chronium")
        self.assertEqual(chronium["symbol"], "Ch")
        self.assertEqual(chronium["protons"], 201)
        self.assertEqual(chronium["neutrons"], 303)
        self.assertEqual(chronium["resonance_hz"], 8.44e12)

    def test_04_mps_and_holographic_boundary_compression(self):
        """Battery 4: Verify Matrix Product States (MPS) & Holographic Boundary Compression."""
        mps = MatrixProductStateEngine(num_qubits=999000000)
        state_rep = mps.compute_state_representation(active_sites=64)
        self.assertTrue(state_rep["is_state_tractable"])
        self.assertEqual(state_rep["surface_code_distance"], 27)
        self.assertEqual(state_rep["entangium_coherent_nodes"], 98)

        # Verify Holographic Boundary Compressor avoids Bekenstein collapse
        compressor = HolographicBoundaryCompressor()
        holo = compressor.compute_boundary_wavefunction(surface_area_m2=1.0e12, recursion_depth=10)
        self.assertTrue(holo["is_below_bekenstein_bound"])
        self.assertEqual(holo["total_simulated_universe_mass_energy"], 0.0)
        self.assertEqual(holo["holographic_closure"], "VERIFIED_COMPUTATIONALLY_MASSLESS")

    def test_05_void_skipper_metric_drive_and_causality(self):
        """Battery 5: Verify Void-Skipper Metric Drive (0.0 G) and Paradox Resolvers."""
        drive = VoidSkipperMetricDrive()
        # Test displacement at 0.5c
        metric = drive.calculate_displacement_metric(
            dissolution_velocity_m_s=0.5 * SubstrateConstants.SPEED_OF_LIGHT,
            displacement_vector_m=(1000.0, 0.0, 0.0),
            proper_time_delta_s=1.0e-3
        )
        self.assertEqual(metric["internal_perceived_g_force"], 0.0)
        self.assertEqual(metric["inertial_neutrality"], "ABSOLUTE_ZERO_G")
        self.assertAlmostEqual(metric["beta_ratio_vs_c"], 0.5, places=5)
        self.assertAlmostEqual(metric["metric_tensor_g00"], -0.75, places=5)

        # Test Novikov Paradox Resolver
        resolver = CausalityFractureResolver()
        paradox = resolver.resolve_paradox_attempt("GRANDFATHER_DELETION")
        self.assertEqual(paradox["execution_probability"], 0.0)
        self.assertTrue(paradox["causality_preserved"])

        # Test Everettian Timeline Bifurcation
        bifurcation = resolver.bifurcate_timeline(t_origin_timestamp=100.0, ftl_data_packet={"msg": "ALERT"})
        self.assertEqual(bifurcation["causality_integrity"], "CONSERVED_ACROSS_EVERETTIAN_BRANCHES")

        # Test Biological Vessel API
        vessel = BiologicalVesselAPI()
        packet = vessel.transmit_cognitive_packet(avatar_dna_id="HOMO_SAPIENS_V6_001", algorithmic_payload={"algo": "PRIME_MAP"})
        self.assertEqual(packet["carrier_frequency_hz"], 2.4e9)
        self.assertEqual(packet["cymatic_reception_layer"], "NON_CODING_DNA_API")
        self.assertFalse(packet["localized_free_will_violated"])

    def test_06_unified_aethercore_and_cognitive_bridge(self):
        """Battery 6: Verify Substrate-Indexed Realism & EtherCoreCognitiveBridge integration."""
        engine = AetherCoreSimulationEngine()
        sir_eval = engine.evaluate_substrate_indexed_realism()
        self.assertEqual(sir_eval["axiom"], "SUBSTRATE_INDEXED_REALISM (SIR)")
        self.assertEqual(sir_eval["status"], "SIR_AXIOM_SATISFIED")
        self.assertEqual(sir_eval["internal_ontological_validity"], "OBJECTIVELY_REAL_TO_INHABITANTS")

        # Test Bridge runtime binding
        bridge = EtherCoreCognitiveBridge()
        self.assertIsNotNone(bridge.watcher)
        self.assertIsNotNone(bridge.chronos)
        self.assertIsNotNone(bridge.simulation_engine)


if __name__ == "__main__":
    unittest.main()
