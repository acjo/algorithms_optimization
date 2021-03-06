# shell2.py
"""Volume 3: Unix Shell 2.
Caelan Osman
Math 321 Sec 3
Nov. 13, 2020
"""

import os
from glob import glob
import subprocess
import numpy as np

# Problem 3
def grep(target_string, file_pattern):
    """Find all files in the current directory or its subdirectories that
    match the file pattern, then determine which ones contain the target
    string.

    Parameters:
        target_string (str): A string to search for in the files whose names
            match the file_pattern.
        file_pattern (str): Specifies which files to search.
    """
    #list containg all the files matching
    matching_files = glob('**/'+file_pattern, recursive = True)
    #list containing the files that have the target string
    target_files = []

    #iterate through file names in matching_files
    for filename in matching_files:
        #get the contents line by line
        with open(filename, 'r') as search:
            lines = search.readlines()
            #if the target string is in the line, append the file name, and break from the loop
            for line in lines:
                if target_string in line:
                    target_files.append(filename)
                    break

    return target_files

# Problem 4
def largest_files(n):
    """Returns a list of the n largest files in the current directory or its
    subdirectories (from largest to smallest).
    """

    #get all files
    all_files = glob('**', recursive = True)

    #iterate through all files getting the size and file name assuming the file name is to a file
    paths = [path for path in all_files if os.path.isfile(path)]
    sizes = np.array([os.path.getsize(path) for path in paths])

    #get the reverse index ranking
    ranking = np.argsort(sizes)[::-1]

    #list of files from largest to smallest (all)
    sorted_paths = [paths[index] for index in ranking]

    #write the line count of the nth smallest file to smallest.txt
    line_count = subprocess.check_output(['wc', '-l', sorted_paths[n-1]]).decode()
    with open('smallest.txt', 'w') as smallest:
        smallest.write(line_count.split()[0])

    #return the n largest files
    return sorted_paths[:n]

# Problem 6
def prob6(n = 10):
   """this problem counts to or from n three different ways, and
      returns the resulting lists each integer

   Parameters:
       n (int): the integer to count to and down from
   Returns:
       integerCounter (list): list of integers from 0 to the number n
       twoCounter (list): list of integers created by counting down from n by two
       threeCounter (list): list of integers created by counting up to n by 3
   """
   #print what the program is doing
   integerCounter = list()
   twoCounter = list()
   threeCounter = list()
   counter = n
   for i in range(n+1):
       integerCounter.append(i)
       if (i % 2 == 0):
           twoCounter.append(counter - i)
       if (i % 3 == 0):
           threeCounter.append(i)
   #return relevant values
   return integerCounter, twoCounter, threeCounter
