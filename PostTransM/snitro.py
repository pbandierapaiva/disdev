import pandas as pd

from Bio import SeqIO
from Bio import Entrez
Entrez.email = "paiva@unifesp.br"


def fetchProt(acc):
    handle = Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()
    return str(record.seq)
    

posfile = open('SNitrosylationPositive.csv')
sitios = pd.DataFrame({'ACC_ID':[],'LOC':[]})
out = open('erros.log','w')

seqs = pd.read_pickle('seqs.pickle')

while True:
    line = posfile.readline()
    if line=='':
        break
    line = line.strip()
    partes = line.split('\t')
    
    for i in range(0,len(partes),3):
        acc = partes[i]
        loc = int(partes[i+1])
        sitios = sitios.append({'ACC_ID':acc,'LOC':loc}, ignore_index = True)
        if acc in set( seqs['ACC_ID'] ): # já baixou 
            seq=None
        else:
            print("Baixando ", acc)
            try:
                seq = fetchProt(acc)
            except:
                print("Erro FETCH")
                out.write( "Erro FETCH "+acc + "\n")
                continue
        if seq:
            seqs = seqs.append({'ACC_ID':acc,'SEQ':seq}, ignore_index = True)

out.close()        
sitios.to_pickle('nitros.pickle')
seqs.to_pickle('seqs.pickle')