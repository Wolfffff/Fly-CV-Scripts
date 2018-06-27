import numpy as np 
allwalks = []
def recursiveWalk(x, y, j, this_list):
  # x and y are the coordinates of the starting point.
  # j is the number of steps left.
  # x and y are positive integers.
  Total = 0
  # Add the current point to list.
  # this_list.append([x,y])
  if j == 0:
    # Successfully reached a self-avoiding walk of the desired length
    #if len(this_list) == len(set(this_list)): 
    # z = this_list.count([2,2])
    # if z <= 2: 
    Total = Total + 1
    allwalks.append(this_list)
  else:  # Check what directions are possible to continue walking
    if j: # At the beginning 
      # start off with all vertices having a value of 0
      lattice = np.zeros([x+y+1, x+y+1]) 
      # let the starting vertex have a value of 1
      for i in range(len(this_list)):
        lattice[this_list[i][0], this_list[i][1]] =  1
      this_list.append([x,y])
      print(this_list)
    #if lattice[x, y] < 2:
    #  lattice[x, y] = lattice[x, y] + 1
    #  recursiveWalk(x, y, j - 1, this_list[:])
    if lattice[x + 1, y] < 2:
      lattice[x + 1, y] = lattice[x + 1, y] + 1
      this_list.append([x + 1, y])
      # print(this_list)
      recursiveWalk(x + 1, y, j - 1, this_list[:])
    if lattice[x - 1, y] < 2:
      lattice[x - 1, y] = lattice[x - 1, y] + 1
      this_list.append([x - 1, y])
      #print(this_list)
      recursiveWalk(x - 1, y, j - 1, this_list[:])
    if lattice[x, y + 1] < 2:
      lattice[x, y + 1] = lattice[x, y + 1] + 1
      this_list.append([x, y + 1])
      #print(this_list)
      recursiveWalk(x, y + 1, j - 1, this_list[:])    
    if lattice[x, y - 1] < 2:
      lattice[x, y - 1] = lattice[x, y - 1] + 1
      this_list.append([x, y - 1])
      #print(this_list)
      recursiveWalk(x, y - 1, j - 1, this_list[:])

# example 
# x and y must be greater than or equal to j.
# j - number of steps
# x,y is the starting point.
recursiveWalk(2,2,2,[])
# length of walk
print("Number of total walks: ", len(allwalks))
print("\nThe walks: ")
# print each walk
for i in range(len(allwalks)):
 print(allwalks[i])
