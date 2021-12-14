

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
