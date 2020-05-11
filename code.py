import csv
from Bio import SeqIO


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

gap_penalty = -1
match_award = 1
mismatch_penalty = -1

def zeros(rows, cols):
    # Define an empty list
    retval = []
    # Set up the rows of the matrix
    for x in range(rows):
        # For each row, add an empty list
        retval.append([])
        # Set up the columns in each row
        for y in range(cols):
            # Add a zero to each column in each row
            retval[-1].append(0)
    # Return the matrix of zeros
    return retval

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def needleman_wunsch(seq1,seq2):
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    return score[m][n]



def passer(list):
    array = []
    for i in range(len(list)):
        for j in range(i+1,len(list)):
            numSimil = needleman_wunsch(list[i][3],list[j][3])
            array[i].append(numSimil)
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
    

if __name__=="__main__":
    list = completeList()
    arr = modify(list)
    accesList = calculMediana(arr)
    completeList = arnGen(accesList)
    passer(completeList)
