# coding: utf-8
import random

generateur = random.SystemRandom() # Génere de manière plus sécurisée 
""""
========================================================================================================================
Algorithme de décomposition d'un entier en produit de facteurs premiers
========================================================================================================================
"""
def decomposition(n):
    """Cette fonction decompose un entier en produit de facteurs premiers

    Args:
        n (double): entier à decomposer

    Returns:
        list: (facteurs, exposant)
    """

    facteurs = [] #liste des facteurs premiers
    i = 2
    while i <= n:
        if n % i == 0:
            facteurs.append(i)
            n //= i
        else:
            i += 1
       # facteurs += [n]
    #print(set(facteurs))
    #print(facteurs[0]**facteurs.count(facteurs[0]))
    xult = sorted([(i, facteurs.count(i)) for i in set(facteurs)])

    return xult 


"""
=======================================================================================================================
Fonction d'exponentiation modulaire rapide
Cette fonction utilise l'exponentiation rapide pour calculer a^e mod p
========================================================================================================================
"""
def expo_rapide_mod(a,exposant,n):
    """fonction d'exponentiation modulaire rapide

    Args:
        a (double): valeur dont on veut les puissances
        exposant (double): exposant utilisé
        n (double): valeur definisant le corps Zp considéré

    Returns:
        double: xte de la division modulaire de a**exposant par n
    """

    #Initialisation

    if(a < 0 or exposant < 1 or n < 1):
        print("erreur: a doit etre un entier positif ; e et p doivent etre des entiers  strictement positifs")
    elif(a > n):
        print("erreur: l'entier a est supérieur à p ce qui est problématique")
    else:
        pass

    exponentiation = 1
    #calcul de l'exponentiation
    while(exposant > 0):
        if(exposant % 2 == 1):
            exponentiation = ((exponentiation * a) % n)
       # print(exponentiation)
        exposant = exposant // 2
        #print(exposant)
        a = a**2 % n

    return exponentiation

"""
==========================================================================================================================
Algorithme qui détermine l'inverse d'un entier par euclide etendu avec calcul de phi(n) et decomposition en nombre premier
==========================================================================================================================
"""
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def inverse(a, m):
    g, x, y = egcd(a, m) #g ici represente notre pgcd
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        r = x % m
        return r

"""def inverse(a, p):
    Cette foncion retourne l'inverse d'un entier dans un corps Zp

    Args:
        a (double): entier dont on veut l'inverse
        p (double): valeur qui defini notre corps Zp

    Returns:
        inv double: inverse de a
    if(a < 0 or p < 1):
        print("erreur: a et p doivent etre des entiers  strictement positifs")
    elif(a > p):
        print("erreur: l'entier a est supérieur à p ce qui est problématique")
    else:
        pass
    decomp = []
    phi = 1
    decomp = decomposition(p)
    
    #print(decomp[1][1]), ici on recupère la valeur de phi à partir de la decomposition en produit de facteurs premiers
    for i in list(range(0, len(decomp))):
        phi = phi * ((decomp[i][0] - 1) ** decomp[i][1])

    inv = pow(a, phi-1, p)

    return inv
"""


"""
=======================================================================================================================
Algorithme qui doit vérifier si un entier p est un nombre premier avec une précision demandée(un nombre d'itérations)
========================================================================================================================
"""
def simple_miller(n, a):
    """test simple sur un facteurs (a**(n-1)/2**k - 1) ou (a**(n-1)/2**k + 1)

    Args:
        n (double): entier dont on veut verifier la primalité
        a (double): valeur aléatoire comprise entre 1 et n-1

    Returns:
        boolean: True si prime et False si composite
    """
    exposant = n - 1

    #Tant que exposant est pair, on divise par 2
    while not exposant & 1: 
        exposant >>= 1
    
    if expo_rapide_mod(a, exposant, n) == 1: #positive one
        return True
        
    while exposant < n - 1:
        if expo_rapide_mod(a, exposant, n) == n - 1: #negative one
            return True
            
        exposant <<= 1
        
    return False

  
def miller_rabin(n, k=40):
    """Fonction de test de primalité de Rabin-Miller avec k itérations

    Args:
        n (double): entier dont on veut verifier la primalité
        k (double, optional): nombre d'itérations. Defaults to 40.

    Returns:
        boolean: True pour prime et False pour composite
    """ 

    for i in range(k):
        a = generateur.randrange(2, n - 1)
        if not simple_miller(n, a):
            return False
            
    return True

def pseudo_gen_premier(nombre_de_bits):
    """Pseudo generateur de nombx premiers sur n bits

    Args:
        nombre_de_bits (double): nombre de bits 

    Returns:
        double: nombre premier sur n bits
    """
    #startTime = time.time()
    while True:
        # avec safeprime impair.
        safeprime = (generateur.randrange(1 << nombre_de_bits - 1, 1 << nombre_de_bits) << 1) + 1
        if miller_rabin(safeprime) and miller_rabin((safeprime-1)//2):
            #print(f"Completed in {time.time() - startTime} seconds.")
            return safeprime

if __name__ == "__main__" :
    print(egcd(2500, 500))