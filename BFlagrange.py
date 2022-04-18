import numpy as np
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

#x = np.array([0,1,2])
#y = np.array([0,1,4])
#poly = lagrange(x, y)
#print(Polynomial(poly.coef[::-1]).coef)

#Brute force counting of integer points in the interior of the dilation of the In-Out polytope 
#I don't remember the exact polytope
#n is the dilation
def f1(n):
    x1, x2, x3, x4, x5, x6, x7, s = 1,1,1,1,1,1,1,0
    while (x1<n):
        x2=1
        while(x2<n):
            x3=1
            while(x3<n):
                x4=1
                while(x4<n):
                    x5=1
                    while(x5<n):
                        x6=1
                        while(x6<n):
                            x7=1
                            while(x7<n):
                                if((x1+x4!=x2+x3) and (x1+x4!=x5+x7) and (x1+x4!=x5+x6) and (x1+x4!=x6+x7) and (x1+x2!=x3+x4) and (x1+x2!=x7+x5) and (x1+x2!=x5+x6) and (x1+x2!=x6+x7) and (x2+x3!=x7+x5) and (x2+x3!=x5+x6) and (x2+x3!=x6+x7) and (x3+x4!=x7+x5) and (x3+x4!=x5+x6) and (x3+x4!=x6+x7) and (x2!=x4) and (x1!=x3) and (x5!=x6) and (x6!=x7) and (x7!=x5)):
                                    s+=1
                                x7+=1
                            x6+=1
                        x5+=1
                    x4+=1
                x3+=1
            x2+=1
        x1+=1
    return s

#Brute force counting in cube and out of hyperplanes
#Example 3.1
def cubog1(n):
    x1, x2, s = 1,1,0
    while (x1<n):
        x2=1
        while (x2<n):
            if ((x2+x1!=n) and (x1!=x2)):
                s+=1
            x2+=1
        x1+=1
    return s

#Brute force count in 3 dimensional simplex
#Example 5.2, B2-[2] with 4 markings
def golP3(n):
    x1,x2,x3,x4,s = 1,1,1,1,0
    while (x1<n):
        x2=1
        while (x2<n):
            x3=1
            while((x3<n) and (n-x1-x2-x3>0)):
                x4=n-x1-x2-x3
                if((x1!=x2 or x2!=x3 or x3!=x1) and(x1!=x2 or x2!=x4 or x4!=x1) and(x1!=x3 or x3!=x4 or x4!=x1) and(x2!=x3 or x3!=x4 or x4!=x2) and(x1!=x2 or x2!=x3+x4 or x3+x4!=x1) and(x1!=x4 or x4!=x2+x3 or x2+x3!=x1) and(x3!=x4 or x4!=x1+x2 or x1+x2!=x3) and(x1!=x2+x3 or x2+x3!=x3+x4 or x3+x4!=x1) and(x4!=x1+x2 or x1+x2!=x2+x3 or x2+x3!=x4) and(x1+x2!=x2+x3 or x2+x3!=x3+x4 or x3+x4!=x1+x2)):
                    s+=1
                x3+=1
            x2+=1
        x1+=1
    return s

#Brute force counting in 2 dimensional simplex
#B2-[2] with 3 markings
def golP2(n):
    x1,x2,x3,s = 1,1,1,0
    while (x1<n):
        x2=1
        while ((x2<n) and n-x1-x2>0):
            x3=n-x1-x2
            if(x1!=x2 or x2!=x3 or x3!=x1):
                s+=1
            x2+=1
        x1+=1
    return s

#Brute force counting in 2 dimensional simplex
#Example 5.4, B3 sets with 3 markings 
def h3m3(n):
    x1,x2,x3,s = 1,1,1,0
    while(x1<n):
        x2=1
        while(x2<n and n-x2-x1>0):
            x3=n-x2-x1
            if(x1!=x2 and x1!=2*x2 and 2*x1!=x2 and x1!=x3 and x1!=2*x3 and 2*x1!=x3 and x2!=x3 and x2!=2*x3 and 2*x2!=x3 and x1!=x2+x3 and 2*x1!=x2+x3 and x1!=2*x2+x3 and x1!=x2+2*x3 and x1!=2*x2+2*x3 and x1+x2!=x3 and 2*x1+x2!=x3 and x1+2*x2!=x3 and 2*x1+2*x2!=x3 and x1+x2!=2*x3 and x1+x3!=x2):
                s+=1
            x2+=1
        x1+=1
    return s

#B2-[2] with 4 markings  polynomial
x = [60,120,180,240]
y = list()
for i in x:
    y.append(golP3(i))

poly = lagrange(x, y)
print(Polynomial(poly.coef[::-1]).coef)

#B3 sets with 3 markings  polynomial
x = [2520,5040,7560,10080]
y = list()
for i in x:
    y.append(h3m3(i))

poly = lagrange(x, y)
print(Polynomial(poly.coef[::-1]).coef)
