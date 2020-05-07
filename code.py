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


def accesionCalculator():
    


def modify(list):
    for i in range(len(list)):
        list[i][1].sort()
    
    return list

def calculMediana(arr):
    list = []
    for i in range(len(arr)):
        long = len(arr[i][1])
        if long % 2 != 0:
            num = arr[i][1][int(round(long/2))-1]
        else:
            num = arr[i][1][int((long/2)+1)-1]
        total = 0
        list.append([arr[i][0],num])
    #print(list)
    accesionCalculator(list)
    

if __name__=="__main__":
    list = completeList()
    arr = modify(list)
    calculMediana(arr)

