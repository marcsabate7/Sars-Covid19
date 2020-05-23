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
