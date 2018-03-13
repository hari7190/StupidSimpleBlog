
# Linear Search - Python

input_arr = [1, 2, 3, 4, 5, 643, 13, 22, 45]

to_find = 45

for x in range(0, len(input_arr)):
    if(input_arr[x] == to_find):
        print("Element present at : " + str(x))

# Output here - Element present at : 8

# Time complexity - O(n)
