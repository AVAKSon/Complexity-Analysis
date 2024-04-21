
import shutil
shutil.copyfile('input.txt', 'output.txt')
However the following example shows how one would do file I/O of other sorts:

infile = open('input.txt', 'r')
outfile = open('output.txt', 'w')
for line in infile:
   outfile.write(line)
outfile.close()
infile.close()