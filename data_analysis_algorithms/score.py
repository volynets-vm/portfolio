from Consensus import Consensus
def Score(Motifs):
    consensus = Consensus(Motifs)
    k = len(consensus)
    score = 0
    for motif in Motifs:
        for j in range(k):
            if motif[j] != consensus[j]:
                score += 1
    return score
