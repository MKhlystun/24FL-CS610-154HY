#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

int main() {
    // Define the number of integers needed for a 1MB array
    const int arraySize = 2500000 ; /// sizeof(int); // 1MB in integers (assuming 4 bytes per int)

    // Create a vector of integers to store the random data
    std::vector<int> arr(arraySize);

    // Seed the random number generator
    std::srand(std::time(0));

    // Fill the array with random integers
    for (int &num : arr) {
        num = std::rand(); // Random number between 0 and RAND_MAX
    }

    // Output unsorted array (optional, for testing)
    std::cout << "Unsorted Array (First 10 elements): ";
    for (int i = 0; i < 10 && i < arraySize; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << "...\n";

    // Sort the array
    std::sort(arr.begin(), arr.end());

    // Output sorted array (optional, for testing)
    std::cout << "Sorted Array (First 10 elements): ";
    for (int i = 0; i < 10 && i < arraySize; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << "...\n";

    return 0;
}
