import pandas as pd


sitios = pd.read_pickle('nitros.pickle').astype({'ACC_ID':str,'LOC':int})
sitios.LOC = sitios.LOC-1   # transforma os LOC para 0 -based

seqs = pd.read_pickle('seqs.pickle')

out = open("snitroseqs.txt","w")
N=20
seqsDisponiveis = list(seqs.ACC_ID)

for i,rowSeq in seqs.iterrows():
    acc = rowSeq['ACC_ID']
    seq = rowSeq['SEQ']
    
    if acc not in seqsDisponiveis:
        continue
        
    listInd = [] # indices de todas as C
    for ind in range(len(seq)):
        if seq[ind]=="C":
                if ind>=N and ind<=len(seq)-N:
                    listInd.append(ind)
                    
    sits = sitios[sitios.ACC_ID==acc]
    
    for locC in listInd:
        if locC in list(sits.LOC): # é sítio de nitrosilação
            out.write("1 ")
        else:
            out.write("0 ")
        out.write(seq[locC-N:locC+N+1]+"\n")

out.close()    