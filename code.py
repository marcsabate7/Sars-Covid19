import csv

with open('sequences.csv','r') as seq_file:
    csv_reader = csv.DictReader(seq_file)

    list = []
    trobat = False

    for seq in csv_reader:
        for j in range(len(list)):
            if seq['Geo_Location'] == list[j]:
                trobat = True
                j = len(list)-1
        if trobat == False:
            list.append(seq['Geo_Location'])
        trobat = False

    print(list)
'''
import csv

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

    print(list)
'''
