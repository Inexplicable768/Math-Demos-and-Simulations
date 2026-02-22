def is_prime(num):
    """Check if a number is prime (simple deterministic method)."""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5)+1, 2):
        if num % i == 0:
            return False
    return True

def find_perfect_numbers(n):
    """Find the first n perfect numbers using Euclid's formula."""
    perfect_numbers = []
    p = 2  # start with exponent 2
    while len(perfect_numbers) < n:
        mersenne_candidate = 2**p - 1
        if is_prime(mersenne_candidate):
            perfect = 2**(p-1) * mersenne_candidate
            perfect_numbers.append(perfect)
        p += 1
    return perfect_numbers

# Example usage:
n = int(input("Enter how many perfect numbers to find: "))
perfects = find_perfect_numbers(n)
for i, num in enumerate(perfects, start=1):
    print(f"{i}: {num}")