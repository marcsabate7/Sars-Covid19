import csv
from Bio import SeqIO
import random


def completeList():
    with open('sequences_table.csv','r') as seq_file:                                               # obrim el csv per tal de treure la informacio de cada pais
        csv_reader = csv.DictReader(seq_file)                                                       # utilitzem el metode DictReader per poder accedir als elements  de cada linia del csv en forma de diccionari
    
        list = []
        trobat = False

        for seq in csv_reader:                                                                      # recorrem el csv
            regio = seq['Geo_Location'].split(':')
            for j in range(len(list)):
                if  list[j][0].find(regio[0])!=-1 and regio[0]!='':                                 # si el pais que estem llegint ya esta a la llista afegirem una nova longitud
                    trobat = True
                    list[j][1].append(int(seq['Length']))
                    j = len(list)-1
            if trobat == False and seq['Geo_Location']!='':                                         # si el pais actual no hi es a la llista afegirem el pais i la longitud
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
    with open('sequences_table.csv','r') as seq_file:                                               # llegim el csv per tal de buscar els que tenen al mateixa longitud i el mateix pais i aixi poder accedir al accesion
        csv_reader = csv.DictReader(seq_file)

        for seq in csv_reader:
            regio2 = seq['Geo_Location'].split(':')
            for i in range(len(medianes)):
                if medianes[i][0]==regio2[0] and int(seq['Length'])==medianes[i][1]:
                    medianes[i].append(seq['Accession'])                                            # a la llista li afegim el accesion corresponent
                while len(medianes[i]) >=4 :
                    medianes[i].pop()
    return medianes

def arnGen(medianes):
    for seq_record in SeqIO.parse("sequences.fasta", "fasta"):                                      # llegim el fasta i agafem les sequencies que coincideicin amb el accesion de cada pais
        for i in range(len(medianes)):
            if medianes[i][2]==seq_record.id:
                temp= str(seq_record.seq)
                if len(temp)>1000:                                                                  # nomes agafem les 1000 primeres lletres de la sequencia
                    temp = temp[:1000]
                medianes[i].append(temp)
    return medianes


# PROVA NEEDLEMAN-WUNSCH #

gap_penalty = -1
match_award = 1
mismatch_penalty = -1



def zeros(rows, cols):
    retval = []                                                                      # defineix una llista buida
    for x in range(rows):                                                            # indica les linies de la matriu
        retval.append([])                                                            # per cada linia afegeix una llista
        for y in range(cols):
            retval[-1].append(0)                                                     # afegeix un 0 a cada culumna de cada fila
    return retval

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty
   
score = zeros(1001,1001)

def needleman_wunsch(seq1, seq2):                                                   # genera una matriu de zeros per anar guardant els scores
    n = len(seq1)                                                                   # guardem la llargada de les dos sequencies a comparar
    m = len(seq2)
    
    for i in range(0, m + 1):                                                       # omple la primera columna
        score[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):                                                       # omple la primera linea
        score[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):                                                       # omple la matriu amb tots els valors
        for j in range(1, n + 1):                                                   # es calcula el score mirant les celes de adalt, a la esquerra i en diagonal
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)                                # guarda el maxim score dels tres possibles
    return score[m][n]

def num_entrePaisos(medianes):                                                      # recorre la taula medianes i realitza les comparacions tots amb tots amb needleman-wunsch
    array=[]                                                                        # els resultats es guarden a la taula array
    for x in range(len(medianes)):                                                                                      
        for y in range(x+1,len(medianes)):                                                                              
            output = needleman_wunsch(medianes[x][3],medianes[y][3])
            array.append([output,medianes[x][0],list[y][0]])
    return array

def elimina_centres_de_aux():                                                       # auxiliar seran totes les mostres a classificar segons el centre que tinguin mes aprop
    for i in range(len(list_randoms)):                                              # per tant, eliminem de les mostres els tres centres
        aux.remove(list_randoms[i])

def crear_grups():                                                                  # la llista aux_random incorpora els k grups
    for i in range(len(list_randoms)):                                              # es coloquen els centres al k grup corresponent
        aux_random.append([list_randoms[i]])


def classifica_per_grups():
                                                                                                    # la llista de mostres sense els centes " aux " es recorre per classificar
    for x in range(len(aux)):                                                                       # cada mostra segons la distancia a cadascun dels centres
        u = list_randoms[0][0]
        dos = list_randoms[1][0]
        tres = list_randoms[2][0]
        minim = min(abs(aux[x][0]-u), abs(aux[x][0]-dos), abs(aux[x][0]-tres))
        if minim == abs(aux[x][0]-u):
            aux_random[0].append(aux[x])
        elif minim == abs(aux[x][0]-dos):
            aux_random[1].append(aux[x])
        elif minim == abs(aux[x][0]-tres):
            aux_random[2].append(aux[x])


def nou_centre():
    control = []                                                                                    # de les mostres de cada grup se selecciona el millor centre
    result = 0                                                                                      # i es defineix novament els centres que tindra cada grup
    indexos = []

    for i in range(len(aux_random)):
        if len(aux_random[i]) > 2:
            for j in range(len(aux_random[i])):
                result = 0
                for h in range(len(aux_random[i])):
                    result = result + abs(aux_random[i][j][0] - aux_random[i][h][0])
                control.append(result)
            index = control.index(min(control))
            list_randoms[i] = aux_random[i][index]
            #print("S'han modificat els centres, ara son: \n") 
            #print(list_randoms)
            control = []
        else: 
            list_randoms[i] = aux_random[i][0]

    
if __name__=="__main__":                                                                                      
    list = completeList()                                                           
    medianes = array_pais_amb_len_mediana(modify(list))
    medianes = add_accessions(medianes)
    medianes = arnGen(medianes)
    array = num_entrePaisos(medianes)
    
    # INICI COMPROVACIÓ DE CENTRES #                                                # INICIALITZACIO CLASSIFICACIO
    k = 3                                                                           # es defineix un valor de k, els grups en els que organitzem 
    aux = array.copy()                                                              # aux s'inicialitza a array, per tal de no modificar mai la taula de les mostres originals
    list_randoms = random.sample(array,k)                                           # de tota la taula array se seleccionen 3 elements aleatoris
    aux_random = []                                                                 # aux_random guardara els k grups
    elimina_centres_de_aux()
    crear_grups()
    classifica_per_grups()
    anterior = list_randoms.copy()                                                  # es crea "anterior" amb els centres actuals
    cont_modificacions = 0
    trobat = True
    while trobat:
        nou_centre()                                                                # Busca nous millors centres de grup i repeteix el proces que en la inicialitzacio 
        aux_random = []                                                             # fins que es troben els mateixos centres, en dues voltes diferents
        aux = array.copy()                                                          # S'haura trobat la millor distribucio / classificacio de les mostres
        elimina_centres_de_aux()
        crear_grups()
        classifica_per_grups()
        #print(aux_random)
        cont_modificacions +=1
        if anterior == list_randoms:
            trobat = False
            print('\n')
            print("Els centres han coincidit amb la volta anterior pertant s'ha acabat la classificació\n")
            print("En el programa hi ha hagut un total de {} centres diferents\n".format(cont_modificacions))
            print("Els centres finals són:\n")
            for i in range(len(list_randoms)):
                print(list_randoms[i])
                print('\n')
            print("I els tres grups:")
            print('\n')
            for j in range(len(aux_random)):
                print(aux_random[j])
                print('\n')
        anterior = list_randoms.copy()
