"""Génération d'un couple clé publique / clé privée avec EL-Gamal
"""
from lecteur_de_fichiers import ouputfiles
from random import randint
import time
from sha256 import hash256
from mathsalgo import pseudo_gen_premier as gensafeprime, miller_rabin, expo_rapide_mod as fastexpo, hexatodecimal
import os

pwd = os.path.dirname(__file__)
file = os.path.join(pwd, "files")
subfile = "ElGamal"
#startTime = time.time()
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
      
    return (sprime,generator)

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
  KE = pow(generator,a,sprime) #ephemeral Key, change pour chaque signature
  out = f"La clé publique générée est : {KE}" + f" et la clé privée générée est: {a}"
  #fic = os.path.join(subfile, "ElGamalkeygen.txt")
  ouputfiles(out, subfile, "ElGamalkeygen.txt")

  return (KE,a)



def ElGamalencryption(sprime, generator, KE, msg, outfile):
  """Fonction qui signe notre message hashé

  Args:
      sprime (double): Nombre fortement premier (public)
      generator (double): Génerateur dans Zsprime*
      KE (double): Clé publique générée
      msg (double): Message en hashé non signé

  Returns:
      (double, double): (KE, digest signé ElGamal)
  """
  msg = hash256(str(msg).encode()).hex()
  msg = hexatodecimal(msg)
  (K,b) = ElGamalKeygeneration(sprime,generator) 
  share_key = pow(KE, b, sprime) % sprime  #share key
  y = (msg * share_key) % sprime # y = résultat du chiffrement de msg
  ptxt = f"Le message clair est: {msg}"
  ouputfiles(ptxt, subfile, "Elgamal_message.txt")
  out = f"Le message signé est: {y} et la clé publique utilisée est : {KE}"
  #fic = os.path.join(subfile, outfile)
  ouputfiles(out, subfile, outfile)
  
  return (K, y)

def ElGamal_trans_encryption(sprime, generator, a, msg, outfile):
      subfile = os.path.join(file, "Blockchain")
      msg = hash256(str(msg).encode()).hex()
      msg = hexatodecimal(msg)
      (K,b) = ElGamalKeygeneration(sprime,generator) 
      share_key = pow(a, b, sprime) % sprime  #share key
      y = (msg * share_key) % sprime # y = résultat du chiffrement de msg
      #ptxt = f"Le message clair est: {msg}"
      #ouputfiles(ptxt, subfile, "Elgamal_message.txt")
      out = f"Le message signé est: {y} et la clé privée utilisée est : {a}"
      #fic = os.path.join(subfile, outfile)
      ouputfiles(out, subfile, outfile)
  
      return (K, y)



def ElGamaldecryption(sprime,generator,a,cipherpair):
  """Verification de signature

  Args:
      sprime (double): Safe prime (public)
      generator (double): Generateur dans Zsprime
      a (double): valeur aléatoire représentant la clé privée
      cipherpair (double): Message hashé signé ElGamal

  Returns:
      double: Message hashé avant signature
  """
  (KE,y) = cipherpair
  plaintext = y*pow(KE,sprime-1-a,sprime) % sprime #plaintext = y * inverse(KE**a) % sprime
  return plaintext 
  
def tester():
  bits = 512
  (sprime,generator)=initialisation()
  (KE,a)=ElGamalKeygeneration(sprime,generator)
  msg = input("Veuillez entrer le message à chiffrer: \n")
  #msg = 123456789123456789123456789123456789123456789123456789
  #assert msg < sprime
  print (bits, 'bit prime ', sprime)
  print ('generator', generator)
  print ('KE', KE)
  print ('a', a)
  print ('msg:', msg)
  cipherpair = ElGamalencryption(sprime,generator,KE, msg, "ElGamaltest.txt")
  (B, cipher) = cipherpair
  print ('B', B)
  print ('cipher', cipher)
  decrypted = ElGamaldecryption(sprime,generator,a, cipherpair)
  print ('decrypted:', decrypted)

if __name__ == '__main__':
  tester()
  pass
