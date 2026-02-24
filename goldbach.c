/*
This is a highly optimized implementation to test Goldbach's conjecture for even numbers in a given range. 
It uses a segmented sieve approach to generate primes and checks the conjecture in parallel using OpenMP.

Keeps memory usage low by only storing odd numbers and uses bit manipulation for efficient storage.

2026 Alex Hauptman - GNU General Public License v3.0
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <math.h>
#include <string.h>
#include <omp.h>

typedef uint64_t u64;

#define GET_BIT(arr, i) (arr[(i) >> 3] & (1 << ((i) & 7)))
#define SET_BIT(arr, i) (arr[(i) >> 3] |= (1 << ((i) & 7)))

#define SEGMENT_SIZE (1ULL << 22)  // 4MB range

// Generate small primes up to sqrt(end)
u64 generate_small_primes(u64 limit, u64 **primes_out) {
    u64 size = (limit / 2) + 1;
    uint8_t *sieve = calloc((size >> 3) + 1, 1);
    if (!sieve) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    u64 sqrt_limit = (u64)sqrt((long double)limit);

    for (u64 i = 3; i <= sqrt_limit; i += 2) {
        if (!GET_BIT(sieve, i >> 1)) {
            for (u64 j = i * i; j <= limit; j += 2 * i)
                SET_BIT(sieve, j >> 1);
        }
    }

    u64 count = 1; // prime 2
    for (u64 i = 3; i <= limit; i += 2)
        if (!GET_BIT(sieve, i >> 1))
            count++;

    u64 *primes = malloc(count * sizeof(u64));
    if (!primes) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    primes[0] = 2;
    u64 idx = 1;
    for (u64 i = 3; i <= limit; i += 2)
        if (!GET_BIT(sieve, i >> 1))
            primes[idx++] = i;

    free(sieve);
    *primes_out = primes;
    return count;
}

static inline int is_prime_segment(uint8_t *segment, u64 n, u64 low) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if ((n & 1) == 0) return 0;
    return !GET_BIT(segment, (n - low) >> 1);
}

// Fallback primality test using small primes
static int is_prime_global(u64 n, u64 *small_primes, u64 small_count) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if ((n & 1) == 0) return 0;

    for (u64 i = 0; i < small_count && small_primes[i] * small_primes[i] <= n; i++) {
        if (n % small_primes[i] == 0)
            return 0;
    }
    return 1;
}

void test_goldbach(u64 start, u64 end) {
    if (start < 4) start = 4;
    if (start & 1) start++;

    u64 sqrt_end = (u64)sqrt((long double)end);
    u64 *small_primes;
    u64 small_count = generate_small_primes(sqrt_end, &small_primes);

    #pragma omp parallel
    {
        uint8_t *segment = malloc((SEGMENT_SIZE >> 4) + 1);
        if (!segment) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(EXIT_FAILURE);
        }

        #pragma omp for schedule(dynamic)
        for (u64 low = 0; low <= end; low += SEGMENT_SIZE) {

            u64 high = low + SEGMENT_SIZE - 1;
            if (high > end) high = end;

            memset(segment, 0, (SEGMENT_SIZE >> 4) + 1);

            // Mark composites (skip prime 2)
            for (u64 i = 1; i < small_count; i++) {
                u64 p = small_primes[i];

                u64 start_index = (low + p - 1) / p * p;
                if (start_index < p * p)
                    start_index = p * p;

                for (u64 j = start_index; j <= high; j += p) {
                    if ((j & 1) && j >= low)
                        SET_BIT(segment, (j - low) >> 1);
                }
            }

            u64 seg_start = (low > start) ? low : start;
            if (seg_start & 1) seg_start++;

            u64 seg_end = (high < end) ? high : end;

            for (u64 n = seg_start; n <= seg_end; n += 2) {

                int found = 0;

                for (u64 i = 0; i < small_count && small_primes[i] <= n / 2; i++) {

                    u64 p = small_primes[i];
                    u64 other = n - p;
                    int prime_flag;

                    if (other >= low && other <= high)
                        prime_flag = is_prime_segment(segment, other, low);
                    else
                        prime_flag = is_prime_global(other, small_primes, small_count);

                    if (prime_flag) {
                        found = 1;
                        break;
                    }
                }

                if (!found) {
                    #pragma omp critical
                    {
                        printf("Goldbach FAILED at %" PRIu64 "\n", n);
                    }
                    abort();
                }
            }
        }

        free(segment);
    }

    free(small_primes);
    printf("Goldbach holds for [%" PRIu64 ", %" PRIu64 "]\n", start, end);
}
int main(void) {
    u64 start, end;

    printf("Goldbach Conjecture Tester\n");
    printf("--------------------------\n");

    printf("Enter start value: ");
    if (scanf("%" SCNu64, &start) != 1) {
        fprintf(stderr, "Invalid input for start value.\n");
        return 1;
    }

    printf("Enter end value: ");
    if (scanf("%" SCNu64, &end) != 1) {
        fprintf(stderr, "Invalid input for end value.\n");
        return 1;
    }

    if (end < start) {
        fprintf(stderr, "Error: end value must be >= start value.\n");
        return 1;
    }

    test_goldbach(start, end);
    return 0;
}