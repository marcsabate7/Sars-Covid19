import csv
from Bio import SeqIO


def completeList():
    with open('sequences.csv','r') as seq_file:                                         # obrim el csv per tal de treure la informacio de cada pais
        csv_reader = csv.DictReader(seq_file)                                           # utilitzem el metode DictReader per poder accedir als elements  de cada linia del csv en forma de diccionari                    

        list = []
        trobat = False

        for seq in csv_reader:                                                          # recorrem el csv
            for j in range(len(list)):
                if seq['Geo_Location'] == list[j][0]:                                   # si el pais que estem llegint ya esta a la llista afegirem una nova longitud
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
    
    retval = []                                                                         # defineix una llista buida
    for x in range(rows):                                                               # indica les linies de la matriu
        retval.append([])                                                               # per cada linia afegeix una llista
        for y in range(cols):                                                           
            retval[-1].append(0)                                                        # afegeix un 0 a cada culumna de cada fila
    return retval                                                                       # retorne la matriu de zeros

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def needleman_wunsch(seq1,seq2):                                                        
    n = len(seq1)                                                                       # guardem la llargada de les dos sequencies a comparar
    m = len(seq2)
    
    score = zeros(m+1, n+1)                                                             # genera una matriu de zeros per anar guardant els scores
   
    # Calculate score table
    
    for i in range(0, m + 1):                                                           # omple la primera columna
        score[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):                                                           # omple la primera linea
        score[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):                                                           # omple la matriu amb tots els valors
        for j in range(1, n + 1):                                                       # es calcula el score mirant les celes de adalt, a la esquerra i en diagonal
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)                                    # guarda el maxim score dels tres possibles
    return score[m][n]



def passer(list):
    array = []
    for i in range(len(list)):                                                          # utilitzem dos bucles aniuats per tal de comparar les sequencies totes amb totes i sense repetir cap
        for j in range(i+1,len(list)):
            numSimil = needleman_wunsch(list[i][3],list[j][3])
            array.append([list[i][0],list[j][0],numSimil])                              # anem afegint els resultats de la comparacio a la llista
    print(array)
                
        
    
        
def arnGen(arr):
    for seq_record in SeqIO.parse("sequences2.fasta", "fasta"):                     # llegim el fasta i agafem les sequencies que coincideicin amb el accesion de cada pais
        for i in range(len(arr)):
            if arr[i][2]==seq_record.id:
                temp= str(seq_record.seq)
                if len(temp)>1000:                                                  # nomes agafem les 1000 primeres lletres de la sequencia
                    temp = temp[:1001]
                arr[i].append(temp)
    return arr


def accesionCalculator(list):
    #print(list)
    with open('sequences.csv','r') as seq_file:                                     # llegim el csv per tal de buscar els que tenen al mateixa longitud i el mateix pais i aixi poder accedir al accesion
        csv_reader = csv.DictReader(seq_file)


        for seq in csv_reader:
            for i in range(len(list)):
                if seq['Geo_Location']==list[i][0] and int(seq['Length'])==list[i][1]:
                    list[i].append(seq['Accession'])                                # a la llista li afegim el accesion corresponent
                while len(list[i]) >=4:
                    list[i].pop()
    return list


def modify(list):
    for i in range(len(list)):                                                      # recorrem la llista
        list[i][1].sort()                                                           # ordenem l'apartat de la llista on es troben totes les longituds per cercar la mitjana
    
    return list


def calculMediana(arr):
    list = []
    for i in range(len(arr)):                                                       # cerquem la mitjana depenen de si el len de arr es parell o imparell i afegim a una llista el pais i la mitjana
        long = len(arr[i][1])
        if long % 2 != 0:
            num = arr[i][1][int(round(long/2))-1]
        else:
            num = arr[i][1][int((long/2)+1)-1]
        total = 0
        list.append([arr[i][0],num])
    
    accesList = accesionCalculator(list)                                            # cridem a aquesta funció per tal de calcular el accesion de cada pais
    return accesList
    

if __name__=="__main__":                                                            # funcio MAIN
    list = completeList()                                                           # cridem a la funció i rebrem la llista de paisos amb totes les longituds de cada pais en concret
    arr = modify(list)                                                              # ordenem totes les longituds de cada pais 
    accesList = calculMediana(arr)                                                  # calculem la mediana de cada pais i seguidament amb la funcio accesionCalculator calculem el seu accesion 
    completeList = arnGen(accesList)                                                # amb la funcio arGen obtenim la sequencia de cada pais en concret
    passer(completeList)                                                            # calculem el aliniament de sequencies
