import csv
from Bio import SeqIO


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

def modify(list):
    for i in range(len(list)):                                                     
        list[i][1].sort()          
    return list

def array_pais_amb_len_mediana(list):
    medianes=[]
    for i in range(len(list)):
        val_mediana_temp = list[i][1][len(list[i][1])//2]
        medianes.append([list[i][0],val_mediana_temp])
    return medianes

def add_accessions(medianes):
    trobat = False
    with open('sequences.csv','r') as seq_file:
        csv_reader = csv.DictReader(seq_file)

        for seq in csv_reader:
            regio2 = seq['Geo_Location'].split(':')
            for i in range(len(medianes)):
                if medianes[i][0]==regio2[0] and int(seq['Length'])==medianes[i][1]:
                    medianes[i].append(seq['Accession'])   
                while len(medianes[i]) >=4 :
                    medianes[i].pop()
    return medianes

def arnGen(medianes):
    for seq_record in SeqIO.parse("sequences2.fasta", "fasta"):                     
        for i in range(len(medianes)):
            if medianes[i][2]==seq_record.id:
                temp= str(seq_record.seq)
                if len(temp)>1000:                                                  
                    temp = temp[:1000]
                medianes[i].append(temp)
    return medianes


gap_penalty = -1
match_award = 1
mismatch_penalty = -1


def zeros(rows, cols):
    retval = []
    for x in range(rows):
        retval.append([])
        for y in range(cols):
            retval[-1].append(0)
    return retval

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty
   
score = zeros(1001,1001)

def needleman_wunsch(seq1, seq2):
    n = len(seq1)  
    m = len(seq2)
    
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)
    return score[m][n]

def num_entrePaisos(medianes):
    array=[]
    for x in range(len(medianes)):                                                                              # len(medianes))
        for y in range(x+1,len(medianes)):                                                                      # len(medianes))
            output = needleman_wunsch(medianes[x][3],medianes[y][3])
            array.append([output,medianes[x][0],list[y][0]])
    return array

if __name__=="__main__":                                                                                   
    list = completeList()                                                           
    medianes = array_pais_amb_len_mediana(modify(list))
    #print(medianes)
    #print('\n')
    medianes = add_accessions(medianes)
    medianes = arnGen(medianes)
    #print (medianes)
    array = num_entrePaisos(medianes) 
    print(len(array))
    #print(array)
