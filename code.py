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
                    list[j][1].append(int(seq['Length']))
                    j = len(list)-1
            if trobat == False:
                list.append([seq['Geo_Location'],[int(seq['Length'])]])
            trobat = False
    return list

def modify(list):
    for i in range(len(list)):
        list[i][1].sort()
    
    return list

def calculMediana(arr):
    list = []
    for i in range(len(arr)-1):
        long = len(arr[i][1])
        if long % 2 != 0:
            total = int(round((long/2)))
            num = arr[i][1]
            numbo = num[total-1]
        else:
            total = int((long/2)+1)
            num = arr[i][1]
            numbo = num[total-1]
        total = 0
        list.append([arr[i][0],numbo])
    print(list)
    
    
if __name__=="__main__":
    list = completeList()
    arr = modify(list)
    calculMediana(arr)

