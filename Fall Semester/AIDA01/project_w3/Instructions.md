# Read a matrix of size NxM
# Convetion N = # of rows, M = # of columns

Each **Row** corresponds to a distribution, where column is the value of the distribution for the current j

A =

[

      value1 value2 value3 valueN  

        .     .      .     .     

        .     .      .     .

        .     .      .     .

]

Each value must be a positive float for example instead of 1/4 -> 0.25
if 1/3 -> round it to 0.3 and make sure values to sum into 1


# Execute with
for calculate_min_KLdivergence (pass argmunet -kl)

*$python3 problem_w3.1.py **-kl** <inputFile_name>*

else (default)

*$python3 problem_w3.1.py  <inputFile_name>*
