
#include <algorithm>
#include <iostream>
#include <iterator>
#include <locale>
#include <vector>
#include "prime_sieve.hpp"

const int limit1 = 1000000;
const int limit2 = 10000000;

class prime_info {
public:
    explicit prime_info(int max) : max_print(max) {}
    void add_prime(int prime);
    void print(std::ostream& os, const char* name) const;
private:
    int max_print;
    int count1 = 0;
    int count2 = 0;
    std::vector<int> primes;
};

void prime_info::add_prime(int prime) {
    ++count2;
    if (prime < limit1)
        ++count1;
    if (count2 <= max_print)
        primes.push_back(prime);
}

void prime_info::print(std::ostream& os, const char* name) const {
    os << "First " << max_print << " " << name << " primes: ";
    std::copy(primes.begin(), primes.end(), std::ostream_iterator<int>(os, " "));
    os << '\n';
    os << "Number of " << name << " primes below " << limit1 << ": " << count1 << '\n';
    os << "Number of " << name << " primes below " << limit2 << ": " << count2 << '\n';
}

int main() {
    prime_sieve sieve(limit2 + 100);

    // write numbers with groups of digits separated according to the system default locale
    std::cout.imbue(std::locale(""));

    // count and print strong/weak prime numbers
    prime_info strong_primes(36);
    prime_info weak_primes(37);
    int p1 = 2, p2 = 3;
    for (int p3 = 5; p2 < limit2; ++p3) {
        if (!sieve.is_prime(p3))
            continue;
        int diff = p1 + p3 - 2 * p2;
        if (diff < 0)
            strong_primes.add_prime(p2);
        else if (diff > 0)
            weak_primes.add_prime(p2);
        p1 = p2;
        p2 = p3;
    }
    strong_primes.print(std::cout, "strong");
    weak_primes.print(std::cout, "weak");
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

#endif
