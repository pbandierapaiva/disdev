import pandas as pd

from Bio import SeqIO
from Bio import Entrez
Entrez.email = "paiva@unifesp.br"


def fetchProt(acc):
    handle = Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()
    return str(record.seq)
    


pho = pd.read_csv("/data/datasets/Phosphorylation_site",sep='\t')

listaP = pho[['ACC_ID','MOD_RSD']].copy()
listaP = listaP[listaP['MOD_RSD'].str.startswith('Y')].reindex()

out = open('erros.log','w')


seqDF = None    #  pd.DataFrame()
sitios = pd.DataFrame({'ACC_ID':[],'LOC':[]})
seqs = pd.DataFrame({'ACC_ID':[],'SEQ':[]})
# tamanho da janela N
N = 2
for i,linha in listaP.iterrows():
    loc = linha['MOD_RSD']
    acc = linha['ACC_ID']
    
    l = int(loc[1:].split('-')[0])
    print(loc,acc)
    
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

    sitios = sitios.append({'ACC_ID':acc,'LOC':l}, ignore_index = True)
    if seq:
        seqs = seqs.append({'ACC_ID':acc,'SEQ':seq}, ignore_index = True)

#     input(seq[l-N-1:l+N])
out.close()        
sitios.to_pickle('phospho.pickle')
seqs.to_pickle('seqs.pickle')