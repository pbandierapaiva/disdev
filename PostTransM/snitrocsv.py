
posfile = open('SNitrosylationPositive.csv')
negfile = open('SNitrosylationNegative.csv')
outfile = open('nitroseqs.txt','w')

while True:
    line = posfile.readline()
    if line=='':
        break
    line = line.strip()
    partes = line.split('\t')
    
    for i in range(0,len(partes),3):
        outfile.write("1 "+partes[i+2]+"\n")

    