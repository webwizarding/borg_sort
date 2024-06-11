#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

void insertion_sort(std::vector<int> &arr) {
  int n = arr.size();
  for (int i = 1; i < n; ++i) {
    int key = arr[i];
    int j = i - 1;
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      --j;
    }
    arr[j + 1] = key;
  }
}

std::vector<int> merge_sorted_arrays(const std::vector<int> &arr1,
                                     const std::vector<int> &arr2) {
  std::vector<int> sorted_array;
  int i = 0, j = 0;
  int n1 = arr1.size(), n2 = arr2.size();
  while (i < n1 && j < n2) {
    if (arr1[i] < arr2[j]) {
      sorted_array.push_back(arr1[i]);
      ++i;
    } else {
      sorted_array.push_back(arr2[j]);
      ++j;
    }
  }
  while (i < n1) {
    sorted_array.push_back(arr1[i]);
    ++i;
  }
  while (j < n2) {
    sorted_array.push_back(arr2[j]);
    ++j;
  }
  return sorted_array;
}

std::vector<int> borg_sort(std::vector<int> &arr, int split_size = 10) {
  std::vector<std::vector<int>> sub_arrays;
  for (size_t i = 0; i < arr.size(); i += split_size) {
    std::vector<int> sub_array(
        arr.begin() + i, arr.begin() + std::min(arr.size(), i + split_size));
    sub_arrays.push_back(sub_array);
  }

  for (auto &sub_array : sub_arrays) {
    insertion_sort(sub_array);
  }

  while (sub_arrays.size() > 1) {
    std::vector<std::vector<int>> merged_arrays;
    for (size_t i = 0; i < sub_arrays.size(); i += 2) {
      if (i + 1 < sub_arrays.size()) {
        merged_arrays.push_back(
            merge_sorted_arrays(sub_arrays[i], sub_arrays[i + 1]));
      } else {
        merged_arrays.push_back(sub_arrays[i]);
      }
    }
    sub_arrays = merged_arrays;
  }

  return sub_arrays.empty() ? std::vector<int>() : sub_arrays[0];
}

int main() {
  const int dataSize = 100000; 
  std::vector<int> data(dataSize);

  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> dis(1, 100000);

  for (int i = 0; i < dataSize; ++i) {
    data[i] = dis(gen);
  }

  std::cout << "Original data size: " << data.size() << std::endl;

  auto start = std::chrono::high_resolution_clock::now();

  std::vector<int> sorted_data = borg_sort(data);

  auto end = std::chrono::high_resolution_clock::now();
  auto elapsed =
      std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

  double time_in_seconds = elapsed.count() / 1000.0;
  int time_in_milliseconds = elapsed.count();

  std::cout << "Sorted data size: " << sorted_data.size() << std::endl;

  std::cout << "Sort time: " << time_in_seconds << " seconds ("
            << time_in_milliseconds << " milliseconds)" << std::endl;

  return 0;
}
