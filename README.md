# BusRoutes

Python scripts for constructing map model for bus route optimization model
Relevant files:
<ol>
<li> model_maker.py
<li> random_map_generator.py
</ol>

model_maker.py 
Uses OSM files downloaded from openstreetmap.org to parse for intersections then uses google map api to find distance matrix between all intersections. Currently, unusable due to timeouts by google server.

random_map_generator.py
Randomly constructs an adjacency graph and from that two files; students.txt and distances.txt. students.txt contains a list of students (one student per line) and for each student a list of intersections,which are within walking distance, represented by their id. distances.txt contains a list of distances between intersections. The first value per line is the id and the second value within [] is the list of distances to other intersections. This is essentially the lower triangular matrix representing a weighted bidirectional graph.

