
#include <iostream>
#include <windows.h>

const int EL_COUNT = 77, LLEN = 11;

class cocktailSort
{
public:
    void sort( int* arr, int len )
    {
	bool notSorted = true;
	while( notSorted )
	{
	    notSorted = false;
	    for( int a = 0; a < len - 1; a++ )
	    {
		if( arr[a] > arr[a + 1] )
		{
		    sSwap( arr[a], arr[a + 1] );
		    notSorted = true;
		}
	    }
 
	    if( !notSorted ) break;
	    notSorted = false;
 
	    for( int a = len - 1; a > 0; a-- )
	    {
		if( arr[a - 1] > arr[a] )
		{
		    sSwap( arr[a], arr[a - 1] );
		    notSorted = true;
		}
	    }
	}
    }
 
private:
    void sSwap( int& a, int& b )
    {
	int t = a;
   	a = b; b = t;
    }
};

int main( int argc, char* argv[] )
{
    srand( GetTickCount() );
    cocktailSort cs;
    int arr[EL_COUNT];
 
    for( int x = 0; x < EL_COUNT; x++ )
        arr[x] = rand() % EL_COUNT + 1;
 
    std::cout << "Original: " << std::endl << "==========" << std::endl;
    for( int x = 0; x < EL_COUNT; x += LLEN )
    {
	for( int s = x; s < x + LLEN; s++ )
	    std::cout << arr[s] << ", ";
 
	std::cout << std::endl;
    }
 
    //DWORD now = GetTickCount(); 
    cs.sort( arr, EL_COUNT );
    //now = GetTickCount() - now;
 
    std::cout << std::endl << std::endl << "Sorted: " << std::endl << "========" << std::endl;
    for( int x = 0; x < EL_COUNT; x += LLEN )
    {
	for( int s = x; s < x + LLEN; s++ )
	    std::cout << arr[s] << ", ";
 
	std::cout << std::endl;
    }
 
    std::cout << std::endl << std::endl << std::endl << std::endl;
    //std::cout << now << std::endl << std::endl; 
    return 0;
}

Alternate version
Uses C++11. Compile with

g++ -std=c++11 cocktail.cpp

#include <algorithm>
#include <iostream>
#include <iterator>

template <typename RandomAccessIterator>
void cocktail_sort(RandomAccessIterator begin, RandomAccessIterator end) {
  bool swapped = true;
  while (begin != end-- && swapped) {
    swapped = false;
    for (auto i = begin; i != end; ++i) {
      if (*(i + 1) < *i) {
        std::iter_swap(i, i + 1);
        swapped = true;
      }
    }
    if (!swapped) {
      break;
    }
    swapped = false;
    for (auto i = end - 1; i != begin; --i) {
      if (*i < *(i - 1)) {
        std::iter_swap(i, i - 1);
        swapped = true;
      }
    }
    ++begin;
  }
}

int main() {
  int a[] = {100, 2, 56, 200, -52, 3, 99, 33, 177, -199};
  cocktail_sort(std::begin(a), std::end(a));
  copy(std::begin(a), std::end(a), std::ostream_iterator<int>(std::cout, " "));
  std::cout << "\n";
}
