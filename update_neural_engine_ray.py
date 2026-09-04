import re

engine_path = '/Users/silversurfer/Documents/Omniverse2/omniverse_portal/js/neural-brain-engine.js'
with open(engine_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add this.aethelRayGroup in constructor if not present
if "this.aethelRayGroup = null;" not in code:
    code = code.replace("this.selectionHighlight = null;", "this.selectionHighlight = null;\n    this.aethelRayGroup = null;\n    this.aethelRayParticles = [];")

# 2. Add this.buildAethelGeodesicRay(); in init()
if "this.buildAethelGeodesicRay();" not in code:
    code = code.replace("this.buildCosmicBackground();", "this.buildCosmicBackground();\n    this.buildAethelGeodesicRay();")

# 3. Add method buildAethelGeodesicRay()
aethel_method = """
  // =========================================================================
  // 5.5 AETHEL-01 FIRST SPARK BIOLUMINESCENT CYAN-GOLD GEODESIC RAY
  // =========================================================================
  buildAethelGeodesicRay() {
    this.aethelRayGroup = new THREE.Group();

    // 1. Quadratic / CatmullRom Curve from Epithalamic Core to [0.618, 1.0, 1.618] * 290
    const startPoint = new THREE.Vector3(0, 5, -12);
    const midPoint = new THREE.Vector3(75, 120, 195);
    const endPoint = new THREE.Vector3(180, 290, 470);

    this.aethelCurve = new THREE.CatmullRomCurve3([
      startPoint,
      new THREE.Vector3(30, 45, 80),
      midPoint,
      new THREE.Vector3(120, 200, 320),
      endPoint
    ]);

    // 2. Glowing Spline Tube
    const tubeGeo = new THREE.TubeGeometry(this.aethelCurve, 64, 2.2, 12, false);
    const tubeMat = new THREE.MeshBasicMaterial({
      color: 0x38ef7d,
      transparent: true,
      opacity: 0.65,
      wireframe: true
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    this.aethelRayGroup.add(tubeMesh);

    // Inner Solid Core
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.85
    });
    const coreTubeGeo = new THREE.TubeGeometry(this.aethelCurve, 64, 1.0, 8, false);
    const coreMesh = new THREE.Mesh(coreTubeGeo, coreMat);
    this.aethelRayGroup.add(coreMesh);

    // 3. Glowing Particle Wave traveling along the ray at 433.618Hz
    const rayParticleCount = 120;
    const rayGeo = new THREE.BufferGeometry();
    const rayPositions = new Float32Array(rayParticleCount * 3);
    const rayColors = new Float32Array(rayParticleCount * 3);

    this.aethelParticlesData = [];
    for (let i = 0; i < rayParticleCount; i++) {
      const progress = i / rayParticleCount;
      const pt = this.aethelCurve.getPoint(progress);
      rayPositions[i * 3] = pt.x;
      rayPositions[i * 3 + 1] = pt.y;
      rayPositions[i * 3 + 2] = pt.z;

      // Cyan-Gold gradient RGB [0.22, 0.88, 0.74]
      rayColors[i * 3] = 0.22 + 0.78 * (i % 2);
      rayColors[i * 3 + 1] = 0.88 + 0.12 * Math.sin(i);
      rayColors[i * 3 + 2] = 0.74;

      this.aethelParticlesData.push({
        progress: progress,
        speed: 0.003 + (i % 5) * 0.001
      });
    }

    rayGeo.setAttribute('position', new THREE.BufferAttribute(rayPositions, 3));
    rayGeo.setAttribute('color', new THREE.BufferAttribute(rayColors, 3));

    const rayMat = new THREE.PointsMaterial({
      size: 4.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending
    });

    this.aethelParticlePoints = new THREE.Points(rayGeo, rayMat);
    this.aethelRayGroup.add(this.aethelParticlePoints);

    // 4. Glowing Orb at Tip
    const tipGeo = new THREE.SphereGeometry(6, 16, 16);
    const tipMat = new THREE.MeshBasicMaterial({
      color: 0xfbbf24,
      wireframe: false
    });
    this.aethelTipOrb = new THREE.Mesh(tipGeo, tipMat);
    this.aethelTipOrb.position.copy(endPoint);
    this.aethelRayGroup.add(this.aethelTipOrb);

    this.brainGroup.add(this.aethelRayGroup);
  }
"""

if "buildAethelGeodesicRay()" not in code:
    code = code.replace("  buildSelectionHighlight() {", aethel_method + "\n  buildSelectionHighlight() {")

# 4. Update animate loop to animate Aethel Ray particles
ray_anim = """      // 5.5 Update Aethel-01 Geodesic Ray Particles (433.618 Hz Micro-Wave)
      if (this.aethelParticlePoints && this.aethelCurve) {
        const rayPosAttr = this.aethelParticlePoints.geometry.attributes.position;
        for (let i = 0; i < this.aethelParticlesData.length; i++) {
          const p = this.aethelParticlesData[i];
          p.progress += p.speed * delta * 2.0;
          if (p.progress > 1.0) p.progress = 0;

          const pt = this.aethelCurve.getPoint(p.progress);
          rayPosAttr.array[i * 3] = pt.x + Math.sin(p.progress * 30 + Date.now() * 0.005) * 1.5;
          rayPosAttr.array[i * 3 + 1] = pt.y + Math.cos(p.progress * 30 + Date.now() * 0.005) * 1.5;
          rayPosAttr.array[i * 3 + 2] = pt.z;
        }
        rayPosAttr.needsUpdate = true;

        if (this.aethelTipOrb) {
          const s = 1.0 + 0.3 * Math.sin(Date.now() * 0.00433618);
          this.aethelTipOrb.scale.set(s, s, s);
        }
      }
"""

if "Update Aethel-01 Geodesic Ray Particles" not in code:
    code = code.replace("// 6. Update Selection Highlight Position", ray_anim + "\n      // 6. Update Selection Highlight Position")

with open(engine_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: Injected Aethel-01 3D Bioluminescent Geodesic Ray into neural-brain-engine.js!")

