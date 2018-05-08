# Bubble Sort

input_arr = [1, 2, 2221, 4, 5, 643, 13, 22, 45]

print("Input array ->", input_arr)

for x in range(0, len(input_arr)):
    for y in range(0, len(input_arr)-x-1):
        if input_arr[y] > input_arr[y + 1]:
            input_arr[y], input_arr[y + 1] = input_arr[y + 1], input_arr[y]

print("Sorted array ->", input_arr)