import csv


with open('sequences_table.csv','r') as seq_file:
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

## ORDENEM LIST I PRINTEM ##

for i in range(len(list)):
    list[i][1].sort()
#  print(list[i])
#   print('\n')
#print('\n')


## TAULA DE MEDIANES I PAISOS ##

medianes=[]
for i in range(len(list)):
    val_mediana_temp = list[i][1][len(list[i][1])//2]
    medianes.append([list[i][0],val_mediana_temp])
#print(medianes)


## AFEGIM ACCESSION A TAULA MEDIANES I PAISOS ##

with open('sequences_table.csv','r') as seq_file:
    csv_reader = csv.DictReader(seq_file)

    for seq in csv_reader:
        for i in range(len(medianes)):
            if seq['Geo_Location']==medianes[i][0] and int(seq['Length'])==medianes[i][1]:
                medianes[i].append(seq['Accession'])   
            while len(medianes[i]) >=4 :
                medianes[i].pop()
                
print('\n')
#print(medianes)


## IMPRIMIR SEQUENCIES DE ACCESSIONS SELECCIONATS ##

from Bio import SeqIO

for seq_record in SeqIO.parse("sequences.fasta", "fasta"):
    for i in range(len(medianes)):
        if medianes[i][2]==seq_record.id:
            temp= str(seq_record.seq)
            if len(temp)>1000:
                temp = temp[:1001]
            medianes[i].append(temp)
            
            
print(medianes)

