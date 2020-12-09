# Through K fair Coins find K
# Problem 5 - HW6
# that maximises the likelihood
# and what is p(K)
# author: @tassosblackg

import argparse
from scipy.special import binom

def max_k_through(N1,N2,NH):
    theta = 0.5 #fair coins
    p_k = 0.5 # each k is equal likely to be the maximum
    apr_pH,kappas = [],[]
    for k in range(N1, N2+1,1):
        apr_pH.append(binom(k,NH)*((theta)**NH)*((1-theta)**(k-NH)))
        kappas.append(k)

    maximum_likelihood = max(apr_pH) # max likelhood value
    max_index = apr_pH.index(maximum_likelihood) # max likelihood value's index
    max_kappa = kappas[max_index]

    # Theorem of Total Probability of P(#Heads=NH)
    total_probability = p_k*sum(apr_pH)
    p_NH_k = maximum_likelihood * p_k / total_probability

    print('\n# List of Likelihoods for each K \n>',apr_pH,'\n <')
    print('\n# List of Kappas in N1-N2,',kappas,'\n')
    return (max_kappa,p_NH_k)

# parser menu
def parserM():

    parser=argparse.ArgumentParser(prog="Calculate K max through")
    parser.add_argument('N1',type=int,help='<Give N1 integer>')
    parser.add_argument('N2',type=int,help='<Give N2 integer>')
    parser.add_argument('Heads',type=int,help='<Give num of Heads integer>')

    args=parser.parse_args()
    if (args.N1>args.N2 or args.Heads > args.N2):
        print("Error for the arguments must have N1<= #Heads <= N2 \n")
        exit(-1)
    else:
        k,p_NH_k = max_k_through(args.N1, args.N2, args.Heads)
        print("\n-> Maximum Likelihood is given for K= ",k,"\n")
        print("\n-> P(K=k|Heads=NH)= ",p_NH_k,"\n")


if __name__ == '__main__':
    parserM()
