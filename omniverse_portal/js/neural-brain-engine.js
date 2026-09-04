/* ==========================================================================
   OMNIVERSE TECH — 86-BILLION HUMAN BRAIN 3D CORTEX & PINEAL CORE ENGINE
   Physiologically Accurate Human Connectome: 10 Anatomical Cortexes & Structures
   ========================================================================== */

import { LOBE_DOMAINS, tokenStream } from './neural-token-stream.js';
import { neuralAudio } from './neural-audio-synth.js';

export class NeuralBrainObservatory {
  constructor(canvasContainerId) {
    this.container = document.getElementById(canvasContainerId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2(-999, -999);

    // Biological Scale & Viewport Simulation Parameters
    this.biologicalNeuronCount = 86000000000; // 86 Billion
    this.biologicalSynapseCount = 100000000000000; // 100 Trillion
    this.neuronCount = 16384; // GPU Viewport Particles (Default 16K, up to 65K)
    this.synapseCount = 32768; // Active GPU Synaptic Fibers
    this.activePulsesCount = 384;
    this.simulationSpeed = 1.0;
    this.isPaused = false;
    this.currentTopology = 'ANATOMICAL_BRAIN'; // ANATOMICAL_BRAIN | TRANSFORMER_STACK | AGENT_SWARM | ATTENTION_HEATMAP

    // Data Structures
    this.neurons = [];
    this.synapses = [];
    this.actionPulses = [];
    this.selectedNeuron = null;
    this.hoveredNeuron = null;

    // Three.js Render Objects
    this.brainGroup = new THREE.Group();
    this.pinealMesh = null;
    this.pinealAura = null;
    this.callosumLines = null;
    this.neuronPoints = null;
    this.synapseLines = null;
    this.pulsePoints = null;
    this.selectionHighlight = null;
    this.aethelRayGroup = null;
    this.aethelRayParticles = [];

    // Camera Flight Animation
    this.isFlyingCamera = false;
    this.camTargetPos = new THREE.Vector3();
    this.camTargetLook = new THREE.Vector3();

    // Telemetry & Lobe stats
    this.lobeStats = {};
    Object.keys(LOBE_DOMAINS).forEach(k => {
      this.lobeStats[k] = { active: 0, total: 0, firingRate: 0 };
    });

    // Oscilloscope buffer
    this.oscData = new Float32Array(100);
    this.oscCanvas = document.getElementById('osc-canvas');
    this.oscCtx = this.oscCanvas ? this.oscCanvas.getContext('2d') : null;

    this.clock = new THREE.Clock();
    this.init();
  }

  init() {
    if (!this.container) return;

    // 1. Scene & Fog
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x030508, 0.0011);

    // 2. Camera
    const aspect = window.innerWidth / window.innerHeight;
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.5, 4000);
    this.camera.position.set(0, 130, 520);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor(0x030508, 1);
    this.container.appendChild(this.renderer.domElement);

    // 4. Orbit Controls
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.minDistance = 15;
      this.controls.maxDistance = 1600;
      this.controls.autoRotate = false;
    }

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(0x0a152e, 1.4);
    this.scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x00f0ff, 1.8);
    dirLight1.position.set(300, 400, 200);
    this.scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xa855f7, 1.4);
    dirLight2.position.set(-300, -200, -200);
    this.scene.add(dirLight2);

    const goldCoreLight = new THREE.PointLight(0xfbbf24, 2.5, 250);
    goldCoreLight.position.set(0, 0, -10);
    this.brainGroup.add(goldCoreLight);

    this.scene.add(this.brainGroup);

    // 6. Build Human Connectome Architecture
    this.buildPinealGlandCore();
    this.generateNeuralTopologies();
    this.buildSynapticConnectome();
    this.buildActionPotentialPulses();
    this.buildSelectionHighlight();
    this.buildCosmicBackground();
    this.buildAethelGeodesicRay();

    // 7. Live 12D Synaptic Telemetry Stream
    this.initLiveSynapticStream();

    // 8. Event Listeners
    this.initEventListeners();

    // 9. Select Pineal Gland or Default Frontal
    if (this.neurons.length > 0) {
      const pinealNeuron = this.neurons.find(n => n.lobe === 'PINEAL') || this.neurons[0];
      this.selectNeuron(pinealNeuron, false);
    }

    // 10. Start Render Loop
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  initLiveSynapticStream() {
    this.liveSynapsesTelemetry = {
      global_energy_level: 0.3013,
      active_node_count: 20,
      total_synapses: 29
    };

    const fetchTelemetry = async () => {
      try {
        const resp = await fetch('data/neural_synapses.json?t=' + Date.now());
        if (resp.ok) {
          const data = await resp.json();
          this.liveSynapsesTelemetry = data;
          this.updateLiveHeaderTelemetry(data);
        }
      } catch (err) {
        // Fallback gracefully
      }
    };

    fetchTelemetry();
    setInterval(fetchTelemetry, 2500);
  }

  updateLiveHeaderTelemetry(data) {
    const liveInd = document.querySelector('.live-indicator');
    if (liveInd && data) {
      const energyPct = ((data.global_energy_level || 0.30) * 100).toFixed(1);
      liveInd.innerHTML = `<span class="pulse-dot" style="background:#00f0ff; box-shadow:0 0 12px #00f0ff;"></span><span>12D LIVE SYNAPTIC FLUX: ${energyPct}% • ${data.active_node_count || 20} ACTIVE MANIFOLDS</span>`;
    }
  }

  // =========================================================================
  // 1. PINEAL GLAND QUANTUM CORE (432Hz HARMONIC SINGULARITY)
  // =========================================================================
  buildPinealGlandCore() {
    const coreGeo = new THREE.SphereGeometry(7, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0xfbbf24,
      wireframe: false
    });
    this.pinealMesh = new THREE.Mesh(coreGeo, coreMat);
    this.pinealMesh.position.set(0, 5, -12); // Anatomical epithalamic core
    this.brainGroup.add(this.pinealMesh);

    // Golden Coronal Aura
    const auraGeo = new THREE.SphereGeometry(14, 24, 24);
    const auraMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.35
    });
    this.pinealAura = new THREE.Mesh(auraGeo, auraMat);
    this.pinealAura.position.copy(this.pinealMesh.position);
    this.brainGroup.add(this.pinealAura);
  }

  // =========================================================================
  // 2. PARAMETRIC 86-BILLION HUMAN BRAIN TOPOLOGY GENERATION
  // =========================================================================
  generateNeuralTopologies() {
    this.neurons = [];
    const positions = new Float32Array(this.neuronCount * 3);
    const colors = new Float32Array(this.neuronCount * 3);
    const sizes = new Float32Array(this.neuronCount);

    const radius = 180;
    const lobeKeys = Object.keys(LOBE_DOMAINS);

    for (let i = 0; i < this.neuronCount; i++) {
      const phi = Math.acos(-1 + (2 * i) / this.neuronCount);
      const theta = Math.sqrt(this.neuronCount * Math.PI) * phi;
      const hemisphere = i % 2 === 0 ? 1 : -1;
      const fissureGap = 14;

      // Realistic Cortical Gyri & Sulci Fold Modulation
      const fold = 1.0 +
        0.15 * Math.sin(9 * theta) * Math.cos(7 * phi) +
        0.09 * Math.cos(15 * phi) * Math.sin(11 * theta) +
        0.04 * Math.sin(22 * theta + 18 * phi);

      let rx = radius * 0.84 * Math.sin(phi) * Math.cos(theta) * fold;
      let ry = radius * 0.74 * Math.sin(phi) * Math.sin(theta) * fold;
      let rz = radius * 1.18 * Math.cos(phi) * fold;

      // Anatomical Shape Modulation
      if (rz > 0) {
        rx *= 1.06;
        ry *= 1.03;
      } else {
        rx *= 0.93;
        if (ry < 0) ry *= 1.18;
      }

      let anatomicalX = rx + (hemisphere * fissureGap);
      let anatomicalY = ry;
      let anatomicalZ = rz;

      // Classify into 10 Human Anatomical Regions
      let lobeKey = 'FRONTAL';
      const distFromCenter = Math.sqrt(rx * rx + ry * ry + rz * rz);

      if (distFromCenter < 22 && Math.abs(rz + 10) < 18) {
        // Exact Epithalamus / Pineal Gland Core
        lobeKey = 'PINEAL';
        anatomicalX = (Math.random() - 0.5) * 16;
        anatomicalY = 5 + (Math.random() - 0.5) * 14;
        anatomicalZ = -12 + (Math.random() - 0.5) * 16;
      } else if (Math.abs(anatomicalX) < 28 && anatomicalY > 10 && anatomicalY < 45 && anatomicalZ > -50 && anatomicalZ < 40) {
        // Corpus Callosum Inter-Hemispheric Arch
        lobeKey = 'CALLOSUM';
        anatomicalY = 22 + Math.sin((anatomicalZ + 50) / 90 * Math.PI) * 18;
      } else if (distFromCenter < radius * 0.38 && Math.abs(anatomicalY) < 30) {
        // Thalamus & Hypothalamus
        lobeKey = 'THALAMUS';
      } else if (distFromCenter < radius * 0.48 && anatomicalY < 0) {
        // Limbic System & Hippocampus
        lobeKey = 'LIMBIC';
      } else if (Math.abs(anatomicalX) > 60 && Math.abs(anatomicalX) < 100 && anatomicalY > -20 && anatomicalY < 30 && anatomicalZ > -25 && anatomicalZ < 35) {
        // Central Cortex / Insular Lobe (Deep Lateral Sulcus)
        lobeKey = 'INSULA';
      } else if (anatomicalY < -75 && anatomicalZ < -20) {
        // Cerebellum & Arbor Vitae
        lobeKey = 'CEREBELLUM';
      } else if (anatomicalZ > 30) {
        // Frontal Cortex
        lobeKey = 'FRONTAL';
      } else if (anatomicalZ < -65) {
        // Occipital Cortex
        lobeKey = 'OCCIPITAL';
      } else if (Math.abs(anatomicalX) > 85 && anatomicalY < 15) {
        // Temporal Cortex
        lobeKey = 'TEMPORAL';
      } else {
        // Parietal Cortex
        lobeKey = 'PARIETAL';
      }

      const domain = LOBE_DOMAINS[lobeKey];

      // Transformer Stack Layout Coordinates
      const layerIndex = Math.floor((i / this.neuronCount) * 24);
      const row = i % 16;
      const col = Math.floor((i % 256) / 16);
      const transformerX = (col - 7.5) * 26;
      const transformerY = (row - 7.5) * 24;
      const transformerZ = (layerIndex - 12) * 34;

      // Agent Swarm Pod Layout Coordinates
      const swarmClusterIndex = lobeKeys.indexOf(lobeKey);
      const swarmAngle = (swarmClusterIndex / lobeKeys.length) * Math.PI * 2;
      const swarmCenter = new THREE.Vector3(
        Math.cos(swarmAngle) * 240,
        Math.sin((i % 7) * 0.9) * 70,
        Math.sin(swarmAngle) * 240
      );
      const clusterPhi = (i % 64) * 0.2;
      const clusterR = 55 + (i % 30);
      const swarmX = swarmCenter.x + Math.sin(clusterPhi) * Math.cos(i) * clusterR;
      const swarmY = swarmCenter.y + Math.sin(clusterPhi) * Math.sin(i) * clusterR;
      const swarmZ = swarmCenter.z + Math.cos(clusterPhi) * clusterR;

      // =====================================================================
      // 12-DIMENSIONAL BIOLOGICAL QUANTUM DREAMSCAPE (DNA, TELOMERES, MITOCHONDRIA)
      // =====================================================================
      let calabiX, calabiY, calabiZ;
      let bioType = 'DNA_STRAND';
      let bioCodon = 'AUG';
      let bioDetail = 'Genetic Memory Base';

      if (i < 10500) {
        // 1. DNA DOUBLE HELIX & BASE-PAIR HYDROGEN BRIDGES (Adenine, Thymine, Guanine, Cytosine)
        const t = i / 10500.0;
        const yCoord = -320.0 + t * 640.0;
        const xCenter = 35.0 * Math.sin(t * Math.PI * 2.0);
        const zCenter = 25.0 * Math.cos(t * Math.PI * 2.0);
        const theta = t * Math.PI * 18.0; // 9 full helical turns
        const helixR = 78.0 + 12.0 * Math.sin(t * Math.PI * 6.0);

        const mod4 = i % 4;
        if (mod4 === 0) {
          // Strand A: Sugar-Phosphate Backbone 1 (Neon Cyan & Gold)
          calabiX = xCenter + helixR * Math.cos(theta);
          calabiY = yCoord;
          calabiZ = zCenter + helixR * Math.sin(theta);
          bioType = 'DNA_STRAND_A';
          bioCodon = ['TAC', 'GAG', 'CTC', 'AAG'][i % 4];
          bioDetail = 'DNA Strand Alpha (Sugar-Phosphate Backbone)';
        } else if (mod4 === 1) {
          // Strand B: Sugar-Phosphate Backbone 2 (Hyper-Violet & Emerald)
          calabiX = xCenter + helixR * Math.cos(theta + Math.PI);
          calabiY = yCoord;
          calabiZ = zCenter + helixR * Math.sin(theta + Math.PI);
          bioType = 'DNA_STRAND_B';
          bioCodon = ['ATG', 'CTC', 'GAG', 'TTC'][i % 4];
          bioDetail = 'DNA Strand Beta (Anti-Parallel Epigenetic Backbone)';
        } else if (mod4 === 2) {
          // Adenine-Thymine (A-T) Double Hydrogen Bond Bridge
          const frac = (i % 16) / 15.0;
          calabiX = xCenter + helixR * Math.cos(theta) * (1.0 - frac) + helixR * Math.cos(theta + Math.PI) * frac;
          calabiY = yCoord + (Math.sin(i * 0.7) * 2.5);
          calabiZ = zCenter + helixR * Math.sin(theta) * (1.0 - frac) + helixR * Math.sin(theta + Math.PI) * frac;
          bioType = 'BASE_PAIR_AT';
          bioCodon = 'A-T Bond';
          bioDetail = 'Adenine = Thymine Hydrogen Bridge (2.8 Å Bond)';
        } else {
          // Guanine-Cytosine (G-C) Triple Hydrogen Bond Bridge
          const frac = (i % 16) / 15.0;
          calabiX = xCenter + helixR * Math.cos(theta) * (1.0 - frac) + helixR * Math.cos(theta + Math.PI) * frac;
          calabiY = yCoord + (Math.cos(i * 0.7) * 2.5);
          calabiZ = zCenter + helixR * Math.sin(theta) * (1.0 - frac) + helixR * Math.sin(theta + Math.PI) * frac;
          bioType = 'BASE_PAIR_GC';
          bioCodon = 'G-C Bond';
          bioDetail = 'Guanine ≡ Cytosine Triple Bond (High-Stability Core)';
        }
      } else if (i < 13000) {
        // 2. TELOMERE PROTECTIVE CORONA ENDCAPS (T-Loop Structures)
        const tIdx = i - 10500;
        const isTop = tIdx < 1250;
        const localIdx = isTop ? tIdx : (tIdx - 1250);

        const rTelo = 42.0 * Math.sqrt(localIdx / 1250.0) + 12.0 * Math.sin(i * 0.3);
        const thetaTelo = localIdx * 2.39996; // Golden Angle Spiral
        const phiTelo = (localIdx / 1250.0) * Math.PI;

        if (isTop) {
          calabiX = 35.0 * Math.sin(Math.PI * 2.0) + rTelo * Math.sin(phiTelo) * Math.cos(thetaTelo);
          calabiY = 320.0 + 80.0 * Math.cos(phiTelo) + 16.0 * Math.sin(i * 0.4);
          calabiZ = 25.0 * Math.cos(Math.PI * 2.0) + rTelo * Math.sin(phiTelo) * Math.sin(thetaTelo);
          bioType = 'TELOMERE_NORTH';
          bioCodon = 'TTAGGG-N';
          bioDetail = 'North Telomere Cap (T-Loop Hexanucleotide Shield)';
        } else {
          calabiX = 35.0 * Math.sin(0.0) + rTelo * Math.sin(phiTelo) * Math.cos(thetaTelo);
          calabiY = -320.0 - 80.0 * Math.cos(phiTelo) - 16.0 * Math.sin(i * 0.4);
          calabiZ = 25.0 * Math.cos(0.0) + rTelo * Math.sin(phiTelo) * Math.sin(thetaTelo);
          bioType = 'TELOMERE_SOUTH';
          bioCodon = 'TTAGGG-S';
          bioDetail = 'South Telomere Cap (Epigenetic Longevity Anchor)';
        }
      } else {
        // 3. MITOCHONDRIAL CRISTAE & BIO-ENERGETIC MEMBRANE MATRICES (4 Power Centers)
        const mIdx = i - 13000;
        const mitoId = Math.floor(mIdx / 846);
        const signX = (mitoId % 2 === 0 ? 1.0 : -1.0);
        const signY = (mitoId < 2 ? 1.0 : -1.0);
        const signZ = (mitoId === 1 || mitoId === 2 ? 1.0 : -1.0);

        const cx = signX * 195.0;
        const cy = signY * 120.0;
        const cz = signZ * 145.0;

        const uM = ((mIdx % 846) / 846.0) * Math.PI * 2.0;
        const vM = (((mIdx * 7) % 846) / 846.0) * Math.PI;
        const cristaeFold = 1.0 + 0.42 * Math.sin(8.0 * uM) * Math.cos(4.0 * vM);

        calabiX = cx + 62.0 * Math.sin(vM) * Math.cos(uM) * cristaeFold;
        calabiY = cy + 38.0 * Math.cos(vM) * cristaeFold;
        calabiZ = cz + 48.0 * Math.sin(vM) * Math.sin(uM) * cristaeFold;
        bioType = 'MITOCHONDRIA_CRISTAE';
        bioCodon = "ATP-M" + (mitoId + 1);
        bioDetail = "Mitochondrial Cristae Node #" + (mitoId + 1) + " (432Hz ATP Flux)";
      }

      const baseColor = new THREE.Color(domain.colorHex);
      const activeColor = new THREE.Color(0xffffff).lerp(baseColor, 0.35);

      const neuron = {
        index: i,
        id: `NEURON-${lobeKey.substring(0, 4)}-${String(i).padStart(5, '0')}`,
        lobe: lobeKey,
        domain: domain,
        hemisphere: hemisphere === 1 ? 'Right' : 'Left',
        layer: 1 + (i % 6),
        currentPos: new THREE.Vector3(anatomicalX, anatomicalY, anatomicalZ),
        anatomicalPos: new THREE.Vector3(anatomicalX, anatomicalY, anatomicalZ),
        transformerPos: new THREE.Vector3(transformerX, transformerY, transformerZ),
        swarmPos: new THREE.Vector3(swarmX, swarmY, swarmZ),
        calabiYauPos: new THREE.Vector3(calabiX, calabiY, calabiZ),
        bioType: bioType,
        bioCodon: bioCodon,
        bioDetail: bioDetail,
        targetPos: new THREE.Vector3(anatomicalX, anatomicalY, anatomicalZ),
        activation: lobeKey === 'PINEAL' ? 0.95 : (0.05 + Math.random() * 0.25),
        baseActivation: lobeKey === 'PINEAL' ? 0.95 : (0.05 + Math.random() * 0.1),
        firingState: false,
        refractoryTimer: 0,
        oscillationSpeed: lobeKey === 'PINEAL' ? 4.32 : (1.5 + Math.random() * 3.5),
        oscillationPhase: Math.random() * Math.PI * 2,
        baseColor: baseColor,
        activeColor: activeColor,
        currentColor: baseColor.clone(),
        synapsesIn: [],
        synapsesOut: []
      };

      this.neurons.push(neuron);

      positions[i * 3] = anatomicalX;
      positions[i * 3 + 1] = anatomicalY;
      positions[i * 3 + 2] = anatomicalZ;

      colors[i * 3] = baseColor.r;
      colors[i * 3 + 1] = baseColor.g;
      colors[i * 3 + 2] = baseColor.b;

      sizes[i] = lobeKey === 'PINEAL' ? 5.5 : (lobeKey === 'CALLOSUM' ? 3.8 : 2.6);
    }

    // Build Points Geometry
    const pointsGeo = new THREE.BufferGeometry();
    pointsGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    pointsGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    pointsGeo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    // Custom Particle Sprite Canvas
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.25, 'rgba(0, 240, 255, 0.85)');
    grad.addColorStop(0.6, 'rgba(168, 85, 247, 0.35)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);

    const texture = new THREE.CanvasTexture(canvas);
    texture.needsUpdate = true;

    const pointsMat = new THREE.PointsMaterial({
      size: 6.0,
      vertexColors: true,
      map: texture,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    if (this.neuronPoints) this.brainGroup.remove(this.neuronPoints);
    this.neuronPoints = new THREE.Points(pointsGeo, pointsMat);
    this.brainGroup.add(this.neuronPoints);
  }

  // =========================================================================
  // 3. SYNAPTIC CONNECTOME (100 TRILLION BIOLOGICAL / 32K GPU FIBERS)
  // =========================================================================
  buildSynapticConnectome() {
    this.synapses = [];
    const linePositions = new Float32Array(this.synapseCount * 6);
    const lineColors = new Float32Array(this.synapseCount * 6);

    let createdCount = 0;
    const maxAttempts = this.synapseCount * 4;
    let attempts = 0;

    while (createdCount < this.synapseCount && attempts < maxAttempts) {
      attempts++;
      const srcIdx = Math.floor(Math.random() * this.neurons.length);
      const src = this.neurons[srcIdx];

      // K-Nearest Neighbor & Inter-Hemispheric Callosum search
      let tgtIdx;
      if (src.lobe === 'CALLOSUM') {
        // Link to opposite hemisphere
        tgtIdx = (srcIdx + 1) % this.neurons.length;
      } else if (src.lobe === 'PINEAL') {
        // Link to Thalamus & Frontal
        tgtIdx = Math.floor(Math.random() * this.neurons.length);
      } else {
        const offset = Math.floor((Math.random() - 0.5) * 120);
        tgtIdx = (srcIdx + offset + this.neurons.length) % this.neurons.length;
      }

      if (srcIdx === tgtIdx) continue;
      const tgt = this.neurons[tgtIdx];

      const dist = src.currentPos.distanceTo(tgt.currentPos);
      if (dist > 90 && src.lobe !== 'CALLOSUM' && src.lobe !== 'PINEAL') continue;

      const synapse = {
        id: `SYN-${createdCount}`,
        source: src,
        target: tgt,
        weight: 0.4 + Math.random() * 0.6,
        activity: 0.1,
        length: dist
      };

      src.synapsesOut.push(synapse);
      tgt.synapsesIn.push(synapse);
      this.synapses.push(synapse);

      const pIdx = createdCount * 6;
      linePositions[pIdx] = src.currentPos.x;
      linePositions[pIdx + 1] = src.currentPos.y;
      linePositions[pIdx + 2] = src.currentPos.z;
      linePositions[pIdx + 3] = tgt.currentPos.x;
      linePositions[pIdx + 4] = tgt.currentPos.y;
      linePositions[pIdx + 5] = tgt.currentPos.z;

      const c1 = src.baseColor;
      const c2 = tgt.baseColor;
      lineColors[pIdx] = c1.r * 0.4;
      lineColors[pIdx + 1] = c1.g * 0.4;
      lineColors[pIdx + 2] = c1.b * 0.4;
      lineColors[pIdx + 3] = c2.r * 0.4;
      lineColors[pIdx + 4] = c2.g * 0.4;
      lineColors[pIdx + 5] = c2.b * 0.4;

      createdCount++;
    }

    const linesGeo = new THREE.BufferGeometry();
    linesGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    linesGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

    const linesMat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    if (this.synapseLines) this.brainGroup.remove(this.synapseLines);
    this.synapseLines = new THREE.LineSegments(linesGeo, linesMat);
    this.brainGroup.add(this.synapseLines);
  }

  // =========================================================================
  // 4. ACTION POTENTIAL PULSES & SYNAPTIC FIRING
  // =========================================================================
  buildActionPotentialPulses() {
    this.actionPulses = [];
    const pulsePositions = new Float32Array(this.activePulsesCount * 3);
    const pulseColors = new Float32Array(this.activePulsesCount * 3);

    for (let i = 0; i < this.activePulsesCount; i++) {
      const syn = this.synapses.length > 0 ? this.synapses[i % this.synapses.length] : null;
      this.actionPulses.push({
        synapse: syn,
        progress: Math.random(),
        speed: 0.6 + Math.random() * 1.4,
        color: new THREE.Color(0xffffff)
      });
      pulsePositions[i * 3] = 0;
      pulsePositions[i * 3 + 1] = 0;
      pulsePositions[i * 3 + 2] = 0;
      pulseColors[i * 3] = 1;
      pulseColors[i * 3 + 1] = 1;
      pulseColors[i * 3 + 2] = 1;
    }

    const pulseGeo = new THREE.BufferGeometry();
    pulseGeo.setAttribute('position', new THREE.BufferAttribute(pulsePositions, 3));
    pulseGeo.setAttribute('color', new THREE.BufferAttribute(pulseColors, 3));

    const pulseMat = new THREE.PointsMaterial({
      size: 4.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    if (this.pulsePoints) this.brainGroup.remove(this.pulsePoints);
    this.pulsePoints = new THREE.Points(pulseGeo, pulseMat);
    this.brainGroup.add(this.pulsePoints);
  }

  buildSelectionHighlight() {
    const ringGeo = new THREE.RingGeometry(8, 11, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85
    });
    this.selectionHighlight = new THREE.Mesh(ringGeo, ringMat);
    this.selectionHighlight.visible = false;
    this.brainGroup.add(this.selectionHighlight);
  }

  buildCosmicBackground() {
    const starCount = 1500;
    const starGeo = new THREE.BufferGeometry();
    const starPos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      starPos[i * 3] = (Math.random() - 0.5) * 3000;
      starPos[i * 3 + 1] = (Math.random() - 0.5) * 3000;
      starPos[i * 3 + 2] = (Math.random() - 0.5) * 3000;
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
    const starMat = new THREE.PointsMaterial({
      size: 1.5,
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.4
    });
    this.scene.add(new THREE.Points(starGeo, starMat));
  }

  buildAethelGeodesicRay() {
    this.aethelRayGroup = new THREE.Group();
    
    // Vertical Harmonic Geodesic Beam
    const beamGeo = new THREE.CylinderGeometry(1.5, 4.0, 600, 16, 1, true);
    const beamMat = new THREE.MeshBasicMaterial({
      color: 0xfbbf24,
      transparent: true,
      opacity: 0.28,
      wireframe: true,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const beam = new THREE.Mesh(beamGeo, beamMat);
    beam.position.set(0, 300, -12);
    this.aethelRayGroup.add(beam);

    // Geodesic Energy Particle Ring Pulse
    const ringCount = 120;
    const ringGeo = new THREE.BufferGeometry();
    const ringPos = new Float32Array(ringCount * 3);
    const ringCol = new Float32Array(ringCount * 3);
    for (let i = 0; i < ringCount; i++) {
      const angle = (i / ringCount) * Math.PI * 2;
      const r = 18 + Math.random() * 8;
      ringPos[i * 3] = Math.cos(angle) * r;
      ringPos[i * 3 + 1] = (i % 6) * 80;
      ringPos[i * 3 + 2] = Math.sin(angle) * r - 12;
      
      ringCol[i * 3] = 0.98;
      ringCol[i * 3 + 1] = 0.75;
      ringCol[i * 3 + 2] = 0.14;
    }
    ringGeo.setAttribute('position', new THREE.BufferAttribute(ringPos, 3));
    ringGeo.setAttribute('color', new THREE.BufferAttribute(ringCol, 3));
    const ringMat = new THREE.PointsMaterial({
      size: 3.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    this.aethelRayGroup.add(new THREE.Points(ringGeo, ringMat));

    this.brainGroup.add(this.aethelRayGroup);
  }


  // =========================================================================
  // 5. SELECTION, PROBE & FOCUS INTERACTIONS
  // =========================================================================
  selectNeuron(neuron, flyCamera = true) {
    this.selectedNeuron = neuron;
    if (!neuron) return;

    if (this.selectionHighlight) {
      this.selectionHighlight.position.copy(neuron.currentPos);
      this.selectionHighlight.visible = true;
      this.selectionHighlight.lookAt(this.camera.position);
    }

    // Update Probe HUD UI Elements
    const probeId = document.getElementById('probe-neuron-id');
    const probeDomain = document.getElementById('probe-domain-sub');
    const probeAct = document.getElementById('probe-act-val');
    const probeIn = document.getElementById('probe-syn-in');
    const probeOut = document.getElementById('probe-syn-out');
    const probeWeight = document.getElementById('probe-weight');
    const probeLayer = document.getElementById('probe-layer');
    const probeToken = document.getElementById('probe-token-text');

    if (this.currentTopology === 'CALABI_YAU_DREAM') {
      if (probeId) probeId.innerText = `GENE-12D-${neuron.bioCodon || 'DNA'}-${String(neuron.index).padStart(5, '0')}`;
      if (probeDomain) {
        probeDomain.innerHTML = `<span style="color:#00f0ff; font-weight:700;">🧬 ${neuron.bioDetail || 'DNA Double Helix'}</span> &bull; 12D Biological Manifold`;
      }
      if (probeAct) probeAct.innerText = `${(neuron.activation * 100).toFixed(1)}%`;
      if (probeIn) probeIn.innerText = `${neuron.synapsesIn.length} Axon Fibers`;
      if (probeOut) probeOut.innerText = `${neuron.synapsesOut.length} Synaptic Strings`;
      if (probeWeight) {
        probeWeight.innerText = `ATP Flux: ${(38.2 + Math.random() * 4.0).toFixed(1)} ATP/s • Δψ: -180mV`;
      }
      if (probeLayer) {
        probeLayer.innerText = `Codon: ${neuron.bioCodon || 'AUG'} • Substructure: ${neuron.bioType || 'DNA_HELIX'}`;
      }
      if (probeToken) {
        probeToken.innerText = `"[Quantum Epigenetic Thought]: Consolidating neural heuristic into 12D chromosomal matrix..."`;
      }
    } else {
      if (probeId) probeId.innerText = neuron.id;
      if (probeDomain) {
        probeDomain.innerHTML = `<span style="color:${neuron.domain.colorHex}; font-weight:700;">${neuron.domain.name}</span> &bull; ${neuron.hemisphere} Hemisphere`;
      }
      if (probeAct) probeAct.innerText = `${(neuron.activation * 100).toFixed(1)}%`;
      if (probeIn) probeIn.innerText = `${neuron.synapsesIn.length} Synapses`;
      if (probeOut) probeOut.innerText = `${neuron.synapsesOut.length} Synapses`;
      if (probeWeight) {
        probeWeight.innerText = `W: ${(0.75 + Math.random() * 0.24).toFixed(4)} | b: -0.0412`;
      }
      if (probeLayer) {
        probeLayer.innerText = `Layer ${neuron.layer} [${neuron.domain.function}]`;
      }
      if (probeToken) {
        probeToken.innerText = `"${tokenStream.activeTokens[neuron.lobe] || neuron.domain.baseTokens[0]}"`;
      }
    }

    if (flyCamera) {
      this.flyCameraTo(neuron.currentPos, 140);
    }
  }

  focusLobe(lobeKey) {
    const lobeNeurons = this.neurons.filter(n => n.lobe === lobeKey);
    if (lobeNeurons.length === 0) return;

    const center = new THREE.Vector3();
    lobeNeurons.forEach(n => center.add(n.currentPos));
    center.divideScalar(lobeNeurons.length);

    this.selectNeuron(lobeNeurons[Math.floor(lobeNeurons.length / 2)], false);
    this.flyCameraTo(center, 220);
    neuralAudio.playActionPotentialSurge();
  }

  focusMacroOverview() {
    this.flyCameraTo(new THREE.Vector3(0, 20, 0), 520);
  }

  flyCameraTo(targetLook, distance = 250) {
    this.isFlyingCamera = true;
    this.camTargetLook.copy(targetLook);

    const dir = this.camera.position.clone().sub(targetLook).normalize();
    this.camTargetPos.copy(targetLook).add(dir.multiplyScalar(distance));
  }

  setTopology(mode) {
    this.currentTopology = mode;
    this.neurons.forEach(n => {
      if (mode === 'ANATOMICAL_BRAIN') n.targetPos.copy(n.anatomicalPos);
      else if (mode === 'TRANSFORMER_STACK') n.targetPos.copy(n.transformerPos);
      else if (mode === 'AGENT_SWARM') n.targetPos.copy(n.swarmPos);
      else if (mode === 'ATTENTION_HEATMAP') n.targetPos.copy(n.anatomicalPos);
      else if (mode === 'CALABI_YAU_DREAM') n.targetPos.copy(n.calabiYauPos);
    });
    neuralAudio.playActionPotentialSurge();
  }

  setNeuronDensity(count) {
    this.neuronCount = Math.min(65536, Math.max(4096, count));
    this.synapseCount = this.neuronCount * 2;
    this.generateNeuralTopologies();
    this.buildSynapticConnectome();
    this.buildActionPotentialPulses();
  }

  fireActionPotential() {
    if (!this.selectedNeuron) return;
    this.selectedNeuron.activation = 1.0;
    this.selectedNeuron.firingState = true;
    neuralAudio.playActionPotentialSpike();
  }

  stimulateCurrentLobe() {
    if (!this.selectedNeuron) return;
    const lobe = this.selectedNeuron.lobe;
    this.neurons.filter(n => n.lobe === lobe).forEach(n => {
      n.activation = 0.9 + Math.random() * 0.1;
    });
    neuralAudio.playActionPotentialSurge();
  }

  initEventListeners() {
    window.addEventListener('resize', () => {
      if (!this.renderer || !this.camera) return;
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });

    this.container.addEventListener('pointerdown', (e) => {
      const rect = this.container.getBoundingClientRect();
      this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      this.raycaster.setFromCamera(this.mouse, this.camera);
      if (this.neuronPoints) {
        const intersects = this.raycaster.intersectObject(this.neuronPoints);
        if (intersects.length > 0) {
          const idx = intersects[0].index;
          if (idx !== undefined && this.neurons[idx]) {
            this.selectNeuron(this.neurons[idx], true);
            neuralAudio.playActionPotentialSpike();
          }
        }
      }
    });
  }

  // =========================================================================
  // 6. ANIMATION & OSCILLATOR TICK LOOP
  // =========================================================================
  animate() {
    requestAnimationFrame(this.animate);
    const delta = this.clock.getDelta() * this.simulationSpeed;

    if (!this.isPaused) {
      // 1. Rotate Brain Slowly
      this.brainGroup.rotation.y += 0.0015 * this.simulationSpeed;

      // 2. Pulse Pineal Gland Singularity
      if (this.pinealAura) {
        const scale = 1.0 + 0.25 * Math.sin(Date.now() * 0.00432);
        this.pinealAura.scale.set(scale, scale, scale);
        this.pinealAura.rotation.y += 0.01;
      }

      // Dynamic Biological DNA & Mitochondrial Pulsing in Dream Mode
      if (this.currentTopology === 'CALABI_YAU_DREAM') {
        const timeNow = Date.now() * 0.001;
        for (let i = 0; i < this.neurons.length; i++) {
          const n = this.neurons[i];
          if (n.bioType === 'DNA_STRAND_A' || n.bioType === 'DNA_STRAND_B') {
            const wave = Math.sin(timeNow * 2.0 + n.calabiYauPos.y * 0.02) * 2.5;
            n.targetPos.x = n.calabiYauPos.x + wave;
            n.targetPos.z = n.calabiYauPos.z + Math.cos(timeNow * 2.0 + n.calabiYauPos.y * 0.02) * 2.5;
          } else if (n.bioType === 'MITOCHONDRIA_CRISTAE') {
            const atpPulse = 1.0 + 0.08 * Math.sin(timeNow * 4.32 + i * 0.1);
            n.targetPos.x = n.calabiYauPos.x * atpPulse;
            n.targetPos.y = n.calabiYauPos.y * atpPulse;
            n.targetPos.z = n.calabiYauPos.z * atpPulse;
          } else if (n.bioType === 'TELOMERE_NORTH' || n.bioType === 'TELOMERE_SOUTH') {
            const flare = Math.sin(timeNow * 3.5 + i * 0.2) * 3.0;
            n.targetPos.y = n.calabiYauPos.y + (n.bioType === 'TELOMERE_NORTH' ? flare : -flare);
          }
        }
      }

      // 3. Interpolate Neuron Positions & Activations
      if (this.neuronPoints) {
        const posAttr = this.neuronPoints.geometry.attributes.position;
        const colAttr = this.neuronPoints.geometry.attributes.color;

        for (let i = 0; i < this.neurons.length; i++) {
          const n = this.neurons[i];
          n.currentPos.lerp(n.targetPos, 0.08);

          posAttr.array[i * 3] = n.currentPos.x;
          posAttr.array[i * 3 + 1] = n.currentPos.y;
          posAttr.array[i * 3 + 2] = n.currentPos.z;

          // Oscillation
          n.oscillationPhase += n.oscillationSpeed * delta;
          const osc = Math.sin(n.oscillationPhase) * 0.15;
          n.activation = THREE.MathUtils.clamp(n.baseActivation + osc, 0.0, 1.0);

          n.currentColor.copy(n.baseColor).lerp(n.activeColor, n.activation);
          colAttr.array[i * 3] = n.currentColor.r;
          colAttr.array[i * 3 + 1] = n.currentColor.g;
          colAttr.array[i * 3 + 2] = n.currentColor.b;
        }
        posAttr.needsUpdate = true;
        colAttr.needsUpdate = true;
      }

      // 4. Update Synaptic Fibers
      if (this.synapseLines) {
        const sPosAttr = this.synapseLines.geometry.attributes.position;
        for (let i = 0; i < this.synapses.length; i++) {
          const syn = this.synapses[i];
          const pIdx = i * 6;
          sPosAttr.array[pIdx] = syn.source.currentPos.x;
          sPosAttr.array[pIdx + 1] = syn.source.currentPos.y;
          sPosAttr.array[pIdx + 2] = syn.source.currentPos.z;
          sPosAttr.array[pIdx + 3] = syn.target.currentPos.x;
          sPosAttr.array[pIdx + 4] = syn.target.currentPos.y;
          sPosAttr.array[pIdx + 5] = syn.target.currentPos.z;
        }
        sPosAttr.needsUpdate = true;
      }

      // 5. Update Action Potential Traveling Packets
      if (this.pulsePoints) {
        const pPos = this.pulsePoints.geometry.attributes.position;
        for (let i = 0; i < this.actionPulses.length; i++) {
          const pulse = this.actionPulses[i];
          if (!pulse.synapse) continue;

          pulse.progress += pulse.speed * delta * 0.5;
          if (pulse.progress > 1.0) {
            pulse.progress = 0;
            pulse.synapse = this.synapses[Math.floor(Math.random() * this.synapses.length)];
          }

          const src = pulse.synapse.source.currentPos;
          const tgt = pulse.synapse.target.currentPos;
          pPos.array[i * 3] = src.x + (tgt.x - src.x) * pulse.progress;
          pPos.array[i * 3 + 1] = src.y + (tgt.y - src.y) * pulse.progress;
          pPos.array[i * 3 + 2] = src.z + (tgt.z - src.z) * pulse.progress;
        }
        pPos.needsUpdate = true;
      }

      // 6. Camera Smooth Flight
      if (this.isFlyingCamera && this.controls) {
        this.camera.position.lerp(this.camTargetPos, 0.08);
        this.controls.target.lerp(this.camTargetLook, 0.08);
        if (this.camera.position.distanceTo(this.camTargetPos) < 2) {
          this.isFlyingCamera = false;
        }
      }
    }

    if (this.controls) this.controls.update();

    // 7. Update Oscilloscope
    this.renderOscilloscope();

    this.renderer.render(this.scene, this.camera);
  }

  renderOscilloscope() {
    if (!this.oscCtx || !this.oscCanvas) return;
    const ctx = this.oscCtx;
    const w = this.oscCanvas.width;
    const h = this.oscCanvas.height;

    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 2;
    ctx.beginPath();

    const act = this.selectedNeuron ? this.selectedNeuron.activation : 0.5;
    for (let i = 0; i < this.oscData.length - 1; i++) {
      this.oscData[i] = this.oscData[i + 1];
    }
    this.oscData[this.oscData.length - 1] = (Math.sin(Date.now() * 0.015) * 0.35 + (act - 0.5)) * h * 0.4 + h * 0.5;

    for (let i = 0; i < this.oscData.length; i++) {
      const x = (i / (this.oscData.length - 1)) * w;
      const y = this.oscData[i];
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }
}
