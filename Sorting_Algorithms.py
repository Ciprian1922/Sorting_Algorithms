# Let's talk about how we can run this test by ourselves.
# You can open the code inside a python compiler(eg: PyCharm) and what you will have to do 
# is to insert the name of your output file (eg: timefor10elements), 
# insert the ammount of list to be sorted (larger number for a better precision(eg:100) if you 
# compute the average of the running time for every sorting algorithm, but for more than 10.000 elements
# you should reduce the preision (the lists to be sorted) so you get a faster running time of the algorithm),
# and finally insert the size of the lists to be generated and sorted.
# Every single sorting algorithm is sorting the same generated list so we can see better the difference in time
# execution.
# The output file will be generated in the same path as where the project will be situated, also the file will
# auto-generate as a CSV file.
# The colaboration for this code was done with two of my colleagues:
# https://github.com/AlexandraStulianec and https://github.com/maxi-todo
import random
import csv
import time

def bubble(list_org, n):
    list_sec = list_org.copy()
    for i in range(n-1):
        for j in range(n-i-1):
            if list_sec[j] > list_sec[j+1]:
                k = list_sec[j]
                list_sec[j] = list_sec[j+1]
                list_sec[j+1] = k

def selection(list_org, n):
    list_sec = list_org.copy()
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if list_sec[j] < list_sec[min_index]:
                min_index = j
                k = list_sec[min_index]
                list_sec[min_index] = list_sec[i]
                list_sec[i] = k
    #print(list_sec)

def insertion(list_org, n):
    list_sec = list_org.copy()
    for i in range(n):
        temp = list_sec[i]
        j = i-1
        while j >= 0 and list_sec[j] > temp:
            list_sec[j+1] = list_sec[j]
            j-=1
        list_sec[j+1] = temp
    #print(list_sec)

def partition(array, low, high):
    pivot = array[high]
    i = low-1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
        (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1

def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)


def quickSort1(array, low, high):
    stack = [(low, high)]
    while stack:
        (start, end) = stack.pop()
        if end - start > 0:
            pivot_index = partition(array, start, end)
            if pivot_index - start < end - pivot_index:
                stack.append((pivot_index + 1, end))
                stack.append((start, pivot_index - 1))
            else:
                stack.append((start, pivot_index - 1))
                stack.append((pivot_index + 1, end))


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)
    for i in range(0, n1):
        L[i] = arr[l + i]
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    i = 0
    j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        (arr[i], arr[largest]) = (arr[largest], arr[i])
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])
        heapify(arr, i, 0)


def count_sort(arr):
    max_element = int(max(arr))
    min_element = int(min(arr))
    range_of_elements = max_element - min_element + 1
    count_arr = [0 for _ in range(range_of_elements)]
    output_arr = [0 for _ in range(len(arr))]
    for i in range(0, len(arr)):
        count_arr[arr[i] - min_element] += 1
    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]
    for i in range(len(arr) - 1, -1, -1):
        output_arr[count_arr[arr[i] - min_element] - 1] = arr[i]
        count_arr[arr[i] - min_element] -= 1
    for i in range(0, len(arr)):
        arr[i] = output_arr[i]
    return arr

def countingSort(arr, exp1):
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]

def radixSort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        countingSort(arr, exp)
        exp *= 10

def bucketSort(arr, noOfBuckets):
    max_ele = max(arr)
    min_ele = min(arr)

    # range(for buckets)
    rnge = (max_ele - min_ele) / noOfBuckets

    temp = []

    # create empty buckets
    for i in range(noOfBuckets):
        temp.append([])

    # scatter the array elements
    # into the correct bucket
    for i in range(len(arr)):
        diff = (arr[i] - min_ele) / rnge - int((arr[i] - min_ele) / rnge)

        # append the boundary elements to the lower array
        if (diff == 0 and arr[i] != min_ele):
            temp[int((arr[i] - min_ele) / rnge) - 1].append(arr[i])

        else:
            temp[int((arr[i] - min_ele) / rnge)].append(arr[i])

    # Sort each bucket individually
    for i in range(len(temp)):
        if len(temp[i]) != 0:
            temp[i].sort()

    # Gather sorted elements
    # to the original array
    k = 0
    for lst in temp:
        if lst:
            for i in lst:
                arr[k] = i
                k = k + 1

# INITIAL INPUTS

print("Write to file name:")
f_name = input()
f_name = f_name + '.csv' #here the code makes the file a CSV format

print("Number of lists generated:")
run = int(input())

print("List length:")
list_len = int(input())

# FILE AND OTHER
f = open(f_name, 'w', newline='')
writer = csv.writer(f)
header = ["list", "bubble", "selection", "insertion", "quick", "merge", "heap", "count", "radix", "bucket"]
writer.writerow(header)
times = []
output_line = []
a = []

# WHERE THE PROGRAM IS BEING EXECUTED
while run:
    # INITIAL EDITS
    times.clear()
    output_line.clear()
    a.clear()

    # RANDOM LIST GENERATION

    # FULL RANGE RANDOM
    for i in range(list_len):
        a.append(i)
    random.shuffle(a)

    # FEW UNIQUE LISTS
    #mm = random.randint(0, 99)
    #mn = mm + random.randint(1,4)
    #for i in range(list_len):
    #    a.append(random.randint(mm, mn))

    # ALMOST SORTED
    #for i in range(list_len):
    #    a.append(i)
    #mm = random.choice(a)
    #mn = random.choice(a)
    #nn = a[mm]
    #a[mm] = a[mn]
    #a[mn] = nn

    # REVERSE SORTED
    #for i in range(list_len):
    #    a.append(list_len-i-1)

    # SORTED
    #for i in range(list_len):
    #    a.append(i)

    #print(a)

    # SORT LISTS

    # BUBBLE_SORT
    t_start = time.perf_counter_ns()
    bubble(a, len(a))
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)
    #print((t_end-t_start)/1000000000)

    # SELECTION_SORT
    t_start = time.perf_counter_ns()
    selection(a, len(a))
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # INSERTION_SORT
    t_start = time.perf_counter_ns()
    insertion(a, len(a))
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # QUICK_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    quickSort1(b, 0, len(a)-1)          #quickSort or quickSort1, quickSort1 is using an iterative approach instead of recursion
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # MERGE_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    mergeSort(b, 0, len(a)-1)
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # HEAP_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    heapSort(b)
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # COUNT_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    count_sort(b)
    t_end = time.perf_counter_ns()
    times.append((t_end-t_start)/1000000000)

    # RADIX_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    radixSort(b)
    t_end = time.perf_counter_ns()
    times.append((t_end - t_start) / 1000000000)

    # BUCKET_SORT
    b = a.copy()
    t_start = time.perf_counter_ns()
    bucketSort(b, list_len//2)
    t_end = time.perf_counter_ns()
    times.append((t_end - t_start) / 1000000000)

    # WRITING_TO_FILE
    output_line.append(list_len)
    for i in range(len(times)):
        output_line.append(times[i])
    writer.writerow(output_line)

    run -= 1

f.close()
