
import random as SystemRandom

generateur = SystemRandom() # Génere de manière plus sécurisée

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

# Fonction d'exponentation modulaire rapide
def exponentation_rapide(a, exp, mod):
    """
    Args:
        a (int): valeur que l'on veut monter à la puissance
        exp (int): puissance souhaitée
        mod (int): valeur definisant le corps Zp considéré

    Returns:
        result: resultat de la division modulaire de a**exposant par n
    """

    a = a % mod

    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * a) % mod
        exp = exp // 2
        a = (a * a) % mod
    return result

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
    
    if pow(a, exposant, n) == 1: #positive one
        return True
        
    while exposant < n - 1:
        if pow(a, exposant, n) == n - 1: #negative one
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
