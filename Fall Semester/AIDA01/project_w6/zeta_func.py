# HW 6
# Problem 12.4
# author:@tassosblackg

import numpy as np
from scipy.special import gamma

numOfClasses = 3
# person 1 with person 2
list = [[13,3,4],[4,9,7],[8,8,4]]
mat = np.array(list)
u = np.ones(numOfClasses, dtype=int)



def zeta(uq):
    numerator = 1
    sum_q=0

    for i in range(uq.shape[0]):
        numerator = numerator*gamma(uq[i])
        sum_q = sum_q + uq[i]

    return (numerator/gamma(sum_q))

# persons 1,2
za = zeta(u+mat[0])
zb = zeta(u+mat[1])
z1 = zeta(u)
zab = zeta(u+mat[0]+mat[1])
p12_dif = za*zb
p12_sam = z1*zab
print("Persons 1-2 bayes factor = ",'(',p12_dif,p12_sam,')','/=',p12_dif/p12_sam,'\n')
#8.368188175996467e-10 2.4202096393388754e-21

#persons 1,3
za = zeta(u+mat[0])
zc = zeta(u+mat[2])

zac = zeta(u+mat[0]+mat[2])
p13_dif = za*zc
p13_sam = z1*zac
print("Persons 1-3 bayes factor = ",'(',p13_dif,p13_sam,')','/=',p13_dif/p13_sam,'\n')


# persons2,3
zb = zeta(u+mat[1])
zc = zeta(u+mat[2])

zbc = zeta(u+mat[1]+mat[2])
p23_dif = zb*zc
p23_sam = z1*zbc
print("Persons 2-3 bayes factor = ",'(',p23_dif,p23_sam,')','/=',p23_dif/p23_sam,'\n')




zabc = zeta(u+mat[0]+mat[1]+mat[2])
p123_dif = za*zb*zc
p123_sam = z1*zabc
print("Persons 1-2-3 bayes factor = ",'(',p123_dif,p123_sam,')','/=',p123_dif/p123_sam,'\n')

print('u+a = [ ',u+mat[0],'] ,','u+b= [ ',u+mat[1],'] u+c= [',u+mat[2],']\n')
print('u+a+b = [ ',u+mat[0]+mat[1],']\n' )
print('u+a+c = [ ',u+mat[0]+mat[2],']\n' )
print('u+b+c = [ ',u+mat[1]+mat[2],']\n' )
