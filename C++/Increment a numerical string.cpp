
// standard C++ string stream operators
#include <cstdlib>
#include <string>
#include <sstream>

// inside a function or method...
std::string s = "12345";

int i;
std::istringstream(s) >> i;
i++;
//or:
//int i = std::atoi(s.c_str()) + 1;

std::ostringstream oss;
if (oss << i) s = oss.str();

Works with: C++11
#include <string>

std::string s = "12345";
s = std::to_string(1+std::stoi(s));

Library: Boost
// Boost
#include <cstdlib>
#include <string>
#include <boost/lexical_cast.hpp>

// inside a function or method...
std::string s = "12345";
int i = boost::lexical_cast<int>(s) + 1;
s = boost::lexical_cast<std::string>(i);

Library: Qt
Uses: Qt (Components:{{#foreach: component$n$|{{{component$n$}}}Property "Uses Library" (as page type) with input value "Library/Qt/{{{component$n$}}}" contains invalid characters or is incomplete and therefore can cause unexpected results during a query or annotation process., }})
// Qt
QString num1 = "12345";
QString num2 = QString("%1").arg(v1.toInt()+1);

Library: MFC
Uses: Microsoft Foundation Classes (Components:{{#foreach: component$n$|{{{component$n$}}}Property "Uses Library" (as page type) with input value "Library/Microsoft Foundation Classes/{{{component$n$}}}" contains invalid characters or is incomplete and therefore can cause unexpected results during a query or annotation process., }})
Uses: C Runtime (Components:{{#foreach: component$n$|{{{component$n$}}}Property "Uses Library" (as page type) with input value "Library/C Runtime/{{{component$n$}}}" contains invalid characters or is incomplete and therefore can cause unexpected results during a query or annotation process., }})
// MFC
CString s = "12345";
int i = _ttoi(s) + 1;
int i = _tcstoul(s, NULL, 10) + 1; 
s.Format("%d", i);

All of the above solutions only work for numbers <= INT_MAX. The following works for an (almost) arbitrary large number:

Works with: g++ version 4.0.2
#include <string>
#include <iostream>
#include <ostream>

void increment_numerical_string(std::string& s)
{
    std::string::reverse_iterator iter = s.rbegin(), end = s.rend();
    int carry = 1;
    while (carry && iter != end)
    {
        int value = (*iter - '0') + carry;
        carry = (value / 10);
        *iter = '0' + (value % 10);
        ++iter;
    }
    if (carry)
        s.insert(0, "1");
}

int main()
{
    std::string big_number = "123456789012345678901234567899";
    std::cout << "before increment: " << big_number << "\n";
    increment_numerical_string(big_number);
    std::cout << "after increment:  " << big_number << "\n";
}
