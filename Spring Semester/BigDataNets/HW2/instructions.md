## Follow Executions Instractions

1. Check *requirements.txt* first to see dependencies.

    if not installed into your system,  open terminal inside the project's directory:
    >  pip install -r requirements.txt

2. To run the program .py:

    Run the script and pass as argmunent the path to the directory where *pcap* files are stored.

    > python3 tr_analysis.py path_to_data_directory

    For example:

    > python3 tr_analysis.py '/home/user/Projects/Hw2/Data'

    where ***Data/*** directory, contains **only** all the *pcap* files.


## Files structure:
- instructions.md : Must be ***READ*** before starting!
- requirements.txt : contains all the package requirements needed for this project.
- tr_analysis.py : is the actual program to analyze the pcap captured files.
- *Report.pdf* : is short of a report for the project overview
- Images/ : contains different kinds of images from running the program  or analysis from wireshark.

## Important Notice :

Project tested and developed using ***Python3.9.2*** version, also developed at Linux distrOS (Manjaro Arch Based)
