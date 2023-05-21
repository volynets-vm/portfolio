from Pr import Pr
def ProfileMostProbablePattern(Text,k,Profile):
    n = len(Text)
    pros = {}
    for i in range(n-k+1):
        kmer = Text[i:i+k]
        pros[kmer] = Pr(kmer, Profile)
    m = max(pros.values())
    pmpp = Text[0:k]
    for kmer in pros:
        if pros[kmer] == m:
            pmpp = kmer
            break
    return pmpp
