import os, egglib, sys, unittest, random, re, gc, time
from random import *
"""
source: http://python.jpvweb.com/mesrecettespython/doku.php?id=loi_binomiale
"""

#########################################################################################################################################from 
def power(a, b):
    if b == 0:
        return 1
    elif b == 1:
        return a
    elif b > 1:
        return a * power(a, b-1)


def combin(n, k):
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x


def binom(k,n,p):
    x=combin(n,k)*pow(p,k)*pow(1-p,n-k)
    return x

def binomcum(k,n,p):
    if k==n:
        return 1.0
    if p==0:
        return 0.0
    if p==1.0:

        return 0.0
    j=int(p*n)
    b=0
    xmin=1.0e-20
    if k<=j:
        for i in range(k,-1,-1):
            x=binom(i,n,p)
            b+=x
            if x<xmin:
                break
    else:
        for i in range(k+1,n+1):
            x=binom(i,n,p)
            b+=x
            if x<xmin:
                break
        b=1.0-b
    return b
 
def binomconfsup(k,n,conf):
    eps=1.0e-8
    r=1.0-conf
    p1=k/n
    dp=0.1
    f1=binomcum(k,n,p1)-r
    while True:
        p2=p1+dp
        f2=binomcum(k,n,p2)-r
        if abs(f2)<eps:
            break
        if ((f1>0)and(f2>0))or((f1<0)and(f2<0)):
            if abs(f2)>abs(f1):
                dp*=-0.5
        else:
            dp*=-0.5
        p1=p2
        f1=f2
    return p2
 
def binomconfinf(k,n,conf):
    eps=1.0e-8
    r=1-conf
    dp=-0.1
    p1=k/n
    f1=1-binomcum(k-1,n,p1)-r
    while True:
        p2=p1+dp
        f2=1-binomcum(k-1,n,p2)-r
        if abs(f2)<eps:
            break
        if ((f1>0)and(f2>0))or((f1<0)and(f2<0)):
            if abs(f2)>abs(f1):
                dp*=-0.5
        else:
            dp*=-0.5
        p1=p2
        f1=f2
    return p2
 
def binomconf(k,n,conf):

    bi=binomconfinf(k,n,conf+(1-conf)/2)
    bs=binomconfsup(k,n,conf+(1-conf)/2)
    return [bi,bs]

#########################################################################################################################################
def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

#########################################################################################################################################

