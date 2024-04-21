
#include <iostream>
#include <boost/date_time/posix_time/posix_time.hpp>

int main( ) {
   boost::posix_time::ptime t ( boost::posix_time::second_clock::local_time( ) ) ;
   std::cout << to_simple_string( t ) << std::endl ;
   return 0 ;
}

C++ 11
#include <chrono>
#include <ctime> //for conversion std::ctime()
#include <iostream>

int main() {
    auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::cout << std::ctime(&timenow) << std::endl;
}
