from Count import Count
def Consensus(Motifs):
    consensus = ""
    k = len(Motifs[0])
    count = Count(Motifs)
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus 
