
#include <algorithm>

int main()
{
    int nums[] = {2,4,3,1,2};
    std::sort(nums, nums+sizeof(nums)/sizeof(int));
    return 0;
}

std::vector
#include <algorithm>
#include <vector>

int main()
{
    std::vector<int> nums;
    nums.push_back(2);
    nums.push_back(4);
    nums.push_back(3);
    nums.push_back(1);
    nums.push_back(2);
    std::sort(nums.begin(), nums.end());
    return 0;
}

std::list
#include <list>

int main()
{
    std::list<int> nums;
    nums.push_back(2);
    nums.push_back(4);
    nums.push_back(3);
    nums.push_back(1);
    nums.push_back(2);
    nums.sort();
    return 0;
}
