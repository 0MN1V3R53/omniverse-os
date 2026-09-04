/* ==========================================================================
   OMNIVERSE TECH — 3D THREE.JS QUANTUM NEURAL MATRIX CANVAS
   Interactive WebGL Hero Visualization with Particle Physics & Mouse Gravitation
   ========================================================================== */

import { soundEngine } from './sound-engine.js';

export function initThreeHero() {
  const container = document.getElementById('three-hero-canvas');
  if (!container || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x06080d, 0.0018);

  const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    1,
    2000
  );
  camera.position.z = 650;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Group to rotate
  const worldGroup = new THREE.Group();
  scene.add(worldGroup);

  // 1. Quantum Neural Node Particles (Sphere Lattice)
  const particleCount = 1200;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  const originalPositions = new Float32Array(particleCount * 3);

  const cyanColor = new THREE.Color(0x00f0ff);
  const purpleColor = new THREE.Color(0xa855f7);
  const emeraldColor = new THREE.Color(0x10b981);
  const whiteColor = new THREE.Color(0xffffff);

  const radius = 280;

  for (let i = 0; i < particleCount; i++) {
    const phi = Math.acos(-1 + (2 * i) / particleCount);
    const theta = Math.sqrt(particleCount * Math.PI) * phi;

    const r = radius + (Math.random() - 0.5) * 40;
    const x = r * Math.cos(theta) * Math.sin(phi);
    const y = r * Math.sin(theta) * Math.sin(phi);
    const z = r * Math.cos(phi);

    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;

    originalPositions[i * 3] = x;
    originalPositions[i * 3 + 1] = y;
    originalPositions[i * 3 + 2] = z;

    // Gradient colors
    let mixedColor;
    const rand = Math.random();
    if (rand < 0.5) {
      mixedColor = cyanColor.clone().lerp(whiteColor, Math.random() * 0.3);
    } else if (rand < 0.8) {
      mixedColor = purpleColor.clone().lerp(cyanColor, Math.random() * 0.4);
    } else {
      mixedColor = emeraldColor.clone();
    }

    colors[i * 3] = mixedColor.r;
    colors[i * 3 + 1] = mixedColor.g;
    colors[i * 3 + 2] = mixedColor.b;
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  // Point Texture
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
  gradient.addColorStop(0.3, 'rgba(0, 240, 255, 0.8)');
  gradient.addColorStop(0.8, 'rgba(0, 240, 255, 0.1)');
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 64, 64);
  const texture = new THREE.CanvasTexture(canvas);

  const material = new THREE.PointsMaterial({
    size: 9,
    vertexColors: true,
    map: texture,
    transparent: true,
    opacity: 0.85,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });

  const particleSystem = new THREE.Points(geometry, material);
  worldGroup.add(particleSystem);

  // 2. Orbital Rings
  const ringGroup = new THREE.Group();
  worldGroup.add(ringGroup);

  function createOrbitalRing(radius, tube, color, rotX, rotY) {
    const ringGeo = new THREE.TorusGeometry(radius, tube, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.35,
      wireframe: true
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = rotX;
    ring.rotation.y = rotY;
    ringGroup.add(ring);
    return ring;
  }

  const ring1 = createOrbitalRing(340, 1.2, 0x00f0ff, Math.PI / 3, 0);
  const ring2 = createOrbitalRing(370, 0.8, 0xa855f7, -Math.PI / 4, Math.PI / 6);
  const ring3 = createOrbitalRing(400, 0.6, 0x10b981, Math.PI / 6, -Math.PI / 3);

  // Mouse Interaction
  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;
  let shockwaveProgress = 0;

  window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX - window.innerWidth / 2) * 0.4;
    mouseY = (e.clientY - window.innerHeight / 2) * 0.4;
  });

  // Shockwave on Canvas Click
  window.addEventListener('click', (e) => {
    if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A' && e.target.tagName !== 'INPUT') {
      shockwaveProgress = 1.0;
      soundEngine.playShockwave();
    }
  });

  // Resize Handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // Animation Loop
  let clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const time = clock.getElapsedTime();

    // Smooth Camera Mouse Parallax
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;

    camera.position.x = targetX * 0.4;
    camera.position.y = -targetY * 0.4;
    camera.lookAt(scene.position);

    // Rotate World Lattice
    worldGroup.rotation.y += 0.002;
    worldGroup.rotation.x = Math.sin(time * 0.2) * 0.1;

    // Rotate Orbital Rings
    ring1.rotation.z += 0.004;
    ring2.rotation.z -= 0.003;
    ring3.rotation.y += 0.005;

    // Shockwave pulse decay
    if (shockwaveProgress > 0) {
      shockwaveProgress -= delta * 1.5;
      if (shockwaveProgress < 0) shockwaveProgress = 0;
    }

    // Dynamic Particle Oscillation & Shockwave Displacement
    const pos = geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
      const ix = i * 3;
      const iy = i * 3 + 1;
      const iz = i * 3 + 2;

      const ox = originalPositions[ix];
      const oy = originalPositions[iy];
      const oz = originalPositions[iz];

      const wave = Math.sin(time * 2 + ox * 0.01 + oy * 0.01) * 6;
      const shockDisplacement = shockwaveProgress * 60 * Math.sin(time * 10 + i);

      const factor = (radius + wave + shockDisplacement) / radius;

      pos[ix] = ox * factor;
      pos[iy] = oy * factor;
      pos[iz] = oz * factor;
    }
    geometry.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
  }

  animate();
}
