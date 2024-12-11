#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>

int main() {
    // Define the number of integers needed for a 1MB array
    const int arraySize = 2500 * 1000 ; /// sizeof(int); // 1MB in integers (assuming 4 bytes per int)

    // Create a vector of integers to store the random data
    std::vector<int> arr(arraySize);

    // Seed the random number generator
    std::srand(std::time(0));

    // Fill the array with random integers
    for (int &num : arr) {
        num = std::rand(); // Random number between 0 and RAND_MAX
    }
    for (int i = 0; i < 4 * arraySize; ++i) {
    // Generate a random index between 0 and 999
    int randomIndex = std::rand() % arraySize;

    // Access the element at the random index
    int value = arr[randomIndex];

    // Optional: Print the value (commented out to avoid excessive output)
    // std::cout << "Random value: " << value << std::endl;
    }

    return 0;
}
