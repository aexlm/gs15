import random
import os
from random import randint
from vote_machine.algos.generator import strong_prem_gen as gensafeprime, miller_rabin
from vote_machine.algos.maths import exponentation_rapide as fastexpo

a=random.randint(2,10)

#To fing gcd of two numbers
"""def gcd(a,b):
    if a<b:
        return gcd(b,a)
    elif a%b==0:
        return b
    else:
        return gcd(b,a%b)
"""
#For key generation i.e. large random number
"""def gen_key(q):
    key= random.randint(fastexpo(10,20),q)
    while gcd(q,key)!=1:
        key=random.randint(fastexpo(10,20),q)
    return key
"""
"""def fastexpo(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c;
        y=(y*y)%c
        b=int(b/2)
    return x%c"""


def initialisation(nombre_bits_sprime = 512):
    """Generation d'un safe prime sprime et d'un élément générateur de Zp

    Args:
        nombre_bits_p (int): nombre de bits de sprime = 512 bits par défaut

    Returns:
        int: (sprime,generator)
    """
    sprime = gensafeprime(nombre_bits_sprime)


    #Verifions si sprime est fortement premier
    if miller_rabin((sprime-1)//2):
        pass
    else:
        print("Not safe prime")

    #Utilisation du théorème de lagrange
    generator = 2
    while True and generator < (sprime-1):
        q = (sprime-1)//2

        # si l'ordre est différent de 1,2 et q alors generator est générateur dans Zp
        #if generator*generator % sprime != 1 and fastexpo(generator,q,sprime) != 1:
        if pow(generator, generator, sprime) != 1 and pow(generator, q, sprime) != 1:
            break
        else:
            generator +=1

    return sprime,generator

#print(initialisation())
#print(f"Completed in {time.time() - startTime} seconds.")


def ElGamalKeygeneration(sprime,generator):
    """Fonction qui va génerer notre couple de clé public/privé sécurisée par le problème du logarithme discret


    Args:
        sprime (double): Nombre fortement premier de 512 bits par défaut
        generator (double): élément générateur de l'ensemble Zp*

    Returns:
        (double, double): (Ephemeral public key, private key)
    """

    a = randint(2,sprime-2)
    KE = fastexpo(generator,a,sprime) #ephemeral Key, change pour chaque signature
    out = f"La clé publique générée est : {KE}" + f" et la clé privée générée est: {a}"

    return KE,a

#For asymetric encryption
def encryption(msg,q,h,g):
    """ElGamal Encryption

    Args:
        msg (string): plaintext message
        q (double): Represente le corps Zp
        h (double): clé publique de celui qui va déchiffrer
        g (double): element générateur de Zp

    Returns:
        ciphertext,p: message chiffré, clé publique de celui qui a chiffré
    """
    # p ici c'est la clé public de l'émetteur (celui qui chiffre)
    # k c'est la clé secrète de l'emetteur (celui qui chiffre)
    # s ici c'est la clé partagée
    ciphertext=[]
    #k=gen_key(q)
    p,k=ElGamalKeygeneration(q, g)
    s=fastexpo(h,k,q)
    #p=fastexpo(g,k,q)
    for i in range(0,len(msg)):
        ciphertext.append(msg[i])
    print("g^k used= ",p)
    print("g^ak used= ",s)
    for i in range(0,len(ciphertext)):
        ciphertext[i]=s*ord(ciphertext[i])
    return ciphertext,p

#For decryption
def decryption(ciphertext,p,key,q):
    """
    q, c'est le corps Zp dans lequel le message a été chiffré
    key, ici c'est la clé secrète du recepteur (celui qui déchiffre)
    h, ici c'est la clé partagée
    p, c'est la clé publique de celui qui a chiffré

    """
    plaintext=[]
    h=fastexpo(p,key,q)
    for i in range(0,len(ciphertext)):
        plaintext.append(chr(int(ciphertext[i]/h)))
    return plaintext

#############TEST##############

if __name__ == '__main__':
    bits = 256
    q,g=initialisation(bits)
    h,key=ElGamalKeygeneration(q,g)
    # h/key étant le couple clé publique/clé privée du recepteur (celui qui déchiffre)
    msg=input("Enter the message: ")
    #q=random.randint(fastexpo(10,20),fastexpo(10,50))
    #g=random.randint(2,q)
    #key=gen_key(q)
    #h=fastexpo(g,key,q)
    print("g used=",g)
    print("g^a used=",h)
    ciphertext,p=encryption(msg,q,h,g)
    print("Original Message=",msg)
    print("Encrypted Maessage=",ciphertext)
    plaintext=decryption(ciphertext,p,key,q)
    d_msg=''.join(plaintext)
    print("Decryted Message=",d_msg)

"""
Public Parameter: A trusted third party publishes a large prime number p and a generator g.

1.Key Generation:

Alice chooses a secret key 1<=a<=p-1.
Computes A=g^a mod p.
Alice se1<=k<=p and the public key pk=(p, g, A) to Bob.
2. Encryption:

Bob chooses a unique random number key 1<=k<=p-1.
Uses Alice’s public key pk and key k to compute the ciphertext (c1,c2) =Epk(m) of the plaintext 1<=m<=p-1 where c1=g^k mod p and c2=m.A^k mod p.
The ciphertext (c1,c2) is sent to Alice by Bob.
3. Decryption:

Alice computes x=c1^a mod p  and its inverse x^-1 with the extended Euclidean algorithm.
Computes the plaintext m’=Dsk(c1,c2)= x^-1.c2 mod p where m’=m.
"""