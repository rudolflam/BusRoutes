import googlemaps
from intersections import find_intersections
key = "AIzaSyCaHJkj5Tzx7gMXDX-M9cUBOw_b3zlgoLw"


def start(file):
    intersections = find_intersections(file)

    client = googlemaps.Client(key)
    ids = []
    coords = []
    with open('distances.txt', 'w') as f:
        f.write('Distance matrix \n')
    counter = 1
    for id, (x,y) in intersections.items():
        print ('Calculating row for: ('+str(counter)+')')
        counter += 1
        print (id)
        ids += [id]
        coords += [(x,y)]
        row = googlemaps.distance_matrix.distance_matrix(client, [(x,y)], coords)
        print ('Received '+str(row))
        
        with open('distances.txt', 'a') as f:
            f.write(str(id) + '\t' + str(row))

def resume(file, intersection):
    intersections = find_intersections(file)

    client = googlemaps.Client(key)
    ids = []
    coords = []
    
    counter = 1
    found = False
    for id, (x,y) in intersections.items():
        print ('Calculating row for: ('+str(counter)+')')
        counter += 1
        
        if not found and id != intersection:
            print ('Skipping '+str(counter-1))
            continue
        elif id == intersection:
            print ('Skipping '+str(counter-1))
            found = True
            continue
        
        print (id)
        ids += [id]
        coords += [(x,y)]
        row = googlemaps.distance_matrix.distance_matrix(client, [(x,y)], coords)
        with open('distances.txt', 'a') as f:
            f.write(str(id) + '\t' + str(row))
            
import argparse
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Construct the distance matrix to model distances between bus stops')
    parser.add_argument('file', help='The OSM file')
    parser.add_argument('--resume', '-r', type=int, help='Resume construction from a certain intersection (input the last id available in the distances.txt file)')
    args = parser.parse_args()
    if args.resume:
        resume(args.file, args.resume)
    else :
        start(args.file)