
#include <iostream>
#include "prime_sieve.hpp"

bool is_left_truncatable(const prime_sieve& sieve, int p) {
    for (int n = 10, q = p; p > n; n *= 10) {
        if (!sieve.is_prime(p % n) || q == p % n)
            return false;
        q = p % n;
    }
    return true;
}

bool is_right_truncatable(const prime_sieve& sieve, int p) {
    for (int q = p/10; q > 0; q /= 10) {
        if (!sieve.is_prime(q))
            return false;
    }
    return true;
}

int main() {
    const int limit = 1000000;

    // find the prime numbers up to the limit
    prime_sieve sieve(limit + 1);

    int largest_left = 0;
    int largest_right = 0;
    // find largest left truncatable prime
    for (int p = limit; p >= 2; --p) {
        if (sieve.is_prime(p) && is_left_truncatable(sieve, p)) {
            largest_left = p;
            break;
        }
    }
    // find largest right truncatable prime
    for (int p = limit; p >= 2; --p) {
        if (sieve.is_prime(p) && is_right_truncatable(sieve, p)) {
            largest_right = p;
            break;
        }
    }
    // write results to standard output
    std::cout << "Largest left truncatable prime is " << largest_left << '\n';
    std::cout << "Largest right truncatable prime is " << largest_right << '\n';
    return 0;
}

Contents of prime_sieve.hpp:

#ifndef PRIME_SIEVE_HPP
#define PRIME_SIEVE_HPP

#include <algorithm>
#include <vector>

/**
 * A simple implementation of the Sieve of Eratosthenes.
 * See https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes.
 */
class prime_sieve {
public:
    explicit prime_sieve(size_t);
    bool is_prime(size_t) const;
private:
    std::vector<bool> is_prime_;
};

/**
 * Constructs a sieve with the given limit.
 *
 * @param limit the maximum integer that can be tested for primality
 */
inline prime_sieve::prime_sieve(size_t limit) {
    limit = std::max(size_t(3), limit);
    is_prime_.resize(limit/2, true);
    for (size_t p = 3; p * p <= limit; p += 2) {
        if (is_prime_[p/2 - 1]) {
            size_t inc = 2 * p;
            for (size_t q = p * p; q <= limit; q += inc)
                is_prime_[q/2 - 1] = false;
        }
    }
}

/**
 * Returns true if the given integer is a prime number. The integer
 * must be less than or equal to the limit passed to the constructor.
 *
 * @param n an integer less than or equal to the limit passed to the
 * constructor
 * @return true if the integer is prime
 */
inline bool prime_sieve::is_prime(size_t n) const {
    if (n == 2)
        return true;
    if (n < 2 || n % 2 == 0)
        return false;
    return is_prime_.at(n/2 - 1);
}
