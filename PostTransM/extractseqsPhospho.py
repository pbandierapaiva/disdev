import pandas as pd


sitios = pd.read_pickle('phospho.pickle').astype({'ACC_ID':str,'LOC':int})
sitios.LOC = sitios.LOC-1

seqs = pd.read_pickle('seqs.pickle')

out = open("phosphoseqs.txt","w")
N=20


for i,rowSeq in seqs.iterrows():
    acc = rowSeq['ACC_ID']
    seq = rowSeq['SEQ']

    listInd = [] # indices de todas as Y
    for ind in range(len(seq)):
        if seq[ind]=="Y":
                if ind>=N and ind<=len(seq)-N:
                    listInd.append(ind)
                    
    sits = sitios[sitios.ACC_ID==acc]
    
    for locY in listInd:
        if locY in list(sits.LOC): # é sítio de fosforilação
            out.write("1 ")
        else:
            out.write("0 ")
        out.write(seq[locY-N:locY+N+1]+"\n")

out.close()    