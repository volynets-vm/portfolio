from Profile import Profile
from Score import score_motif
from pr_kmer import Profile_Most_Probable_Pattern
def GreedyMotifSearch(Dna, k ,t):
    best_motifs = []
    for i in range (0,t):
        best_motifs.append(Dna[i][0:k])
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1,t):
            P = Profile(Motifs)
            Motifs.append(Profile_Most_Probable_Pattern(Dna[j],k,P))
        if score_motif(Motifs) < score_motif(best_motifs):
            best_motifs = Motifs
    return best_motifs
t = int(input("enter numbers of rows: "))
k = int(input("enter your kmer: "))
dna = []
while len(dna)<t:
    dna += list(input().split(' '))
#print(dna)

num = 1
while num <=1000:
    Motifs = GreedyMotifSearch(dna, k, t)
    num+=1
    print("compiling")
print(Motifs)



