/*
 * Omniverse OS - Real-World Silicon Power & Benchmark Test Engine
 * Base Reality Benchmark: CPU Single/Multi-core, AVX2 SIMD, Memory Bandwidth, and I/O
 * Author: CEO Dr. Alexander Vance & Dr. Kai Sterling
 * Pod: Pod 16 (macOS Systems Division)
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <pthread.h>
#include <immintrin.h>
#include <unistd.h>
#include <fcntl.h>

static double get_time_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec * 1e-6;
}

// 1. Single-Core Integer Benchmark: Sieve of Eratosthenes (Primes up to 10M)
typedef struct {
    uint64_t primes_found;
    double elapsed_sec;
    double ops_per_sec;
} SieveResult;

SieveResult run_sieve_benchmark(uint32_t limit) {
    SieveResult res;
    double t0 = get_time_sec();
    
    uint8_t *is_prime = (uint8_t *)malloc(limit + 1);
    memset(is_prime, 1, limit + 1);
    is_prime[0] = is_prime[1] = 0;
    
    for (uint32_t p = 2; p * p <= limit; p++) {
        if (is_prime[p]) {
            for (uint32_t i = p * p; i <= limit; i += p) {
                is_prime[i] = 0;
            }
        }
    }
    
    uint64_t count = 0;
    for (uint32_t i = 2; i <= limit; i++) {
        if (is_prime[i]) count++;
    }
    
    double t1 = get_time_sec();
    free(is_prime);
    
    res.primes_found = count;
    res.elapsed_sec = t1 - t0;
    res.ops_per_sec = (double)limit / res.elapsed_sec;
    return res;
}

// 2. Multi-Core AVX2 Floating Point Benchmark
#define MATRIX_DIM 512
#define THREAD_COUNT 4

typedef struct {
    int thread_id;
    int dim;
    float *A;
    float *B;
    float *C;
    double elapsed_sec;
    double gflops;
} MatMulThreadArg;

void *matmul_worker(void *arg) {
    MatMulThreadArg *m = (MatMulThreadArg *)arg;
    int n = m->dim;
    float *A = m->A;
    float *B = m->B;
    float *C = m->C;
    
    int rows_per_thread = n / THREAD_COUNT;
    int start_row = m->thread_id * rows_per_thread;
    int end_row = (m->thread_id == THREAD_COUNT - 1) ? n : start_row + rows_per_thread;
    
    double t0 = get_time_sec();
    for (int i = start_row; i < end_row; i++) {
        for (int k = 0; k < n; k++) {
            __m256 a_val = _mm256_set1_ps(A[i * n + k]);
            for (int j = 0; j < n; j += 8) {
                __m256 b_val = _mm256_loadu_ps(&B[k * n + j]);
                __m256 c_val = _mm256_loadu_ps(&C[i * n + j]);
                c_val = _mm256_fmadd_ps(a_val, b_val, c_val);
                _mm256_storeu_ps(&C[i * n + j], c_val);
            }
        }
    }
    double t1 = get_time_sec();
    m->elapsed_sec = t1 - t0;
    
    // Each element in result requires N multiply-adds = 2*N operations
    double total_ops = 2.0 * (double)(end_row - start_row) * (double)n * (double)n;
    m->gflops = (total_ops / m->elapsed_sec) * 1e-9;
    return NULL;
}

// 3. Memory Bandwidth Benchmark (Streaming AVX2 Read/Write)
typedef struct {
    double write_gb_sec;
    double read_gb_sec;
    double total_time_sec;
} MemBenchResult;

MemBenchResult run_memory_bandwidth(size_t buffer_bytes) {
    MemBenchResult res;
    size_t count = buffer_bytes / sizeof(float);
    float *src = (float *)malloc(buffer_bytes);
    float *dst = (float *)malloc(buffer_bytes);
    
    if (!src || !dst) {
        res.write_gb_sec = 0;
        res.read_gb_sec = 0;
        res.total_time_sec = 0;
        return res;
    }
    
    for (size_t i = 0; i < count; i++) {
        src[i] = (float)i * 0.001f;
    }
    
    // Sequential Streaming Write (Non-Temporal)
    double t0 = get_time_sec();
    __m256 v = _mm256_set1_ps(3.14159f);
    for (size_t iter = 0; iter < 4; iter++) {
        for (size_t i = 0; i < count; i += 8) {
            _mm256_stream_ps(&dst[i], v);
        }
    }
    _mm_sfence();
    double t1 = get_time_sec();
    double write_time = t1 - t0;
    res.write_gb_sec = (4.0 * (double)buffer_bytes / (1024.0 * 1024.0 * 1024.0)) / write_time;
    
    // Sequential Vector Read
    double t2 = get_time_sec();
    __m256 accum = _mm256_setzero_ps();
    for (size_t iter = 0; iter < 4; iter++) {
        for (size_t i = 0; i < count; i += 8) {
            __m256 in = _mm256_loadu_ps(&dst[i]);
            accum = _mm256_add_ps(accum, in);
        }
    }
    _mm_sfence();
    double t3 = get_time_sec();
    double read_time = t3 - t2;
    if (read_time < 0.0001) read_time = 0.0001;
    res.read_gb_sec = (4.0 * (double)buffer_bytes / (1024.0 * 1024.0 * 1024.0)) / read_time;
    res.total_time_sec = write_time + read_time;
    
    free(src);
    free(dst);
    return res;
}

// 4. Crucial BX500 SSD Storage I/O Benchmark
typedef struct {
    double write_mb_sec;
    double read_mb_sec;
    size_t test_size_bytes;
} DiskBenchResult;

DiskBenchResult run_disk_benchmark(const char *test_path, size_t size_bytes) {
    DiskBenchResult res;
    res.test_size_bytes = size_bytes;
    
    char *buf = (char *)malloc(1024 * 1024); // 1 MB chunk
    memset(buf, 0xAB, 1024 * 1024);
    
    // Write test
    int fd = open(test_path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        res.write_mb_sec = 0;
        res.read_mb_sec = 0;
        free(buf);
        return res;
    }
    
    size_t chunks = size_bytes / (1024 * 1024);
    double t0 = get_time_sec();
    for (size_t i = 0; i < chunks; i++) {
        write(fd, buf, 1024 * 1024);
    }
    fsync(fd);
    double t1 = get_time_sec();
    close(fd);
    
    res.write_mb_sec = ((double)size_bytes / (1024.0 * 1024.0)) / (t1 - t0);
    
    // Read test
    fd = open(test_path, O_RDONLY);
    if (fd < 0) {
        res.read_mb_sec = 0;
        free(buf);
        return res;
    }
    
    double t2 = get_time_sec();
    for (size_t i = 0; i < chunks; i++) {
        read(fd, buf, 1024 * 1024);
    }
    double t3 = get_time_sec();
    close(fd);
    unlink(test_path);
    
    res.read_mb_sec = ((double)size_bytes / (1024.0 * 1024.0)) / (t3 - t2);
    free(buf);
    return res;
}

int main(void) {
    printf("{\n");
    printf("  \"benchmark_version\": \"Omniverse Real-World Silicon Power Engine 1.0\",\n");
    printf("  \"system\": \"iMac16,1 (Broadwell-U Core i5-5250U @ 1.60GHz / Turbo 2.70GHz)\",\n");
    
    // 1. Run Sieve
    SieveResult sieve = run_sieve_benchmark(10000000);
    printf("  \"single_core_int\": {\n");
    printf("    \"task\": \"Sieve of Eratosthenes (10,000,000 integers)\",\n");
    printf("    \"primes_found\": %llu,\n", sieve.primes_found);
    printf("    \"elapsed_seconds\": %.4f,\n", sieve.elapsed_sec);
    printf("    \"integers_per_sec\": %.2f\n", sieve.ops_per_sec);
    printf("  },\n");
    
    // 2. Run Matrix Multi-Core AVX2
    int n = MATRIX_DIM;
    size_t mat_bytes = n * n * sizeof(float);
    float *A = (float *)malloc(mat_bytes);
    float *B = (float *)malloc(mat_bytes);
    float *C = (float *)malloc(mat_bytes);
    for (int i = 0; i < n * n; i++) {
        A[i] = (float)(i % 100) * 0.01f;
        B[i] = (float)((i + 1) % 100) * 0.01f;
        C[i] = 0.0f;
    }
    
    pthread_t threads[THREAD_COUNT];
    MatMulThreadArg args[THREAD_COUNT];
    double mat_t0 = get_time_sec();
    for (int t = 0; t < THREAD_COUNT; t++) {
        args[t].thread_id = t;
        args[t].dim = n;
        args[t].A = A;
        args[t].B = B;
        args[t].C = C;
        pthread_create(&threads[t], NULL, matmul_worker, &args[t]);
    }
    
    double total_gflops = 0;
    for (int t = 0; t < THREAD_COUNT; t++) {
        pthread_join(threads[t], NULL);
        total_gflops += args[t].gflops;
    }
    double mat_t1 = get_time_sec();
    
    printf("  \"multi_core_avx2_fma\": {\n");
    printf("    \"task\": \"Dense 512x512 FP32 Matrix Multiplication (AVX2 FMA, 4 Threads)\",\n");
    printf("    \"elapsed_seconds\": %.4f,\n", mat_t1 - mat_t0);
    printf("    \"sustained_gflops\": %.2f,\n", total_gflops);
    printf("    \"thread_count\": %d\n", THREAD_COUNT);
    printf("  },\n");
    
    free(A); free(B); free(C);
    
    // 3. Run Memory Bandwidth (128 MB Buffer)
    MemBenchResult mem = run_memory_bandwidth(128 * 1024 * 1024);
    printf("  \"memory_bandwidth\": {\n");
    printf("    \"task\": \"SIMD AVX2 Non-Temporal Streaming (128 MB working buffer)\",\n");
    printf("    \"streaming_write_gb_s\": %.2f,\n", mem.write_gb_sec);
    printf("    \"streaming_read_gb_s\": %.2f,\n", mem.read_gb_sec);
    printf("    \"bus_width\": \"128-bit Dual Channel DDR3 1867MHz\"\n");
    printf("  },\n");
    
    // 4. Run Crucial BX500 Disk Benchmark (64 MB payload)
    DiskBenchResult disk = run_disk_benchmark("/tmp/omniverse_disk_test.tmp", 64 * 1024 * 1024);
    printf("  \"storage_io\": {\n");
    printf("    \"device\": \"Crucial BX500 SSD (APFS Container)\",\n");
    printf("    \"sequential_write_mb_s\": %.2f,\n", disk.write_mb_sec);
    printf("    \"sequential_read_mb_s\": %.2f\n", disk.read_mb_sec);
    printf("  }\n");
    printf("}\n");
    
    return 0;
}
