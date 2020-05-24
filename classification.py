
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
            print("S'han modificat els centres, ara son: \n") 
            print(list_randoms)
            control = []
        else: 
            list_randoms[i] = aux_random[i][0]



array = num_entrePaisos(medianes)
# INICI COMPROVACIÓ DE CENTRES #                                                # INICIALITZACIO CLASSIFICACIO
    k = 3                                                                           # es defineix un valor de k, els grups en els que organitzem 
    aux = array.copy()                                                              # aux s'inicialitza a array, per tal de no modificar mai la taula de les mostres originals
    list_randoms = random.sample(array,k)                                           # de tota la taula array se seleccionen 3 elements aleatoris
    aux_random = []                                                                 # aux_random guardara els k grups
    elimina_centres_de_aux()
    crear_grups()
    classifica_per_grups()
    #print(aux_random)
    anterior = list_randoms.copy()                                                  # es crea "anterior" amb els centres actuals

    trobat = True
    while trobat:
        nou_centre()                                                                # Busca nous millors centres de grup i repeteix el proces que en la inicialitzacio 
        aux_random = []                                                             # fins que es troben els mateixos centres, en dues voltes diferents
        aux = array.copy()                                                          # S'haura trobat la millor distribucio / classificacio de les mostres
        elimina_centres_de_aux()
        crear_grups()
        classifica_per_grups()
        #print(aux_random)
        if anterior == list_randoms:
            trobat = False
            print("Els centres han coincidit amb la volta anterior pertant s'ha acabat la classificació")
        anterior = list_randoms.copy()
