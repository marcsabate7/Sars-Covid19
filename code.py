import csv
from Bio import SeqIO


def completeList():
    with open('sequences.csv','r') as seq_file:                                         # obrim el csv per tal de treure la informacio de cada pais
        csv_reader = csv.DictReader(seq_file)                                           # utilitzem el metode DictReader per poder accedir a les longituds de cada pais en forma de diccionari                    

        list = []
        trobat = False

        for seq in csv_reader:
            for j in range(len(list)):
                if seq['Geo_Location'] == list[j][0]:                                   # si el pais que estem llegint ya esta a la llista afegirem una nova londitud
                    trobat = True
                    list[j][1].append(int(seq['Length']))
                    j = len(list)-1
            if trobat == False:                                                         # si el pais actual no hi es a la llista afegirem el pais i la longitud
                list.append([seq['Geo_Location'],[int(seq['Length'])]])
            trobat = False
    return list

gap_penalty = -1
match_award = 1
mismatch_penalty = -1

def zeros(rows, cols):
    
    retval = []                                                                         # Define an empty list
    for x in range(rows):                                                               # Set up the rows of the matrix
        retval.append([])                                                               # For each row, add an empty list
        for y in range(cols):                                                           # Set up the columns in each row
            retval[-1].append(0)                                                        # Add a zero to each column in each row
    return retval                                                                       # Return the matrix of zeros

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def needleman_wunsch(seq1,seq2):                                                        # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    score = zeros(m+1, n+1)                                                             # Generate matrix of zeros to store scores
   
    # Calculate score table
    
    for i in range(0, m + 1):                                                           # Fill out first column
        score[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):                                                           # Fill out first row
        score[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):                                                           # Fill out all other values in the score matrix
        for j in range(1, n + 1):                                                       # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)                                    # Record the maximum score from the three possible scores calculated above
    return score[m][n]



def passer(list):
    array = []
    for i in range(50):
        for j in range(i+1,50):
            numSimil = needleman_wunsch(list[i][3],list[j][3])
            array.append([list[i][0],list[j][0],numSimil])
    print(array)
                
        
    
        
def arnGen(arr):
    for seq_record in SeqIO.parse("sequences2.fasta", "fasta"):
        for i in range(len(arr)):
            if arr[i][2]==seq_record.id:
                temp= str(seq_record.seq)
                if len(temp)>1000:
                    temp = temp[:1001]
                arr[i].append(temp)
    return arr


def accesionCalculator(list):
    #print(list)
    with open('sequences.csv','r') as seq_file:
        csv_reader = csv.DictReader(seq_file)


        for seq in csv_reader:
            for i in range(len(list)):
                if seq['Geo_Location']==list[i][0] and int(seq['Length'])==list[i][1]:
                    list[i].append(seq['Accession'])   
                while len(list[i]) >=4:
                    list[i].pop()
    return list


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
    
    accesList = accesionCalculator(list)
    return accesList
    

if __name__=="__main__":                                                            # funcio MAIN
    list = completeList()                                                           # rebrem la llista de paisos amb totes les longituds de cada pais en concret
    arr = modify(list)                                                              # ordenem totes les longituds de cada pais 
    accesList = calculMediana(arr)                                                  # calculem la mediana de cada pais i seguidament amb la funcio accesionCalculator calculem el seu accesion 
    completeList = arnGen(accesList)                                                # amb la funcio argen obtenim la sequuencia de cada pais en concret
    passer(completeList)                                                            # calculem el aliniament de sequencies
