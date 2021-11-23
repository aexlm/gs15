"""fonction qui permet d'ouvrir un fichier quelconque par blocs de N bits.Pour faciliter les choses,
on pourra considérer que N=8k autrement,dit on pourra lire un fichier quelconque par blocs de k octets."""

import os

pwd = os.path.dirname(__file__)
file = os.path.join(pwd, "files")

def readplaintext(filename):
    fichiertxt = os.path.join(file, filename)
    if not os.path.exists(fichiertxt):
        print("fichier introuvable!!")
    else:
        pass
    with open(fichiertxt, "r") as f:
        cont = f.read()
        return cont

def ouputfiles(contenu, subfile, namefile):
    fichiertxt = os.path.join(file, subfile)
    fichiertxt = os.path.join(fichiertxt, namefile)
    if not os.path.exists(fichiertxt):
        with open(fichiertxt, "w+") as f:
            f.write(contenu)
    else:
        print(f"Update du repertoire {file}...")
        with open(fichiertxt, "w+") as f:
            f.write(contenu)

def ouputlog(contenu, subfile, namefile):
    fichiertxt = os.path.join(file, subfile)
    fichiertxt = os.path.join(fichiertxt, namefile)
    if not os.path.exists(fichiertxt):
        with open(fichiertxt, "a+") as f:
            f.write(contenu)
    else:
        print(f"Update du repertoire {file}...")
        with open(fichiertxt, "a+") as f:
            f.write(contenu)

if __name__ == "__main__":
    #contenu = 
    print(readplaintext("plaintext.txt"))
    #print(contenu)