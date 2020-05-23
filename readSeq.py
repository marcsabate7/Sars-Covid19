
def completeList():
    with open('sequences.csv','r') as seq_file:
        csv_reader = csv.DictReader(seq_file)
    
        list = []
        trobat = False

        for seq in csv_reader:
            regio = seq['Geo_Location'].split(':')
            for j in range(len(list)):
                if  list[j][0].find(regio[0])!=-1 and regio[0]!='':
                    trobat = True
                    list[j][1].append(int(seq['Length']))
                    j = len(list)-1
            if trobat == False and seq['Geo_Location']!='':
                list.append([regio[0],[int(seq['Length'])]])
            trobat = False
    return list
