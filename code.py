import csv


def completeList():
    with open('sequences.csv','r') as seq_file:
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
    return list

    
def ordenarArray(arr):
    for index in range(1, len(arr)):
        current = arr[index]
        position = index

        while position > 0 and arr[position-1] > current:
            arr[position] = arr[position-1]
            position -= 1

        arr[position] = current

    print(arr)
    
    
    
def modify(list):
    for i in range(len(list)):
        ordenarArray(list[i])

    
if __name__=="__main__":
    list = completeList()
    modify(list)
