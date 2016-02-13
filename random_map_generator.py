from random import randint
from random import gauss
from random import random
import numpy as np

def minplus(A,B,n):
    ''' min plus operation on matrices A and B of dimension nxn'''
    C = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            choices = [A[i,k] + B[k,j] for k in range(n)]
            C[i,j] = min(choices)
    return C

def power_minplus(A,n, power):
    div, odd = divmod(power, 2)
    if div == 1:
        return A
    elif div == 2 and odd == 0:
        D = minplus(A,A,n)
        return D
    elif odd:
        C = power_minplus(A,n,div) 
        D = minplus(A, minplus(C,C,n),n)
        return D
    else:
        C = power_minplus(A,n,div)
        D = minplus(C,C,n)
        return D

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Construct the distance matrix to model distances between bus stops from a random procedure')
    parser.add_argument('n', type=int, help='Size of map (min 3) (number of intersections including the school (n-1st) and bus depot(nth) )')
    parser.add_argument('s', type=int, help='Number of students (min 1)')
    parser.add_argument('--file', '-f', help='Provide a file name for the output file (default:distances.txt)')
    args = parser.parse_args()
    n = args.n if args.n >= 3 else 3
    s = args.s if args.s >= 1 else 1
    intersections = list(range(n))
    distances = [[0]*n for i in intersections]
    for i in intersections:
        minimum = min(3, n-i-1)
        branches = randint(1, minimum) if minimum > 1 else 1
        branches_map = { randint(i+1,n-1) if i+1 < n-1 else n-1: gauss(220,75) for branch in range(branches)}
        for j in range(n):
            distances[i][j] = 0 if i==j else float('inf') if j not in branches_map.keys() else branches_map[j] 

    # adjacency matrix
    matrix = np.matrix(distances)
    for i in range(n):
        for j in range(n):
            if i>j:
                matrix[i,j] = matrix[j,i]
    # students 
    students_nearest_stops = [ [randint(0, n-3)] for i in range(s)]
    for i, locations in enumerate(students_nearest_stops):
        for j in range(n):
            if matrix[ locations[0], j] < float('inf') and random() < 0.15:
                students_nearest_stops[i] += [j]
    with open('./students.txt', 'w') as f:
        for s in students_nearest_stops:
            f.write(str(s)+'\n')
    # construct distance matrix
    result = power_minplus(matrix, n, n).T
    filename = args.file if args.file else './distances.txt'
    with open(filename, 'w') as f:
        f.write('Randomly generated map\n')
        for i,row in enumerate(result):
            f.write( str(i) + ' ' + str(list(row[:i])) +'\n')