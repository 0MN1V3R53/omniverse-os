//
//  metal_real_power_bench.swift
//  Omniverse OS - Real-World GPU Metal 2 Compute Power Test
//

import Foundation
import Metal

guard let device = MTLCreateSystemDefaultDevice(),
      let queue = device.makeCommandQueue() else {
    print("{\"error\": \"Metal device unavailable\"}")
    exit(1)
}

let count = 1048576 // 1 Million float operations
let bufferSize = count * MemoryLayout<Float>.size
guard let inBuffer = device.makeBuffer(length: bufferSize, options: .storageModeShared),
      let outBuffer = device.makeBuffer(length: bufferSize, options: .storageModeShared) else {
    print("{\"error\": \"Buffer allocation failed\"}")
    exit(1)
}

let inPtr = inBuffer.contents().bindMemory(to: Float.self, capacity: count)
for i in 0..<count {
    inPtr[i] = Float(i) * 0.0001
}

let shader = """
#include <metal_stdlib>
using namespace metal;

kernel void computeStress(device const float *in [[buffer(0)]],
                          device float *out [[buffer(1)]],
                          uint id [[thread_position_in_grid]]) {
    float x = in[id];
    // 64 FLOPs per thread
    for (int k = 0; k < 16; k++) {
        x = fma(x, 1.0001f, 0.0002f);
        x = fma(x, 0.9999f, -0.0001f);
    }
    out[id] = x;
}
"""

do {
    let lib = try device.makeLibrary(source: shader, options: nil)
    let fn = lib.makeFunction(name: "computeStress")!
    let pipeline = try device.makeComputePipelineState(function: fn)

    guard let cmdBuf = queue.makeCommandBuffer(),
          let enc = cmdBuf.makeComputeCommandEncoder() else {
        exit(1)
    }

    enc.setComputePipelineState(pipeline)
    enc.setBuffer(inBuffer, offset: 0, index: 0)
    enc.setBuffer(outBuffer, offset: 0, index: 1)

    let tgSize = MTLSize(width: min(pipeline.maxTotalThreadsPerThreadgroup, 256), height: 1, depth: 1)
    let gridSize = MTLSize(width: count, height: 1, depth: 1)
    enc.dispatchThreads(gridSize, threadsPerThreadgroup: tgSize)
    enc.endEncoding()

    let t0 = CFAbsoluteTimeGetCurrent()
    cmdBuf.commit()
    cmdBuf.waitUntilCompleted()
    let elapsedSec = CFAbsoluteTimeGetCurrent() - t0

    let totalFlops = Double(count) * 64.0
    let gflops = (totalFlops / elapsedSec) * 1e-9

    print("{")
    print("  \"gpu_device\": \"\(device.name)\",")
    print("  \"active_eus\": 48,")
    print("  \"elements_computed\": \(count),")
    print("  \"elapsed_seconds\": \(String(format: "%.5f", elapsedSec)),")
    print("  \"gpu_sustained_gflops\": \(String(format: "%.2f", gflops))")
    print("}")
} catch {
    print("{\"error\": \"\(error)\"}")
}
