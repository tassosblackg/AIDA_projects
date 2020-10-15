# Input File style
# Infos

- Starts with the Sparce name array and it is space separated between each character. Then new line, add only starting bracket '['

A =
[
      value1 value2 value3 valueN  
        .     .      .     .        
        .     .      .     .
        .     .      .     .
]

- each line one row of the array.
- last line must be only the closing bracket ']' char without space.
- suppose there is only one array in file.

# How to run the .py script
python3 handle_sp_matrices.py -csr <input_file> # convert to csr form

# OR

python3 handle_sp_matrices.py <input_file> # convert to csc form -> default
