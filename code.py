import csv
'''
with open('sequences_table.csv','r') as seq_file:
    csv_reader = csv.DictReader(seq_file)

    list = []
    trobat = False

    for seq in csv_reader:
        for j in range(len(list)):
            if seq['Geo_Location'] == list[j][0]:
                trobat = True
                list[j].append(seq['Length'])
                j = len(list)-1
        if trobat == False:
            list.append([seq['Geo_Location'],seq['Length']])
        trobat = False
    #print(list)

def partition(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        # If the current value we're looking at is larger than the pivot
        # it's in the right place (right side of pivot) and we can move left,
        # to the next element.
        # We also need to make sure we haven't surpassed the low pointer, since that
        # indicates we have already moved all the elements to their correct side of the pivot
        while low <= high and array[high] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low] <= pivot:
            low = low + 1

        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
        if low <= high:
            array[low], array[high] = array[high], array[low]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start], array[high] = array[high], array[start]

    return high
#And finally, let's implement the quick_sort() function:

def quick_sort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)

for i in range(len(list)-1):
    quick_sort(list[i],1,len(list[i])-1)

print(list)
