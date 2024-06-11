import time
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sorted_arrays(arr1, arr2):
    sorted_array = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            sorted_array.append(arr1[i])
            i += 1
        else:
            sorted_array.append(arr2[j])
            j += 1
    sorted_array.extend(arr1[i:])
    sorted_array.extend(arr2[j:])
    return sorted_array


def split_and_merge_sort(arr, split_size=10):
    sub_arrays = [arr[i:i + split_size] for i in range(0, len(arr), split_size)]

    for i in range(len(sub_arrays)):
        sub_arrays[i] = insertion_sort(sub_arrays[i])

    while len(sub_arrays) > 1:
        merged_arrays = []
        for i in range(0, len(sub_arrays), 2):
            if i + 1 < len(sub_arrays):
                merged_arrays.append(merge_sorted_arrays(sub_arrays[i], sub_arrays[i + 1]))
            else:
                merged_arrays.append(sub_arrays[i])
        sub_arrays = merged_arrays

    return sub_arrays[0] if sub_arrays else []


file_path = 'kc_house_data.csv'
data = pd.read_csv(file_path)

prices = data['price'].tolist()

start_time = time.time()
for _ in tqdm(range(1), desc="Borg Sort Progress"):
    borg_sorted = split_and_merge_sort(prices.copy())
borg_sort_time = time.time() - start_time

print(f"Borg Sort Time: {borg_sort_time} seconds")

methods = ['Borg Sort']
times = [borg_sort_time]

plt.bar(methods, times, color=['green'])
plt.xlabel('Sorting Method')
plt.ylabel('Time (seconds)')
plt.title('Sorting Time Comparison')
plt.show()

sorted_data = data.copy()
sorted_data['price'] = borg_sorted
sorted_data.to_csv('borg_sorted_prices.csv', index=False)
