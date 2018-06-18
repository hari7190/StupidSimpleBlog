# Merge Sort

input_arr = [1, 2, 2221, 4, 5, 643, 13, 22, 45]

print("Input array ->", input_arr)

# MergeSort(arr[], l,  r)
# If r > l
# 1. Find the middle point to divide the array into two halves:
#       middle m = (l+r)/2
# 2. Call mergeSort for first half:
#       Call mergeSort(arr, l, m)
# 3. Call mergeSort for second half:
#       Call mergeSort(arr, m+1, r)
# 4. Merge the two halves sorted in step 2 and 3:
#       Call merge(arr, l, m, r)

def mergeSort(input_arr):
    if(len(input_arr) > 1):
        mid = len(input_arr)//2
        lefthalf = input_arr[:mid]
        righthalf = input_arr[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i = 0
        j = 0
        k = 0

        while(i < len(lefthalf) and j < len(righthalf)):
            if(lefthalf[i] < righthalf[j]):
                input_arr[k] = lefthalf[i]
                i = i + 1
            else:
                input_arr[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while(i < len(lefthalf)):
            input_arr[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while(j < len(righthalf)):
            input_arr[k] = righthalf[j]
            j = j + 1
            k = k + 1

    print("Merging", input_arr)




mergeSort(input_arr)
