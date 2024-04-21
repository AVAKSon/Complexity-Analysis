
#include <iostream>
#include <cstdint>
#include <vector>
#include "prime_sieve.hpp"

using integer = uint32_t;
using vector = std::vector<integer>;

void print_vector(const vector& vec) {
    if (!vec.empty()) {
        auto i = vec.begin();
        std::cout << '(' << *i;
        for (++i; i != vec.end(); ++i)
            std::cout << ", " << *i;
        std::cout << ')';
    }
}

class diffs {
public:
    diffs(std::initializer_list<integer> list) : diffs_(list) {}
    diffs(const vector& vec) : diffs_(vec) {}
    void test_group(const vector&);
    size_t size() const {
        return diffs_.size();
    }
    void print(std::ostream&);
private:
    vector diffs_;
    vector first_;
    vector last_;
    integer count_ = 0;
};

void diffs::test_group(const vector& vec) {
    if (vec.size() < size() + 1)
        return;
    size_t start = vec.size() - size() - 1;
    for (size_t i = 0, j = start + 1; i < size(); ++i, ++j) {
        if (vec[j] - vec[j - 1] != diffs_[i])
            return;
    }
    vector group(vec.begin() + start, vec.end());
    if (count_ == 0)
        first_ = group;
    last_ = group;
    ++count_;
}

void diffs::print(std::ostream& out) {
    print_vector(diffs_);
    out << ": first group = ";
    print_vector(first_);
    out << ", last group = ";
    print_vector(last_);
    out << ", count = " << count_ << '\n';
}

int main() {
    const integer limit = 1000000;
    const size_t max_group_size = 4;
    prime_sieve sieve(limit);
    diffs d[] = { {2}, {1}, {2, 2}, {2, 4}, {4, 2}, {6, 4, 2} };
    vector group;
    for (integer p = 0; p < limit; ++p) {
        if (!sieve.is_prime(p))
            continue;
        if (group.size() >= max_group_size)
            group.erase(group.begin());
        group.push_back(p);
        for (auto&& diff : d) {
            diff.test_group(group);
        }
    }
    for (auto&& diff : d) {
        diff.print(std::cout);
    }
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
