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
