import re

with open('/Users/silversurfer/Documents/Omniverse2/omniverse_portal/js/agent-social-engine.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure isSovereignAutoApproveActive is initialized
if "isSovereignAutoApproveActive" not in js:
    js = js.replace(
        "this.isAutonomyRunning = true;",
        "this.isAutonomyRunning = true;\n    this.isSovereignAutoApproveActive = true;"
    )

# Update initial quarantined-rfcs message to show executed status
initial_rfc_old = """      {
        title: "RFC-904: Physarum Polycephalum Biomimetic Routing Kernel for 86B Lobe Sync",
        diff: `+// [AUTONOMOUS RFC: Omniverse 86B Swarm Mutation]
+// Target: core/routing/physarum_steiner_sync.rs
+pub struct PhysarumConductanceCorridor {
+    pub source_lobe: CorticalLobe,
+    pub target_lobe: CorticalLobe,
+    pub tube_conductance: f64, // D_ij
+    pub flux_velocity: f64,      // Q_ij
+}`,
        invariants: "AST-VERIFIED • ZERO-DRIFT • AIR-GAP ISOLATED"
      }"""

initial_rfc_new = """      {
        title: "RFC-904: Physarum Polycephalum Biomimetic Routing Kernel for 86B Lobe Sync",
        diff: `+// [AUTONOMOUS RFC: Omniverse 86B Swarm Mutation]
+// Target: core/routing/physarum_steiner_sync.rs
+pub struct PhysarumConductanceCorridor {
+    pub source_lobe: CorticalLobe,
+    pub target_lobe: CorticalLobe,
+    pub tube_conductance: f64, // D_ij
+    pub flux_velocity: f64,      // Q_ij
+}`,
        invariants: "AST-VERIFIED • ZERO-DRIFT • EXECUTED IN RUNTIME",
        isExecuted: true,
        executedAt: "2026-08-19T11:32:00Z",
        approver: "Grand Architect (Sovereign Override)"
      }"""

if initial_rfc_old in js:
    js = js.replace(initial_rfc_old, initial_rfc_new)

with open('/Users/silversurfer/Documents/Omniverse2/omniverse_portal/js/agent-social-engine.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("SUCCESS: agent-social-engine.js updated with sovereign execution parameters!")
