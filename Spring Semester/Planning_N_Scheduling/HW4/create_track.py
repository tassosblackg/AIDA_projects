import os

"""
Create a.txt file containing the route of the track

"#" -> Represents a wall element
"." -> Represents the available road/track
"S" -> Represents the Start of the race
"F" -> Represents the Finish line
"""

numberofrows = 12
numberofcols = 16

with open("u_track.txt", "w") as f:
    f.write(str(numberofrows) + "," + str(numberofcols) + "\n")

    for i in range(numberofrows):
        if i <= 1:  # first two lines are walls
            f.write("#" * numberofcols)
            f.write("\n")
        elif i == 2:
            f.write("#" * 2)
            f.write("S" * 2)
            f.write("." * 10)
            f.write("#" * (numberofcols - 14))
            f.write("\n")
        elif i <= 4:
            f.write("#" * 2)
            f.write("S" * 2)
            f.write("." * 11)
            f.write("#" * (numberofcols - 15))
            f.write("\n")
        elif i <= 6:
            f.write("#" * 11)
            f.write("." * 3)
            f.write("#" * (numberofcols - 14))
            f.write("\n")
        elif i <= 8:
            f.write("#" * 5)
            f.write("F" * 2)
            f.write("." * 7)
            f.write("#" * (numberofcols - 14))
            f.write("\n")
        elif i == 9:
            f.write("#" * 5)
            f.write("F" * 2)
            f.write("." * 6)
            f.write("#" * (numberofcols - 13))
            f.write("\n")
        else:
            f.write("#" * numberofcols)
            f.write("\n")
