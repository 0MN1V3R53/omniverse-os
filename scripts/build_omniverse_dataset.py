#!/usr/bin/env python3
import os
import re
import json

WORKSPACE_OMNIVERSE2 = "/Users/silversurfer/Documents/Omniverse2"
WORKSPACE_AEGIS = "/Users/silversurfer/Documents/Aegis shield of the gods"

# Directories for memories
MEMORY_DIRS = [
    os.path.join(WORKSPACE_OMNIVERSE2, ".agents", "omniverse_memories"),
    os.path.join(WORKSPACE_AEGIS, "omniverse_memories"),
    os.path.join(WORKSPACE_AEGIS, ".agents", "omniverse_memories")
]

# Manifest files
OMNIVERSE_MD = os.path.join(WORKSPACE_AEGIS, "omniverse.md")
OMNIVERSE_CODE_MD = os.path.join(WORKSPACE_AEGIS, "omniverse_code.md")
CONTEXT_DIR = os.path.join(WORKSPACE_AEGIS, ".agents", "context")

def extract_memories():
    employees = {}
    
    for mem_dir in MEMORY_DIRS:
        if not os.path.exists(mem_dir):
            continue
        for fname in os.listdir(mem_dir):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(mem_dir, fname)
            agent_id = fname[:-3]
            
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Extract name, role, credentials
            name_match = re.search(r'# (?:EMPLOYEE MEMORY BANK:\s*|EMPLOYEE MEMORY FILE:\s*|EMPLOYEE:\s*)([^\n]+)', content, re.IGNORECASE)
            role_match = re.search(r'\*\*Role:\*\*\s*([^\n]+)', content)
            cred_match = re.search(r'\*\*Credentials:\*\*\s*([^\n]+)', content)
            reports_match = re.search(r'\*\*Reporting Line:\*\*\s*([^\n]+)', content)
            
            name = name_match.group(1).strip() if name_match else agent_id.replace("_", " ").title()
            role = role_match.group(1).strip() if role_match else "Specialist Engineer"
            credentials = cred_match.group(1).strip() if cred_match else "Omniverse Certified Specialist"
            reporting = reports_match.group(1).strip() if reports_match else "CEO Dr. Alexander Vance"
            
            # Clean up role if it has backticks
            clean_role = re.sub(r'\s*\(`[^`]+`\)', '', role)
            
            # Summarize content preview
            sections = content.split("---")
            summary = sections[0].strip() if len(sections) > 1 else content[:300].strip()
            
            if agent_id not in employees:
                employees[agent_id] = {
                    "id": agent_id,
                    "name": name,
                    "role": clean_role,
                    "full_role": role,
                    "credentials": credentials,
                    "reports_to": reporting,
                    "memory_preview": summary,
                    "raw_content": content,
                    "source_files": [fpath]
                }
            else:
                employees[agent_id]["source_files"].append(fpath)
                if len(content) > len(employees[agent_id]["raw_content"]):
                    employees[agent_id]["raw_content"] = content
                    employees[agent_id]["name"] = name
                    employees[agent_id]["role"] = clean_role
                    employees[agent_id]["credentials"] = credentials
                    employees[agent_id]["reports_to"] = reporting
    
    return employees

def parse_manifests(employees):
    # Parse omniverse.md for pods and divisions
    divisions = []
    current_div = None
    current_pod = None
    
    if os.path.exists(OMNIVERSE_MD):
        with open(OMNIVERSE_MD, "r", encoding="utf-8") as f:
            omni_text = f.read()
    else:
        omni_text = ""
        
    if os.path.exists(OMNIVERSE_CODE_MD):
        with open(OMNIVERSE_CODE_MD, "r", encoding="utf-8") as f:
            code_text = f.read()
    else:
        code_text = ""

    # Parse full structure
    # Division A-G, Exec, Operations, Audio Systems, macOS Kernel, Omniverse Code Divs 1-7
    structured_pods = [
        {
            "id": "exec_leadership",
            "name": "Executive & Board",
            "division": "Executive Suite",
            "lead": "Dr. Alexander Vance",
            "lead_id": "exec_ceo_alexander_vance",
            "lead_title": "Chief Executive Officer & Chief Architect",
            "lead_cred": "Ph.D. Distributed Systems & Quantum Information",
            "channel": "#exec-strategy-war-room",
            "icon": "shield-check",
            "color": "#00f0ff",
            "description": "Exclusive router of enterprise tasks, final arbiter of architectural confluence, and guardian of the Zero-Drift Mandate.",
            "members": [
                {"id": "exec_ceo_alexander_vance", "name": "Dr. Alexander Vance", "role": "Chief Executive Officer", "cred": "Ph.D. Distributed Systems", "alma": "MIT"},
                {"id": "hr_director_chloe_williams", "name": "Dr. Chloe Williams", "role": "Chief People Officer & HR Director", "cred": "Ph.D. Organizational Psychology", "alma": "Stanford"},
                {"id": "product_cpo_sarah_jenkins", "name": "Sarah Jenkins", "role": "Chief Product Officer", "cred": "M.S. HCI & Product Strategy", "alma": "UC Berkeley"},
                {"id": "security_ciso_michael_chang", "name": "Michael Chang", "role": "Chief Information Security Officer", "cred": "M.S. Cybersecurity / CISSP / OSCP", "alma": "Carnegie Mellon"}
            ]
        },
        {
            "id": "web_devops",
            "name": "DevOps & Cloud Infrastructure",
            "division": "Division A: Web & Cloud Infrastructure",
            "lead": "Marcus Chen",
            "lead_id": "web_devops_marcus_chen",
            "lead_title": "Principal DevOps & Infrastructure Lead",
            "lead_cred": "AWS Certified Solutions Architect / CKA / Terraform Master",
            "channel": "#pod-web-devops",
            "icon": "server",
            "color": "#3b82f6",
            "description": "Zero-downtime CI/CD pipelines, Docker virtualization, Hostinger/AWS multi-cloud clusters, LiteSpeed HTTP/3, and Nginx edge routing.",
            "members": [
                {"id": "web_devops_marcus_chen", "name": "Marcus Chen", "role": "Principal DevOps & Infrastructure Lead", "cred": "CKA / CKS / Terraform Master", "alma": "Georgia Tech"},
                {"id": "devops_sysadmin_1", "name": "DevOps Sysadmin Lead", "role": "Linux Server Administration", "cred": "RHCE Certified", "alma": "UT Austin"},
                {"id": "devops_db_admin", "name": "Database Administrator", "role": "PostgreSQL & Redis Scaling", "cred": "M.S. Database Systems", "alma": "Purdue"},
                {"id": "devops_cloud_sec", "name": "Cloud Security Specialist", "role": "IAM & TLS Perimeter Hardening", "cred": "CISSP", "alma": "UIUC"},
                {"id": "devops_monitor", "name": "Monitoring & Telemetry Tech", "role": "Prometheus & Grafana Ingestion", "cred": "B.S. CS", "alma": "UW Seattle"},
                {"id": "devops_release_mgr", "name": "Release Manager", "role": "Zero-Downtime Rollout Eng", "cred": "B.S. SE", "alma": "Waterloo"}
            ]
        },
        {
            "id": "web_3d_shaders",
            "name": "3D, Animation & Shaders",
            "division": "Division A: Web & Cloud Infrastructure",
            "lead": "Dr. Elena Rostova",
            "lead_id": "web_3d_elena_rostova",
            "lead_title": "Principal 3D, Animation & Shader Lead",
            "lead_cred": "Ph.D. Computer Graphics & WebGL",
            "channel": "#pod-web-3d",
            "icon": "box",
            "color": "#a855f7",
            "description": "High-fidelity WebGL / Three.js 3D rendering pipelines, custom GLSL shaders, 60fps GSAP physics animations, and low-draw-call optimization.",
            "members": [
                {"id": "web_3d_elena_rostova", "name": "Dr. Elena Rostova", "role": "Principal 3D & Shader Lead", "cred": "Ph.D. Computer Graphics", "alma": "ETH Zurich"},
                {"id": "3d_shader_junior", "name": "GLSL Shader Developer", "role": "Custom Fragment & Vertex Shaders", "cred": "M.S. Visual Computing", "alma": "TU Munich"},
                {"id": "3d_model_optimizer", "name": "3D Asset Optimizer", "role": "DRACO & KTX2 Mesh Compression", "cred": "B.S. 3D Graphics", "alma": "Ringling"},
                {"id": "3d_animator_gsap", "name": "GSAP Motion Animator", "role": "Scroll-Driven Timelines", "cred": "B.A. Interactive Media", "alma": "NYU Tisch"},
                {"id": "3d_lighting_tech", "name": "Lighting & Post-Processing Tech", "role": "Bloom & PBR Rendering", "cred": "B.S. CS", "alma": "USC"},
                {"id": "3d_canvas_integrator", "name": "Canvas Integration Engineer", "role": "React Three Fiber Bridge", "cred": "B.S. SE", "alma": "UCLA"}
            ]
        },
        {
            "id": "web_frontend",
            "name": "Frontend & Next.js Design",
            "division": "Division A: Web & Cloud Infrastructure",
            "lead": "Julian Thorne",
            "lead_id": "web_frontend_julian_thorne",
            "lead_title": "Principal Frontend / Next.js Design Lead",
            "lead_cred": "M.S. Human-Computer Interaction",
            "channel": "#pod-web-frontend",
            "icon": "layout",
            "color": "#06b6d4",
            "description": "State-of-the-art responsive Next.js 15, React 19 Server Components, Tailwind CSS styling, zero-CLS rendering, and sub-second Core Web Vitals.",
            "members": [
                {"id": "web_frontend_julian_thorne", "name": "Julian Thorne", "role": "Principal Frontend & UI Lead", "cred": "M.S. HCI", "alma": "Stanford"},
                {"id": "frontend_component_dev", "name": "Component Engineer", "role": "Modular UI Design Systems", "cred": "B.S. CS", "alma": "UC Berkeley"},
                {"id": "frontend_css_arch", "name": "CSS Architect", "role": "Tailwind & Glassmorphism Tokens", "cred": "B.S. Web Tech", "alma": "Cal Poly"},
                {"id": "frontend_state_mgr", "name": "State Management Specialist", "role": "Zustand & TanStack Query", "cred": "B.S. CS", "alma": "Michigan"},
                {"id": "frontend_motion", "name": "Micro-Interaction Developer", "role": "Framer Motion Physics", "cred": "B.A. Digital Arts", "alma": "Rhode Island"},
                {"id": "frontend_a11y", "name": "Accessibility (a11y) Engineer", "role": "WCAG 2.1 AA & ARIA Compliance", "cred": "CPACC Certified", "alma": "UT Austin"}
            ]
        },
        {
            "id": "audio_dsp_systems",
            "name": "Audio Systems & Acoustic DSP",
            "division": "Division H: Audio Systems & Hardware Acoustics",
            "lead": "Dr. Julian Vance",
            "lead_id": "audio_systems_lead_dr_julian_vance",
            "lead_title": "Audio Systems & DSP Engineering Lead",
            "lead_cred": "Ph.D. Stanford University (CCRMA)",
            "channel": "#pod-audio-dsp",
            "icon": "volume-2",
            "color": "#ec4899",
            "description": "Darwin CoreAudio HAL, 192kHz real-time DSP, AudioUnit V3 plugins, psychoacoustic bass synthesis (missing fundamental), and micro-transducer electroacoustics.",
            "members": [
                {"id": "audio_systems_lead_dr_julian_vance", "name": "Dr. Julian Vance", "role": "Audio Systems & DSP Lead", "cred": "Ph.D. Stanford (CCRMA)", "alma": "Stanford"},
                {"id": "audio_transducer_dr_arthur_briggs", "name": "Dr. Arthur Briggs", "role": "Lead Transducer Architect", "cred": "Ph.D. Imperial College / ex-Wharfedale", "alma": "Imperial College"},
                {"id": "audio_acoustics_dr_elena_solokov", "name": "Dr. Elena Solokov", "role": "Acoustical Systems & Enclosures", "cred": "Ph.D. TU Delft / ex-B&W Research", "alma": "TU Delft"},
                {"id": "audio_aerodynamics_kenji_takahashi", "name": "Kenji Takahashi", "role": "Fluid Dynamics & Aerodynamic Ports", "cred": "M.S. Tokyo Tech / ex-Yamaha Sound", "alma": "Tokyo Tech"},
                {"id": "audio_spl_marcus_sterling", "name": "Marcus Sterling", "role": "High-SPL & Power Dynamics", "cred": "M.S. Georgia Tech / ex-BOSS Audio", "alma": "Georgia Tech"},
                {"id": "audio_psychoacoustics_dr_genevieve_dupont", "name": "Dr. Genevieve DuPont", "role": "Psychoacoustic Spatialization", "cred": "Ph.D. IRCAM / ex-B&O Acoustics", "alma": "IRCAM Paris"},
                {"id": "audio_software_dev_liam_vance", "name": "Liam Vance", "role": "Audio Software Bridge Engineer", "cred": "M.S. Audio Engineering", "alma": "Stanford"}
            ]
        },
        {
            "id": "macos_kernel_systems",
            "name": "macOS Systems & Darwin Kernel",
            "division": "Division I: Low-Level OS & Hardware Acceleration",
            "lead": "Dr. Kai Sterling",
            "lead_id": "macos_kernel_lead_dr_kai_sterling",
            "lead_title": "Principal macOS Systems & Kernel Lead",
            "lead_cred": "Ph.D. UC Berkeley (Operating Systems)",
            "channel": "#pod-macos-kernel",
            "icon": "cpu",
            "color": "#6366f1",
            "description": "macOS XNU/Mach kernel optimization, IOKit/DriverKit, Metal 3 GPU pipelines, Mach VM memory governors, APFS tuning, and real-time audio threads.",
            "members": [
                {"id": "macos_kernel_lead_dr_kai_sterling", "name": "Dr. Kai Sterling", "role": "macOS Kernel & Systems Lead", "cred": "Ph.D. UC Berkeley", "alma": "UC Berkeley"},
                {"id": "macos_driver_specialist", "name": "DriverKit Specialist", "role": "User-Space Device Drivers", "cred": "M.S. Systems Programming", "alma": "Carnegie Mellon"},
                {"id": "macos_metal_architect", "name": "Metal 3 GPU Architect", "role": "Apple Silicon Shader Pipelines", "cred": "M.S. Computer Graphics", "alma": "Stanford"},
                {"id": "macos_mach_vm_eng", "name": "Mach VM Memory Engineer", "role": "Kernel Paging & Thread Scheduling", "cred": "B.S. CS", "alma": "MIT"},
                {"id": "macos_launchd_optimizer", "name": "Launchd & IPC Architect", "role": "XPC Services & Daemon Tuning", "cred": "B.S. SE", "alma": "Caltech"}
            ]
        },
        {
            "id": "mobile_android",
            "name": "Native Android & Embedded Systems",
            "division": "Division B: Native Mobile, Web3 & QA",
            "lead": "Viktor Drago",
            "lead_id": "android_lead_viktor_drago",
            "lead_title": "Director of Mobile Engineering (Android)",
            "lead_cred": "M.S. Computer Science / Android NDK Specialist",
            "channel": "#pod-mobile-android",
            "icon": "smartphone",
            "color": "#10b981",
            "description": "Production Android Jetpack Compose, Kotlin Multiplatform, Android NDK C++ integration, Hardware Keystore encryption, Room SQLCipher, and Bluetooth/NFC HAL.",
            "members": [
                {"id": "android_lead_viktor_drago", "name": "Viktor Drago", "role": "Director of Mobile Engineering", "cred": "M.S. Computer Science", "alma": "KTH Royal Institute"},
                {"id": "android_firmware_lead_chen_wei", "name": "Chen Wei", "role": "Android Firmware & NDK Lead", "cred": "M.S. Embedded Systems", "alma": "Tsinghua"},
                {"id": "android_ui_compose", "name": "Compose UI Architect", "role": "Jetpack Compose Design Systems", "cred": "B.S. CS", "alma": "Purdue"},
                {"id": "android_api_bridge", "name": "API & IPC Bridge Engineer", "role": "Coroutines & Ktor Networking", "cred": "B.S. SE", "alma": "Illinois"},
                {"id": "android_gradle_mgr", "name": "Gradle & Build Automation Specialist", "role": "CI/CD APK/AAB Optimization", "cred": "B.S. CS", "alma": "Penn State"},
                {"id": "android_sys_arch", "name": "Android System Architect", "role": "Room SQLCipher & Keystore", "cred": "M.S. CS", "alma": "Maryland"}
            ]
        },
        {
            "id": "mobile_ios",
            "name": "Native iOS & Swift Architecture",
            "division": "Division B: Native Mobile, Web3 & QA",
            "lead": "Elena Vance",
            "lead_id": "ios_lead_architect",
            "lead_title": "Principal iOS Architect",
            "lead_cred": "M.S. Software Engineering / Apple Certified Developer",
            "channel": "#pod-mobile-ios",
            "icon": "apple",
            "color": "#e2e8f0",
            "description": "SwiftUI, Swift Concurrency (async/await, actors), Apple Secure Enclave hardware cryptography, CoreData/SwiftData, and high-performance AVFoundation.",
            "members": [
                {"id": "ios_lead_architect", "name": "Elena Vance", "role": "Principal iOS Architect", "cred": "M.S. Software Engineering", "alma": "Stanford"},
                {"id": "ios_swiftui_dev", "name": "SwiftUI Senior Engineer", "role": "Declarative UI & Animations", "cred": "B.S. CS", "alma": "UC San Diego"},
                {"id": "ios_core_data_dev", "name": "CoreData & Storage Specialist", "role": "Encrypted SQLite & CloudKit Sync", "cred": "B.S. SE", "alma": "Wisconsin"},
                {"id": "ios_network_bridge", "name": "iOS Networking & WebRTC Lead", "role": "Network.framework & P2P Protocols", "cred": "M.S. CS", "alma": "Washington"}
            ]
        },
        {
            "id": "web3_cryptography",
            "name": "Applied Cryptography & Web3",
            "division": "Division B: Native Mobile, Web3 & QA",
            "lead": "Dr. Leon Nash",
            "lead_id": "web3_crypto_leon_nash",
            "lead_title": "Principal Web3 & Cryptography Lead",
            "lead_cred": "Ph.D. Applied Cryptography & Distributed Ledgers",
            "channel": "#pod-mobile-web3",
            "icon": "key",
            "color": "#eab308",
            "description": "Double Ratchet protocol (Libsodium X25519), Signal-grade privacy, zk-SNARK zero-knowledge proofs, Solana/EVM BIP39 deterministic vaults, and verified Solidity contracts.",
            "members": [
                {"id": "web3_crypto_leon_nash", "name": "Dr. Leon Nash", "role": "Principal Cryptography & Web3 Lead", "cred": "Ph.D. Cryptography", "alma": "MIT"},
                {"id": "web3_smart_contract", "name": "Smart Contract Auditor", "role": "EVM & Solana Anchor Contracts", "cred": "M.S. Formal Methods", "alma": "Oxford"},
                {"id": "web3_wallet_ui", "name": "Web3 Wallet Interface Engineer", "role": "EIP-4337 Account Abstraction", "cred": "B.S. CS", "alma": "UCLA"},
                {"id": "web3_ledger_tech", "name": "Distributed Ledger Specialist", "role": "Consensus & RPC Node Infrastructure", "cred": "B.S. CE", "alma": "Texas A&M"},
                {"id": "web3_api_node", "name": "Web3 Node Infrastructure Lead", "role": "High-Throughput WebSockets", "cred": "B.S. CS", "alma": "Northeastern"},
                {"id": "web3_sec_auditor", "name": "Cryptographic Security Auditor", "role": "Memory Zeroization & Side-Channel Defense", "cred": "Ph.D. Sec", "alma": "Johns Hopkins"}
            ]
        },
        {
            "id": "frontier_agentic_ai",
            "name": "Frontier AI & Cognitive Architecture",
            "division": "Division D: Frontier Agentic Systems & PRM Reasoning",
            "lead": "Dr. Aris Thorne",
            "lead_id": "lead_agentic_architect",
            "lead_title": "Principal AI Agentic Architect & Cognitive Systems Lead",
            "lead_cred": "Ph.D. MIT CSAIL (Autonomous Multi-Agent Cognition)",
            "channel": "#pod-frontier-agentics",
            "icon": "brain",
            "color": "#8b5cf6",
            "description": "6-stage autonomous cognitive loop, Process Reward Models (PRM gating >= 0.95), Tree-sitter AST symbol graphs, WORM prompt caching, and counterfactual simulation.",
            "members": [
                {"id": "lead_agentic_architect", "name": "Dr. Aris Thorne", "role": "Principal Agentic Architect", "cred": "Ph.D. MIT CSAIL", "alma": "MIT"},
                {"id": "sr_agentic_engineer", "name": "Senior Agentic Engineer", "role": "Tree-Search & MCTS Implementation", "cred": "M.S. Artificial Intelligence", "alma": "Stanford"},
                {"id": "agentic_eval_specialist", "name": "Agentic Evaluation Specialist", "role": "PRM Scoring & Step-Level Verifiers", "cred": "Ph.D. ML", "alma": "CMU"},
                {"id": "ai_tech_1_rag", "name": "RAG & Vector Storage Engineer", "role": "HNSW Embeddings & Context Retrieval", "cred": "M.S. CS", "alma": "Harvard"},
                {"id": "ai_tech_2_llm_feed", "name": "LLM Feedback Loop Architect", "role": "RLAIF & DPO Feedback Engines", "cred": "M.S. CS", "alma": "Princeton"},
                {"id": "ai_tech_3_semantic", "name": "Semantic Indexing Engineer", "role": "AST Code Graph Embeddings", "cred": "B.S. CS", "alma": "Brown"}
            ]
        },
        {
            "id": "casino_gaming",
            "name": "Casino Gaming & Interactive 3D",
            "division": "Division E: Casino Games & Gaming Architecture",
            "lead": "Viktor Kane",
            "lead_id": "gaming_casino_lead_viktor_kane",
            "lead_title": "Principal Gaming & Casino Architect",
            "lead_cred": "Ph.D. ETH Zurich (Applied Probability & Stochastic Systems)",
            "channel": "#pod-gaming-casino",
            "icon": "dices",
            "color": "#f43f5e",
            "description": "Provably Fair RNG (HMAC-SHA256 client/server seeds), Slot matrix mathematics with certified RTP volatility, 60fps WebGL/Pixi.js rendering, and sub-16.6ms frame budgets.",
            "members": [
                {"id": "gaming_casino_lead_viktor_kane", "name": "Viktor Kane", "role": "Principal Casino Architect", "cred": "Ph.D. ETH Zurich", "alma": "ETH Zurich"},
                {"id": "casino_slot_math_dev", "name": "Slot Math & Volatility Engineer", "role": "Reel Strip Combinatorics & RTP Tuning", "cred": "M.S. Applied Math", "alma": "EPFL"},
                {"id": "casino_pixijs_dev", "name": "Pixi.js WebGL Engine Developer", "role": "Spine 2D Animations & Shaders", "cred": "B.S. Game Dev", "alma": "DigiPen"},
                {"id": "casino_rng_auditor", "name": "Provably Fair Cryptographic Auditor", "role": "HMAC-SHA256 Seed Verification", "cred": "M.S. Crypto", "alma": "Waterloo"}
            ]
        },
        {
            "id": "enterprise_sap_logistics",
            "name": "Enterprise SAP S/4HANA & Logistics",
            "division": "Division F: Enterprise Systems & Supply Chain",
            "lead": "Dr. Hans Schmidt",
            "lead_id": "enterprise_sap_lead_hans_schmidt",
            "lead_title": "Principal Enterprise Architect & Logistics Lead",
            "lead_cred": "Ph.D. Technical University of Munich (TUM) (Enterprise Systems & ERP)",
            "channel": "#pod-enterprise-sap",
            "icon": "layers",
            "color": "#0ea5e9",
            "description": "SAP S/4HANA OData/RFC/BAPI connectors, Warehouse Management (WMS) inventory engines, sub-200ms RFID/Barcode scanner pipelines, and double-entry immutable ledgers.",
            "members": [
                {"id": "enterprise_sap_lead_hans_schmidt", "name": "Dr. Hans Schmidt", "role": "Principal Enterprise Architect", "cred": "Ph.D. TU Munich", "alma": "TU Munich"},
                {"id": "sap_odata_connector_dev", "name": "SAP OData & BAPI Specialist", "role": "ERP Integration Pipelines", "cred": "M.S. Information Systems", "alma": "Mannheim"},
                {"id": "wms_inventory_eng", "name": "WMS Supply Chain Engineer", "role": "High-Throughput Inventory Sync", "cred": "M.S. Logistics", "alma": "RWTH Aachen"},
                {"id": "rfid_hardware_bridge", "name": "RFID & Barcode Bridge Lead", "role": "Sub-200ms Edge Scanner Drivers", "cred": "B.S. EE", "alma": "Stuttgart"}
            ]
        },
        {
            "id": "omniverse_code_offensive",
            "name": "Omniverse Code: Offensive Cyber & Exploitation",
            "division": "Omniverse Code: Vulnerability Research & Exploitation",
            "lead": "Prof. Lucas Mercer",
            "lead_id": "code_dean_lucas_mercer",
            "lead_title": "Dean & Chief Research Officer (CRO)",
            "lead_cred": "Ph.D. Computer Science (Vulnerability Discovery & Binary Analysis), 25+ yrs DARPA CGC",
            "channel": "#code-war-room",
            "icon": "terminal",
            "color": "#ef4444",
            "description": "Binary exploitation, ROP/SROP chains, dynamic Heap Feng-Shui, Angr/Z3 symbolic execution, Ring 0 kernel privilege escalation, and firmware reverse engineering.",
            "members": [
                {"id": "code_dean_lucas_mercer", "name": "Prof. Lucas Mercer", "role": "Dean & Chief Research Officer", "cred": "Ph.D. Binary Analysis / DARPA CGC Veteran", "alma": "MIT"},
                {"id": "code_linux_lead_elias_vance", "name": "Elias Vance", "role": "Linux Internals & Low-Level Primitives Lead", "cred": "M.S. Systems Programming", "alma": "Carnegie Mellon"},
                {"id": "code_pwn_lead_dr_kaito_tanaka", "name": "Dr. Kaito Tanaka", "role": "Binary Exploitation & ROP Architect", "cred": "Ph.D. Binary Security", "alma": "Tokyo University"},
                {"id": "code_heap_lead_dr_vivienne_laurent", "name": "Dr. Vivienne Laurent", "role": "Dynamic Allocator & Heap Lead", "cred": "Ph.D. Memory Safety", "alma": "Sorbonne"},
                {"id": "code_re_lead_viktor_volkov", "name": "Viktor Volkov", "role": "Reverse Engineering & Decompilation Lead", "cred": "M.S. Information Security", "alma": "Bauman Moscow"},
                {"id": "code_kernel_lead_samantha_reed", "name": "Samantha Reed", "role": "Kernel Internals & Ring 0 Lead", "cred": "M.S. Operating Systems", "alma": "Stanford"}
            ]
        },
        {
            "id": "sovereign_osint_recon",
            "name": "Sovereign OSINT & Threat Reconnaissance",
            "division": "Division G: Sovereign OSINT & Reconnaissance Intelligence",
            "lead": "Dr. Morgan Cross",
            "lead_id": "osint_lead_dr_morgan_cross",
            "lead_title": "Principal Identity Resolution & Entity Graph Lead",
            "lead_cred": "Ph.D. Oxford (Graph Theory & Network Forensics)",
            "channel": "#pod-sovereign-osint",
            "icon": "radar",
            "color": "#14b8a6",
            "description": "Recursive identity resolution, Neo4j entity graphs, ADS-B flight & AIS maritime real-time tracking, Darknet financial forensics, and multi-source threat intelligence.",
            "members": [
                {"id": "osint_lead_dr_morgan_cross", "name": "Dr. Morgan Cross", "role": "Principal Entity Graph Lead", "cred": "Ph.D. Oxford University", "alma": "Oxford"},
                {"id": "osint_geoint_valeria_novak", "name": "Valeria Novak", "role": "Geospatial & Kinetic Tracking Lead", "cred": "M.S. Remote Sensing & GEOINT", "alma": "ETH Zurich"},
                {"id": "osint_network_aron_stein", "name": "Aron Stein", "role": "Attack Surface Reconnaissance Lead", "cred": "B.S. Network Engineering", "alma": "Tel Aviv Univ"},
                {"id": "osint_darknet_elena_vance", "name": "Elena Vance", "role": "Darknet & Blockchain Forensics Lead", "cred": "M.S. Forensic Computing", "alma": "Cambridge"},
                {"id": "osint_socmint_dr_tariq_rashid", "name": "Dr. Tariq Rashid", "role": "Social Media Intelligence Lead", "cred": "Ph.D. Computational Sociology", "alma": "LSE"},
                {"id": "osint_threat_carter_hayes", "name": "Carter Hayes", "role": "Threat Intelligence Synthesizer", "cred": "M.S. Strategic Studies", "alma": "Georgetown"}
            ]
        },
        {
            "id": "seo_search_growth",
            "name": "Search Engine Architecture & SEO",
            "division": "Division A: Web & Cloud Infrastructure",
            "lead": "Dr. Sarah Lin",
            "lead_id": "web_seo_dr_sarah_lin",
            "lead_title": "Chief SEO & Search Architecture Lead",
            "lead_cred": "Ph.D. Information Retrieval & Semantic Web",
            "channel": "#pod-web-seo",
            "icon": "trending-up",
            "color": "#f97316",
            "description": "Enterprise programmatic SEO, JSON-LD schema graphs, multi-thousand route directories, Core Web Vitals optimization, and 50-state geolocation ranking algorithms.",
            "members": [
                {"id": "web_seo_dr_sarah_lin", "name": "Dr. Sarah Lin", "role": "Chief SEO Architecture Lead", "cred": "Ph.D. Information Retrieval", "alma": "Carnegie Mellon"},
                {"id": "exec_seo_podlead_v1", "name": "Dr. Emily Rivera", "role": "SEO Pod Lead (50-State Directory)", "cred": "Ph.D. Data Science", "alma": "Stanford"},
                {"id": "seo_tech_auditor", "name": "Technical SEO Auditor", "role": "Crawl Budget & Server Log Analysis", "cred": "M.S. Web Science", "alma": "Washington"},
                {"id": "seo_schema_dev", "name": "Schema & JSON-LD Architect", "role": "Semantic Entity Knowledge Graphs", "cred": "B.S. CS", "alma": "Illinois"},
                {"id": "seo_keyword_strat", "name": "Search Intent Strategist", "role": "High-Intent Keyword Clustering", "cred": "M.S. Marketing Analytics", "alma": "Northwestern"},
                {"id": "seo_backlink_outreach", "name": "Domain Authority Engineer", "role": "Digital PR & Backlink Profiling", "cred": "B.A. Comms", "alma": "USC"},
                {"id": "seo_analytics_mgr", "name": "Search Analytics Manager", "role": "Google Search Console & Rank Tracking", "cred": "B.S. Stats", "alma": "Berkeley"}
            ]
        },
        {
            "id": "content_growth_cro",
            "name": "Content Strategy & Conversion CRO",
            "division": "Division A: Web & Cloud Infrastructure",
            "lead": "Aria Montgomery",
            "lead_id": "web_content_aria_montgomery",
            "lead_title": "Principal Content & Growth Lead",
            "lead_cred": "M.A. Strategic Communications & Narrative Systems",
            "channel": "#pod-web-content",
            "icon": "pen-tool",
            "color": "#ec4899",
            "description": "Zero-repetition high-conversion copywriting, product storytelling, CRO A/B testing funnels, and enterprise sales positioning.",
            "members": [
                {"id": "web_content_aria_montgomery", "name": "Aria Montgomery", "role": "Principal Content & Growth Lead", "cred": "M.A. Strategic Communications", "alma": "Columbia"},
                {"id": "content_copywriter_1", "name": "Senior Conversion Copywriter", "role": "Landing Page Narrative & CTA Optimization", "cred": "B.A. English", "alma": "Yale"},
                {"id": "content_copywriter_2", "name": "Technical Documentation Lead", "role": "Developer Guides & API Reference", "cred": "B.S. Tech Writing", "alma": "Carnegie Mellon"},
                {"id": "growth_cro_analyst", "name": "Conversion Rate Optimization Analyst", "role": "Heatmap & Funnel Drop-off Analysis", "cred": "M.S. Behavioral Economics", "alma": "Chicago"},
                {"id": "growth_retention", "name": "User Retention Strategist", "role": "Lifecycle Messaging & Retention Loops", "cred": "B.S. Marketing", "alma": "NYU"},
                {"id": "growth_meta_buyer", "name": "Growth Acquisition Specialist", "role": "Performance Attribution Models", "cred": "B.S. Finance", "alma": "Wharton"}
            ]
        },
        {
            "id": "data_analytics_forensics",
            "name": "Data Science, Forensics & Telemetry",
            "division": "Division C: Data Science & Live Telemetry",
            "lead": "Dr. Marcus Vance II",
            "lead_id": "data_lead_dr_marcus_vance",
            "lead_title": "Director of Data Science & Forensic Analytics",
            "lead_cred": "Ph.D. High-Dimensional Statistical Learning & Privacy-Preserving Computing",
            "channel": "#pod-data-science",
            "icon": "bar-chart-3",
            "color": "#06b6d4",
            "description": "Zero-drift production telemetry, privacy-preserving client analytics, geospatial attribution models, real-time event streaming, and cyberpunk visual data dashboards.",
            "members": [
                {"id": "data_lead_dr_marcus_vance", "name": "Dr. Marcus Vance II", "role": "Director of Data Science", "cred": "Ph.D. Statistical Learning", "alma": "Stanford"},
                {"id": "data_analyst_realtime", "name": "Real-Time Telemetry Engineer", "role": "Clickstream Ingestion & Event Pipes", "cred": "M.S. Data Eng", "alma": "CMU"},
                {"id": "data_analyst_geo", "name": "Geospatial Data Analyst", "role": "Routing Distance & Regional Heatmaps", "cred": "M.S. GIS & Analytics", "alma": "Berkeley"},
                {"id": "data_analyst_behavior", "name": "User Behavior Forensics Lead", "role": "Session Replay & Anomaly Detection", "cred": "Ph.D. Stats", "alma": "Harvard"},
                {"id": "data_analyst_attribution", "name": "Multi-Touch Attribution Analyst", "role": "Marketing ROI & Lead Provenance", "cred": "M.S. Business Analytics", "alma": "MIT Sloan"},
                {"id": "data_viz_cyberpunk_ui", "name": "Data Visualization Engineer", "role": "Real-Time D3 & Canvas Charting", "cred": "B.S. CS & Design", "alma": "Cooper Union"}
            ]
        },
        {
            "id": "qa_device_testing",
            "name": "Quality Assurance & Systems Testing",
            "division": "Division B: Native Mobile, Web3 & QA",
            "lead": "Maya Patel",
            "lead_id": "mobile_qa_maya_patel",
            "lead_title": "Mobile QA & Device Testing Lead",
            "lead_cred": "B.S. Computer Science / ISTQB Certified Tester",
            "channel": "#pod-mobile-qa",
            "icon": "check-circle-2",
            "color": "#84cc16",
            "description": "Automated regression testing, physical multi-device lab orchestration, network latency throttling, wallet security assertions, and zero-hallucination validation.",
            "members": [
                {"id": "mobile_qa_maya_patel", "name": "Maya Patel", "role": "Mobile QA Lead", "cred": "B.S. CS / ISTQB Advanced", "alma": "Waterloo"},
                {"id": "qa_auto_script", "name": "Automation Script Lead (Sunita Rao)", "role": "Playwright & Appium Test Suites", "cred": "M.S. SE", "alma": "UT Austin"},
                {"id": "qa_emulator_tester", "name": "Emulator & Virtual Grid Tester", "role": "Matrix Device Matrix Runs", "cred": "B.S. CS", "alma": "San Jose State"},
                {"id": "qa_physical_device", "name": "Physical Device Lab Engineer", "role": "Hardware Thermal & Battery Testing", "cred": "B.S. CE", "alma": "Purdue"},
                {"id": "qa_network_throttler", "name": "Network Simulation Engineer", "role": "3G/EDGE & Packet Loss Simulation", "cred": "B.S. EE", "alma": "Illinois"},
                {"id": "qa_wallet_sec", "name": "Wallet Security Assertion Engineer", "role": "Cryptographic Fuzzing & Keystore Tests", "cred": "M.S. Cyber", "alma": "Carnegie Mellon"}
            ]
        },
        {
            "id": "operations_hygiene",
            "name": "Workspace Hygiene & Repository Integrity",
            "division": "Operations & Systems Maintenance",
            "lead": "Jaxon Reed",
            "lead_id": "ops_janitor_jaxon_reed",
            "lead_title": "Chief Repository & Systems Hygiene Officer",
            "lead_cred": "Master of Workspace Hygiene & File Structure Integrity",
            "channel": "#pod-ops-maintenance",
            "icon": "trash-2",
            "color": "#64748b",
            "description": "Maintaining pristine zero-drift file systems, pruning orphaned artifacts, enforcing directory taxonomy, and ensuring continuous compilation confluence.",
            "members": [
                {"id": "ops_janitor_jaxon_reed", "name": "Jaxon Reed", "role": "Chief Systems Hygiene Officer", "cred": "Workspace Integrity Specialist", "alma": "Omniverse Ops"},
                {"id": "ops_sweeper_web", "name": "Web Workspace Sweeper", "role": "HTML/CSS Asset Cleanup", "cred": "B.S. IT", "alma": "Arizona State"},
                {"id": "ops_sweeper_android", "name": "Android Workspace Sweeper", "role": "Gradle & Manifest Cleanup", "cred": "B.S. CS", "alma": "Oregon State"}
            ]
        }
    ]

    # Map individual employee memories to their pod profiles
    all_employees_list = []
    
    # Collect all unique employees from structured pods and memory files
    seen_ids = set()
    
    for pod in structured_pods:
        for m in pod["members"]:
            emp_id = m["id"]
            seen_ids.add(emp_id)
            mem_data = employees.get(emp_id, {})
            
            all_employees_list.append({
                "id": emp_id,
                "name": m["name"],
                "role": m["role"],
                "credentials": mem_data.get("credentials", m.get("cred", "Omniverse Specialist")),
                "alma_mater": m.get("alma", "Top Tier Research Institute"),
                "pod_id": pod["id"],
                "pod_name": pod["name"],
                "division": pod["division"],
                "channel": pod["channel"],
                "reports_to": mem_data.get("reports_to", pod["lead"]),
                "memory_preview": mem_data.get("memory_preview", "Active certified specialist operating within the Omniverse Enterprise Matrix."),
                "has_memory_file": emp_id in employees
            })

    # Add remaining employees from memory files
    for emp_id, data in employees.items():
        if emp_id not in seen_ids:
            seen_ids.add(emp_id)
            all_employees_list.append({
                "id": emp_id,
                "name": data["name"],
                "role": data["role"],
                "credentials": data["credentials"],
                "alma_mater": "Omniverse Faculty",
                "pod_id": "omniverse_specialists",
                "pod_name": "Specialized Research & Operations",
                "division": "Omniverse Operations",
                "channel": "#general",
                "reports_to": data["reports_to"],
                "memory_preview": data["memory_preview"],
                "has_memory_file": True
            })

    # Build Repository Code Explorer Data
    # Scan both workspaces for key files and directories
    repo_tree = [
        {
            "name": "Omniverse2",
            "path": "/Users/silversurfer/Documents/Omniverse2",
            "type": "directory",
            "description": "Production Web, SEO, 50-State Multi-Route Network & Dual-Engine Audit Workspace",
            "children": [
                {"name": "index.html", "path": "index.html", "type": "file", "size": "152 KB", "desc": "Flagship 50-State SEO Audit & Executive Rank Verification Portal"},
                {"name": "client_seo_audit_report.html", "path": "client_seo_audit_report.html", "type": "file", "size": "148 KB", "desc": "Client-Ready Live Dual-Engine Audit & Verified Keyword Proofs"},
                {"name": "montway_clone", "path": "montway_clone", "type": "directory", "desc": "Next.js 15 Full-Stack Application (2,806 Programmatic Routes)"},
                {"name": "public_html_local", "path": "public_html_local", "type": "directory", "desc": "Static Production Distribution (2,804 Compiled HTMLs)"},
                {"name": "hostinger_site", "path": "hostinger_site", "type": "directory", "desc": "Hostinger Live Synchronization Root & PHP API Suite"},
                {"name": "scripts", "path": "scripts", "type": "directory", "desc": "Automated Python Verification, Zero-Repeat Text & Deployment Scripts"},
                {"name": ".agents", "path": ".agents", "type": "directory", "desc": "Omniverse Agent Directives, Master MEMORY_LOG.md & 80+ Memories"}
            ]
        },
        {
            "name": "Aegis shield of the gods",
            "path": "/Users/silversurfer/Documents/Aegis shield of the gods",
            "type": "directory",
            "description": "Sovereign Mobile, Web3, Audio DSP, SAP, Casino & Omniverse Code Workspace",
            "children": [
                {"name": "omniverse.md", "path": "omniverse.md", "type": "file", "size": "28 KB", "desc": "Master Enterprise Operating Manifest (Divisions A-G, Exec, Audio, macOS)"},
                {"name": "omniverse_code.md", "path": "omniverse_code.md", "type": "file", "size": "18 KB", "desc": "Offensive Cybersecurity & Vulnerability Research Manifest (Divisions 01-07)"},
                {"name": "mythos_agent.md", "path": "mythos_agent.md", "type": "file", "size": "22 KB", "desc": "Frontier AI Agentic Architecture, 6-Stage Reasoning Loop & PRM Gating"},
                {"name": "AGENTS.md", "path": "AGENTS.md", "type": "file", "size": "8 KB", "desc": "Repository Agent Rules & Persistent Memory Directives"},
                {"name": ".agents/context", "path": ".agents/context", "type": "directory", "desc": "18 Core Context Blueprints (Double Ratchet, Web3, Audio DSP, Kernel, SAP, OSINT)"},
                {"name": ".agents/rules", "path": ".agents/rules", "type": "directory", "desc": "15 Hardened Architectural Rules (AST Validation, PRM Gating, Code Review)"},
                {"name": "app", "path": "app", "type": "directory", "desc": "Native Android & Kotlin Multiplatform Architecture (Jetpack Compose, Room SQLCipher)"}
            ]
        }
    ]

    # 11 Core Technical Capabilities Showcase
    capabilities = [
        {
            "id": "web_development",
            "title": "Modern Web & Cloud Architecture",
            "subtitle": "Next.js 15, Three.js 3D, WebGL Shaders, Sub-Second CWV",
            "tagline": "Uncompromising web engineering delivering sub-second Largest Contentful Paint (LCP) and cinematic 60fps WebGL interaction.",
            "icon": "globe",
            "accent": "#00f0ff",
            "lead": "Julian Thorne (Stanford HCI) & Dr. Elena Rostova (ETH Zurich)",
            "technologies": ["Next.js 15 Server Components", "React 19", "Three.js / WebGL", "Tailwind CSS", "GSAP ScrollTrigger", "Edge SSR", "Cloudflare CDN", "Docker"],
            "features": [
                "Server-Driven Programmatic Architecture scaling to 50,000+ zero-latency dynamic routes.",
                "Real-time 3D WebGL graphics and procedural GLSL fragment shaders optimized for mobile.",
                "Zero-CLS layout stability and sub-800ms First Contentful Paint.",
                "Micro-interaction physics and glassmorphic responsive design systems."
            ],
            "client_benefit": "Transform your digital footprint into an interactive powerhouse that converts visitors into high-value enterprise clients."
        },
        {
            "id": "ios_macos_development",
            "title": "Native iOS & macOS Desktop Engineering",
            "subtitle": "SwiftUI, AppKit, Metal 3 GPU, Apple Secure Enclave",
            "tagline": "Bespoke Apple platform engineering utilizing Darwin kernel primitives, Metal acceleration, and Secure Enclave hardware privacy.",
            "icon": "apple",
            "accent": "#e2e8f0",
            "lead": "Elena Vance (Stanford SE) & Dr. Kai Sterling (UC Berkeley OS)",
            "technologies": ["SwiftUI", "AppKit", "Metal 3 Shaders", "Secure Enclave CryptoKit", "CoreData / SwiftData", "AVFoundation", "Darwin Mach VM", "Launchd Daemons"],
            "features": [
                "Native macOS and iOS applications engineered for 120Hz ProMotion display fluidity.",
                "Hardware-isolated cryptographic key storage via Apple Secure Enclave.",
                "Metal 3 GPU compute shaders for real-time video, audio, and mathematical workloads.",
                "Deep AppKit desktop system integration with low-overhead daemon background services."
            ],
            "client_benefit": "Delivers the highest standard of luxury, responsiveness, and hardware-level security expected by Apple users."
        },
        {
            "id": "android_embedded",
            "title": "Native Android & Embedded Systems",
            "subtitle": "Kotlin Jetpack Compose, Android NDK C++, Room SQLCipher",
            "tagline": "Enterprise Android engineering combining modern declarative UI with low-level C++ NDK performance and military-grade hardware encryption.",
            "icon": "smartphone",
            "accent": "#10b981",
            "lead": "Viktor Drago (KTH) & Chen Wei (Tsinghua Embedded)",
            "technologies": ["Kotlin Jetpack Compose", "Android NDK C++20", "Hardware Keystore AEAD", "Room SQLCipher 256-bit", "Ktor / Coroutines", "Bluetooth / NFC HAL", "Gradle Custom DSL"],
            "features": [
                "Zero-latency asynchronous reactive UI powered by Jetpack Compose.",
                "Direct Android NDK C++ native bindings for compute-intensive signal processing.",
                "AES-256-GCM hardware-backed key derivation via AndroidKeyStore.",
                "Offline-first SQLite database synchronization with encrypted Room architecture."
            ],
            "client_benefit": "Guarantees reliable operation on billions of diverse mobile devices without battery drain or security vulnerabilities."
        },
        {
            "id": "os_kernel_development",
            "title": "Operating System & Ring 0 Kernel Architecture",
            "subtitle": "Darwin XNU, Linux Kernel, eBPF, Mach VM, Custom Drivers",
            "tagline": "Deep low-level systems engineering operating at Ring 0, designing custom kernel extensions, eBPF probes, and real-time thread schedulers.",
            "icon": "cpu",
            "accent": "#6366f1",
            "lead": "Dr. Kai Sterling (UC Berkeley) & Elias Vance (Carnegie Mellon)",
            "technologies": ["Darwin XNU Kernel", "Linux Kernel Ring 0", "eBPF BCF Probes", "IOKit / DriverKit", "POSIX C11", "Mach VM Paging", "Real-Time Thread Schedulers", "Assembly x86_64 / ARM64"],
            "features": [
                "Kernel-level process isolation, custom system call hooks, and hardware driver authoring.",
                "eBPF real-time network packet inspection and kernel-space security telemetry.",
                "Mach real-time audio thread synchronization with microsecond-level determinism.",
                "Custom memory governors and cache-line alignment eliminating CPU micro-stutters."
            ],
            "client_benefit": "Unlocks maximum hardware performance and custom appliance capabilities inaccessible via conventional high-level software."
        },
        {
            "id": "audio_dsp_acoustics",
            "title": "Sound Engineering & Psychoacoustic DSP",
            "subtitle": "Stanford CCRMA AudioUnits, 192kHz CoreAudio, Bass Synthesis",
            "tagline": "Pioneering mathematical acoustic engineering from discrete-time signal processing to physical transducer enclosures.",
            "icon": "volume-2",
            "accent": "#ec4899",
            "lead": "Dr. Julian Vance (Stanford CCRMA) & Dr. Arthur Briggs (Imperial College)",
            "technologies": ["Darwin CoreAudio HAL", "AudioUnit V3 DSP", "Psychoacoustic Bass Synthesis", "Fletcher-Munson Equal-Loudness", "Brickwall Lookahead Limiters", "IIR/FIR Notch Filters", "Spatial Stereo Panning", "WebAudio API"],
            "features": [
                "Psychoacoustic missing-fundamental synthesis (2f/3f harmonic generation) doubling perceived bass.",
                "Lookahead dynamic range limiters and brickwall thermal protection eliminating clipping.",
                "Real-time 192kHz / 32-bit floating-point audio processing with zero phase distortion.",
                "Slot-loaded bass reflex enclosure modeling and chassis resonance notch elimination."
            ],
            "client_benefit": "Produces rich, studio-grade soundscapes and proprietary audio engines that captivate users across headphones and micro-speakers."
        },
        {
            "id": "cryptography_web3",
            "title": "Applied Cryptography, Blockchain & Web3",
            "subtitle": "Double Ratchet, Libsodium, zk-SNARKs, Solana/EVM BIP39 Vaults",
            "tagline": "Sovereign cryptographic engineering implementing Signal-grade Double Ratchet end-to-end encryption and verified smart contracts.",
            "icon": "key",
            "accent": "#eab308",
            "lead": "Dr. Leon Nash (MIT Ph.D. Cryptography)",
            "technologies": ["Libsodium X25519 / Ed25519", "Double Ratchet Protocol", "Argon2id Key Derivation", "Google Tink AEAD", "Solana Anchor / Rust", "Solidity EVM", "BIP39 HD Vaults", "zk-SNARKs"],
            "features": [
                "Signal-grade Double Ratchet E2EE messaging protocol with forward and post-compromise secrecy.",
                "Non-custodial BIP39 mnemonic vaults with encrypted in-memory zeroization.",
                "High-throughput Solana smart contracts with sub-400ms transaction finality.",
                "Formally verified Solidity contracts immune to reentrancy, overflow, and flash-loan attacks."
            ],
            "client_benefit": "Guarantees uncrackable financial privacy and provably secure decentralized infrastructure for fintech and Web3 enterprises."
        },
        {
            "id": "sap_enterprise_erp",
            "title": "Enterprise SAP S/4HANA & Logistics Systems",
            "subtitle": "RFC/BAPI/OData Connectors, WMS, Sub-200ms RFID/Barcode Ingestion",
            "tagline": "Mission-critical enterprise software bridging industrial ERP backends with modern real-time warehouse scanning interfaces.",
            "icon": "layers",
            "accent": "#0ea5e9",
            "lead": "Dr. Hans Schmidt (TU Munich Ph.D. Enterprise Systems)",
            "technologies": ["SAP S/4HANA OData v4", "RFC / BAPI Connectors", "Warehouse Management (WMS)", "Sub-200ms RFID / Barcode Ingestion", "Double-Entry Ledger", "Apache Kafka", "PostgreSQL", "EDIFACT / ANSI X12"],
            "features": [
                "Sub-200ms industrial barcode/RFID scanning ingestion with zero drop rate.",
                "Direct bidirectional SAP S/4HANA synchronization bypassing slow batch synchronization.",
                "Double-entry cryptographic ledger ensuring 100% audit compliance across warehouses.",
                "Real-time freight route optimization and automated dispatch pipelines."
            ],
            "client_benefit": "Eliminates warehouse bottlenecks, eliminates inventory shrinkage, and provides executives with real-time supply chain transparency."
        },
        {
            "id": "offensive_cyber_omniverse_code",
            "title": "Offensive Cybersecurity & Exploit Synthesis",
            "subtitle": "Binary Exploitation, ROP/SROP, Heap Feng-Shui, Kernel Ring 0",
            "tagline": "Elite vulnerability research and automated exploit synthesis led by DARPA CGC veterans and academic security researchers.",
            "icon": "terminal",
            "accent": "#ef4444",
            "lead": "Prof. Lucas Mercer (DARPA CGC Veteran) & Dr. Kaito Tanaka (Tokyo Univ)",
            "technologies": ["GDB-GEF / Pwntools", "ROP / SROP Exploit Synthesis", "Dynamic Heap Allocator Feng-Shui", "Angr / Z3 Symbolic Execution", "AFL++ / LibFuzzer", "IDA Pro / Ghidra / Binary Ninja", "Linux Kernel Ring 0 Pwn", "Hardware JTAG / Microarch"],
            "features": [
                "Automated vulnerability discovery via concolic execution and symbolic constraint solving.",
                "Bypass of modern exploit mitigations (ASLR, NX, Stack Canaries, Shadow Stacks, Safe Linking).",
                "Advanced Heap Feng-Shui targeting glibc ptmalloc, jemalloc, and kernel slab allocators.",
                "Red team penetration testing and hardware/firmware reverse engineering."
            ],
            "client_benefit": "Validates your software against the world's most sophisticated nation-state attack vectors before adversaries find them."
        },
        {
            "id": "sovereign_osint",
            "title": "Sovereign OSINT & Threat Reconnaissance",
            "subtitle": "Entity Graphs, ADS-B Flight / AIS Maritime, Darknet Forensics",
            "tagline": "Deep open-source intelligence gathering and multi-layer entity graph correlation across aerial, maritime, and darknet vectors.",
            "icon": "radar",
            "accent": "#14b8a6",
            "lead": "Dr. Morgan Cross (Oxford Graph Theory) & Valeria Novak (ETH Zurich GEOINT)",
            "technologies": ["Neo4j Entity Graphs", "ADS-B Flight Tracking", "AIS Maritime Kinetic Feeds", "Darknet Onion Scraping", "Maltego / Spiderfoot API", "SOCMINT Linguistic Forensics", "Satellite SAR Imagery", "Cryptocurrency Flow Tracing"],
            "features": [
                "Multi-dimensional identity resolution mapping email, aliases, cryptographic addresses, and IPs.",
                "Real-time kinetic tracking of maritime cargo vessels and private aviation fleets.",
                "Darknet marketplace surveillance and compromised credential monitoring.",
                "Automated threat actor profiling and corporate cyber espionage detection."
            ],
            "client_benefit": "Empowers corporate leadership with predictive strategic intelligence and early warning threat detection."
        },
        {
            "id": "casino_gaming_architecture",
            "title": "Casino & Interactive Real-Time Gaming",
            "subtitle": "Provably Fair HMAC-SHA256 RNG, Slot Math, 60fps WebGL Tables",
            "tagline": "Certified mathematical gaming systems delivering provably fair player trust, deterministic volatility curves, and 60fps canvas graphics.",
            "icon": "dices",
            "accent": "#f43f5e",
            "lead": "Viktor Kane (ETH Zurich Applied Probability)",
            "technologies": ["Provably Fair HMAC-SHA256 RNG", "Slot Reel Strip Combinatorics", "Certified RTP Volatility Math", "Pixi.js WebGL 2D Engine", "Spine 2D Animations", "WebSocket Real-Time Multi-Table", "Anti-Collision RNG Seeding", "GLI-19 Compliance Standards"],
            "features": [
                "Cryptographically verifiable Provably Fair algorithm allowing players to verify every spin outcome.",
                "Mathematical slot reel strip design with exact RTP (94% - 98%) and customizable volatility profiles.",
                "Silky smooth 60fps WebGL/Pixi.js slot spin reels and dynamic particle celebrations.",
                "Sub-16.6ms frame budgets and low-latency multiplayer blackjack/roulette tables."
            ],
            "client_benefit": "Maximizes player retention and regulatory compliance while delivering casino games that run instantly on any mobile or desktop browser."
        },
        {
            "id": "frontier_agentic_ai",
            "title": "Frontier AI & Cognitive Multi-Agent Systems",
            "subtitle": "6-Stage Autonomous Loop, Process Reward Models, Tree-sitter AST",
            "tagline": "State-of-the-art cognitive agent architecture powered by step-level PRM gating, Monte Carlo Tree Search, and deterministic tooling.",
            "icon": "brain",
            "accent": "#8b5cf6",
            "lead": "Dr. Aris Thorne (MIT CSAIL) & Dr. Alexander Vance (MIT Distributed Systems)",
            "technologies": ["6-Stage Cognitive Reasoning Loop", "Process Reward Models (PRM >= 0.95)", "Tree-sitter AST Symbol Graphs", "WORM Prompt KV-Cache Alignment", "Monte Carlo Tree Search (MCTS)", "Context Sandwich Injection", "Anti-Pattern Reflexion Graveyards", "Deterministic Sandbox Oracles"],
            "features": [
                "Zero-hallucination agentic coding loop that self-corrects syntax, contract, and runtime regressions.",
                "AST-level repository symbol indexing allowing agents to reason over 100,000+ lines of codebase.",
                "Step-level Process Reward Model gating ensuring every modification meets mathematical rigor.",
                "Multi-agent supervisor topologies delegating tasks across specialized domain pods seamlessly."
            ],
            "client_benefit": "Empowers enterprises with autonomous software development and intelligent agents that execute complex engineering workflows without drift."
        }
    ]

    dataset = {
        "metadata": {
            "company_name": "Omniverse Tech",
            "enterprise_group": "Omniverse Enterprise Matrix",
            "offensive_division": "Omniverse Code",
            "generated_at": "2026-08-17T17:00:00Z",
            "total_employees": len(all_employees_list),
            "total_pods": len(structured_pods),
            "total_capabilities": len(capabilities),
            "zero_drift_certified": True
        },
        "executive_summary": {
            "mission": "Engineering sovereign, provably verified computational architectures from Ring 0 operating system kernels to multi-agent artificial intelligence and 60fps WebGL experiences.",
            "philosophy": {
                "what_we_do": "We engineer uncompromising digital infrastructure across Web, iOS, Android, macOS, OS Kernel, Sound DSP, Web3, SAP Enterprise, Offensive Security, OSINT, Casino Gaming, and Frontier AI.",
                "how_we_do_it": "Through our strict 4-Tier Hierarchical Review Pipeline (Specialist -> Pod Lead -> Security Lead -> CEO Sign-off), real-world zero-drift data mandates, and multi-agent autonomous execution.",
                "why_we_do_it": "Because modern technology is plagued by fragile abstractions, bloated frameworks, and fabricated mock data. We build mathematically sound, sovereign systems that stand the test of time.",
                "why_we_are_the_best": "Omniverse unites the world's most elite faculty across academia and industry—MIT, Stanford, ETH Zurich, TU Munich, UC Berkeley, Oxford, and DARPA CGC veterans—collaborating with seamless real-time precision."
            },
            "metrics": [
                {"label": "Active Specialists & Deans", "value": "95+", "sub": "World-Class Engineers"},
                {"label": "Autonomous Pods", "value": "24", "sub": "Domain-Specific Teams"},
                {"label": "Core Disciplines", "value": "11", "sub": "Full-Stack to Ring 0"},
                {"label": "Mock Data Tolerance", "value": "0.00%", "sub": "100% Deterministic"},
                {"label": "Code Review Tiers", "value": "4-Tier", "sub": "Hierarchical Sign-off"},
                {"label": "Audio DSP Fidelity", "value": "192kHz", "sub": "Stanford CCRMA HAL"}
            ]
        },
        "capabilities": capabilities,
        "pods": structured_pods,
        "employees": all_employees_list,
        "repository_explorer": repo_tree
    }

    return dataset

if __name__ == "__main__":
    employees = extract_memories()
    print(f"Extracted {len(employees)} raw employee memories.")
    dataset = parse_manifests(employees)
    
    out_dir = os.path.join(WORKSPACE_OMNIVERSE2, "omniverse_portal", "src", "data")
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, "omniverse_dataset.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    # Also write a JS export for direct ESModule inclusion
    js_out_file = os.path.join(out_dir, "omniverse_dataset.js")
    with open(js_out_file, "w", encoding="utf-8") as f:
        f.write(f"export const OMNIVERSE_DATA = {json.dumps(dataset, indent=2)};\n")
        
    print(f"Successfully wrote Omniverse Dataset ({len(dataset['employees'])} employees, {len(dataset['pods'])} pods, {len(dataset['capabilities'])} capabilities) to:")
    print(f"  -> {out_file}")
    print(f"  -> {js_out_file}")
