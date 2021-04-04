import math_graph
import random
from math_graph import Point3D
from datetime import datetime

# Python program to print all paths from a source to destination.

from collections import defaultdict

# This class represents a directed graph
# using adjacency list representation


class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
	visited[] keeps track of vertices in current path.
	path[] stores actual vertices and path_index is current
	index in path[]'''

    def printAllPathsUtil(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            print(path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i] == False:
                    self.printAllPathsUtil(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False

    # Prints all paths from 's' to 'd'

    def printAllPaths(self, s, d):

        # Mark all the vertices as not visited
        visited = [False]*(self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)


# Create a graph given in the above diagram

g = Graph(300)
for i in range(0, 300):
    g.addEdge(random.randint(0, 20), random.randint(0, 20))

s = 20
d = 30
print("Following are all different paths from % d to % d :" % (s, d))
g.printAllPaths(s, d)

# get dict of all points each point in 3d has an id
# add edges from one point to another

def get_around_points(point):
    points = list()
    points.append(math_graph.Point3D(point.x + 1, point.y, point.z))
    points.append(math_graph.Point3D(point.x - 1, point.y, point.z))
    points.append(math_graph.Point3D(point.x, point.y + 1, point.z))
    points.append(math_graph.Point3D(point.x, point.y - 1, point.z))
    points.append(math_graph.Point3D(point.x, point.y, point.z + 1))
    points.append(math_graph.Point3D(point.x, point.y, point.z - 1))
    points_filtered = filter_matrix_points(points)
    return points_filtered

def filter_matrix_points(points):
    points_filtered = list()
    for s in points:
        if s.x >= matrix_cube_size[0] or s.x < 0:
            continue
        if s.y >= matrix_cube_size[1] or s.y < 0:
            continue
        if s.z >= matrix_cube_size[2] or s.z < 0:
            continue

        points_filtered.append(s)

    return points_filtered

graph = Graph((3*3*3) + 1)
dic_points = {}
dic_points_id = {}
id_counter = 1
matrix_cube_size = (3, 3, 3)
for x in range(0, matrix_cube_size[0]):
  for y in range(0, matrix_cube_size[1]):
      for z in range(0, matrix_cube_size[2]): 
            dic_points[(x, y, z)] = id_counter
            dic_points_id[id_counter] = (x, y, z)
            id_counter += 1

for p in dic_points_id.values():
    around_points = get_around_points(math_graph.Point3D(p[0], p[1], p[2]))
    for ap in around_points:
        graph.addEdge(dic_points[p], dic_points[ap.to_tuple()])

s = 2
d = 6

print("Following are all different paths from % d to % d :" % (s, d))
#graph.printAllPaths(s, d)
