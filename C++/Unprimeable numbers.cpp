
#include <iostream>
#include <cstdint>
#include "prime_sieve.hpp"

typedef uint32_t integer;

// return number of decimal digits
int count_digits(integer n) {
    int digits = 0;
    for (; n > 0; ++digits)
        n /= 10;
    return digits;
}

// return the number with one digit replaced
integer change_digit(integer n, int index, int new_digit) {
    integer p = 1;
    integer changed = 0;
    for (; index > 0; p *= 10, n /= 10, --index)
        changed += p * (n % 10);
    changed += (10 * (n/10) + new_digit) * p;
    return changed;
}

// returns true if n unprimeable
bool unprimeable(const prime_sieve& sieve, integer n) {
    if (sieve.is_prime(n))
        return false;
    int d = count_digits(n);
    for (int i = 0; i < d; ++i) {
        for (int j = 0; j <= 9; ++j) {
            integer m = change_digit(n, i, j);
            if (m != n && sieve.is_prime(m))
                return false;
        }
    }
    return true;
}

int main() {
    const integer limit = 10000000;
    prime_sieve sieve(limit);

    // print numbers with commas
    std::cout.imbue(std::locale(""));

    std::cout << "First 35 unprimeable numbers:\n";
    integer n = 100;
    integer lowest[10] = { 0 };
    for (int count = 0, found = 0; n < limit && (found < 10 || count < 600); ++n) {
        if (unprimeable(sieve, n)) {
            if (count < 35) {
                if (count != 0)
                    std::cout << ", ";
                std::cout << n;
            }
            ++count;
            if (count == 600)
                std::cout << "\n600th unprimeable number: " << n << '\n';
            int last_digit = n % 10;
            if (lowest[last_digit] == 0) {
                lowest[last_digit] = n;
                ++found;
            }
        }
    }
    for (int i = 0; i < 10; ++i)
        std::cout << "Least unprimeable number ending in " << i << ": " << lowest[i] << '\n';
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
