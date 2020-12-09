# HW 6 PGMs
# Problem 12.5.4 calculations
# author: @tassosblackg

from scipy.special import beta

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
