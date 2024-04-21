
import os
for directory in ['/', './']:
  open(directory + 'output.txt', 'w').close()  # create /output.txt, then ./output.txt
  os.mkdir(directory + 'docs')                 # create directory /docs, then ./docs

Works with: Python version 2.5
Exception-safe way to create file:

from __future__ import with_statement
import os
def create(directory):
    with open(os.path.join(directory, "output.txt"), "w"):
        pass
    os.mkdir(os.path.join(directory, "docs"))
   
create(".") # current directory
create("/") # root directory
