
from operateur import *

taut, cont = Tautologie(), Contradiction()
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = [Variable(lettre) for lettre in "abcdefghijklmnopqrstuvwxyz"]


def plus(v1, v2):
    return ((v1 + v2) * -(v1 * v2)).calculer()

def retenu(v1, v2):
    print("-", v1.afficher_valeur(), v2.afficher_valeur())
    return (v1 * v2).calculer()


def addition_binaire(v1, v2):
    return plus(v1, v2), retenu(v1, v2)

def addition(bits1, bits2):
    assert len(bits1) == len(bits2)
    assert len(bits1) == 2
    v1, v2 = [], []
    for v, l in zip(bits1, range(len(bits1))):
        v1.append(Variable(str(l), int(v)))
    for v, l in zip(bits2, range(len(bits2))):
        v2.append(Variable(str(l), int(v)))
    v3 = []
    v3.append(plus(v1[-1], v2[-1]))

def plus_un(bits1):
    assert len(bits1) == 2
    v1, v2 = [], []
    for v, l in zip(bits1, range(len(bits1))):
        v1.append(Variable(str(l), True if int(v) else False))
    v3 = []
    v3.append(plus(v1[-1], taut))
    premiere_retenu = Variable("", retenu(v1[-1], taut))
    print(premiere_retenu.valeur)
    v3.append(plus(v1[-2], premiere_retenu))
    v3.append(retenu(v1[-2], premiere_retenu))

    v3.reverse()
    return v3
    
    
        

##
##a.valeur = int(input("a: "))
##b.valeur = int(input("b: "))
##resultat = addition_binaire(a, b)
##
##
##print(int(resultat[0]), int(resultat[1]))


print(plus_un(input()))
