def Pr(Text, Profile):
    p = 1
    for i in range(len(Text)):
        p *= Profile[Text[i]][i]
    return p
