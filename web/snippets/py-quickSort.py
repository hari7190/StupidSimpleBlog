input_arr = [1, 2, 2221, 4, 5, 643, 13, 22, 45]

print("Input array ->", input_arr)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp

    temp = arr[i+1]
    arr[i+1] = arr[high]
    arr[high] = temp
    return i+1


def quickSort(arr, low, high):
    if low < high :
        pi = partition(arr, low, high)

        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)



quickSort(input_arr, 0, len(input_arr)-1)


print("Sorted array ->", input_arr)