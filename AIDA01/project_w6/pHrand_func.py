# HW 6 PGMs
# Problem 12.5.4 calculations
# author: @tassosblackg
from scipy.special import beta
import random
from statistics import stdev,mean
from math import sqrt

a,b = 1,1

R1 = 10
W1 = 12

R2 = 100
W2 = 120

def p_random_H(R,W,a,b):

    numerator = 0.5 **(R+W)
    denominator = numerator + beta(R+a,W+b)/beta(a,b)

    return (numerator/denominator)


pHr1 = p_random_H(R1, W1, a, b)
pHr2 = p_random_H(R2, W2, a, b)

print('For R=10,w=12 = ',pHr1,'\n')
print('For R=100,w=120 = ',pHr2,'\n')

# Trying to prove the 12.5.5 question by using a
# Monte Carlo experiments, approach  by calculating the mean values
# for N iterations with different Values of R and W
# and at the end the distance must be as small as possible
# N equal to the number of R,W values
# For large values of R,W beta gives nan
def converge_std():
     R = random.sample(range(10, 130), 100)
    #R = [1,10,100,140,180]
    W = random.sample(range(min(R)+15, max(R)+15), 100)
    #W = [2,12,120,160,200]
    val_equation, approx_val = [],[]
    for i in range(len(R)):
        val_equation.append(p_random_H(R[i], W[i], 1, 1))
        approx_val.append(0.5*sqrt(R[i]+W[i])) # std value given the type

    print(val_equation)
    std_equation = stdev(val_equation)

    std_approx = mean(approx_val)

    print('Stdev using equation from (12.5.4) = ',std_equation,'\n')
    print('Stdev using approximation type of (12.5.5) = ',std_approx,'\n')
    print('Stdev Absolute Distance between two stds = ',abs(std_equation - std_approx),'\n')

converge_std()
