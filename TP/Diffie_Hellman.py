"""Echange de clé par diffie-hellman
"""

from random import randint
from mathsalgo import pseudo_gen_premier
from lecteur_de_fichiers import ouputfiles
import os


pwd = os.path.dirname(__file__)
file = os.path.join(pwd, "files")
subfile = "Diffie_Hellman"
 
def diffie_hellman(bits = 512):
 
    # Both the persons will be agreed upon the 
    # public keys G and P 
    # A prime number P is taken 
    P = pseudo_gen_premier(bits)
    rand = pseudo_gen_premier(128)
    # A primitve root for P, G is taken
    g = 2
    while True and g < (P-1):
        q = (P-1)//2 
        # si l'ordre est différent de 1,2 et q alors g est générateur dans Zp
        # #if g*g % P != 1 and fastexpo(g,q,P) != 1: 
        if pow(g, g, P) != 1 and pow(g, q, P) != 1:
            break
        else:
            g +=1
    G = g
      
    print(f"Le nombre premier P généré est: {P}")
    print(f"L'élément générateur G de Zp* est: {G}")
     
    # Alice will choose the private key a 
    a = randint(2, rand)
    print(f"La clé public d'Alice est: {a}")
     
    # gets the generated key
    AliceKey = int(pow(G,a,P))  
     
    # Bob will choose the private key b
    b = randint(2, rand)
    print('La clé privée de Bob est: {b}')
    
    # gets the generated key
    sharekey = int(pow(G,b,P))  
     
    # Secret key for Alice 
    ka = int(pow(sharekey,a,P))
     
    # Secret key for Bob 
    kb = int(pow(AliceKey,b,P))
     
    A = f"La clé echangé coté Alice est : {ka}\n La clé privée d'Alice est {a}"
    B = f"La clé echangé coté Bob est : {kb}\n La clé privée de Bob est {b}"
    print("Alice Key = Bob Key?:",ka==kb)
    
    fic_A = "dh_Alice.txt"
    fic_B = "dh_Bob.txt"
    ouputfiles(A, subfile, fic_A)
    ouputfiles(B, subfile, fic_B)

    return A, B

if __name__ == "__main__":
    A, B = diffie_hellman()
  
