def Count(Motifs):
    count = {}
    k = len(Motifs[0])
    for symbol in "ACTG":
        count[symbol] = [0]*k
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j]+=1
    return count
