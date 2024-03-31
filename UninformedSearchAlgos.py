import sys
import csv
import heapq
from random import random

class MovieEnvironment:
    def __init__(self):
        filepath =  r"disney-movies-data.csv"
        self.titles = []
        self.length = 0
        self.__tdict = {}
        self.__adj_list = {}

        self.__read_movie_data(filepath)
        self.__generate_graph()


    def __read_movie_data(self, filepath):
        file = open(filepath, "r")
        data = list(csv.reader(file, delimiter=","))
        self.titles = [row[0] for row in data]
        file.close()
        self.length = len(self.titles)

    def __generate_graph(self):
        i = 0
        while i < 500: # number of edges in the graph.
            r1 = int(random()*self.length)
            r2 = int(random()*self.length)
            while r2 == r1:
                r2 = int(random()*self.length)
            
            while (r1,r2) in self.__tdict.keys() or (r2,r1) in self.__tdict.keys():
                r2 = int(random()*self.length)

            self.__tdict[(r1,r2)] = 1
            self.__tdict[(r2,r1)] = 1

            weight = random()
            self.__adj_list.setdefault(self.titles[r1],{})[self.titles[r2]]=round(weight,2)*100
            self.__adj_list.setdefault(self.titles[r2],{})[self.titles[r1]]=round(weight,2)*100
            i+=1

    def get_neighbours(self, m1):
        """
        Returns the neighbours (similar movies) for a movie.

        :param str m1: The movie name whose neighbours to find.
        :return dict[str,float]: The dictionary of neighbour nodes and their link weights (0-100) as float which show similarity (lower value means more similar).
        """
        return self.__adj_list[m1]

    #def display_graph(self):
        #import networkx as nx
        #g = nx.DiGraph(self.__adj_list)
        #nx.draw(g, with_labels=True, font_weight='bold')
        #import matplotlib.pyplot as plt
        #plt.show()


""" Your code starts here   """

def breadth_first_search(env, movie1, movie2):
    """
    Returns the shortest path from movie1 to movie2 (ignore the weights).
    """
     # maintain a visited set
    visited = set()
    # maintain a queue for iterating
    queue = []
    # enqueue the current movie along with the path
    queue.append((movie1, [movie1]))

    # while the queue is NOT empty
    while queue:
        # pop the current movie along with its path as we have visited this node
        curr_movie, path = queue.pop(0)
        
        #ensure the movie popped from queue set is added to visited set so we know we visited that node
        if curr_movie not in visited:
            visited.add(curr_movie)

        if curr_movie==movie2:
            return path   

        # iterate through all the neighbours of the current_movie node. we only care about the keys because the values contain the weights
        for neighbour_movie in env.get_neighbours(curr_movie).keys():
            # check search condition
            if neighbour_movie == movie2:
                # if search condition true, add that neighboring node to the path
                path.append(neighbour_movie)
                visited.add(neighbour_movie)
                
                print(" ")
                print ("Nodes visited ",visited)
                print("Number of Nodes visited ",len(visited))
                print(" ")
                return path  

            if neighbour_movie not in visited:
                # if the search condition is false and we have visited neighbouring node, mark and add it to visited set
                queue.append((neighbour_movie, path + [neighbour_movie]))


    # if no path, return all the visited nodes/movies
    return visited

def depth_first_search(env, movie1, movie2):
    """
    Returns the path from movie1 to movie2
    """
     # maintain a visited set
    visited = set()
    # maintain a stack for iterating
    stack = []
    # push the current movie along with the pathE
    stack.append((movie1, [movie1]))

    #while the stack is NOT empty
    while stack:

        #we wanna pop the last element as DFS uses LIFO
        curr_movie, path=stack.pop()

        #mark the node as visited
        if curr_movie not in visited:
            visited.add(curr_movie)

        if curr_movie==movie2:
            return path    

        #go through all the neighbouring nodes of the current movie
        for neighbour_movie in env.get_neighbours(curr_movie).keys():

            #check search condition
            if neighbour_movie==movie2:
                #we have found shortest path
                path.append(neighbour_movie)
                visited.add(neighbour_movie)

                print ("Nodes visited ",visited)
                print("Number of Nodes visited ",len(visited))
                return path
            
            if neighbour_movie not in visited:
            #if search conidition false, store the neighbouring nodes in a stack
                stack.append((neighbour_movie,path+[neighbour_movie]))

    # if no path, return all the visited nodes/movies
    return visited


def uniform_cost_search(env, movie1, movie2):
    """
    Returns the path from movie1 to movie2 with the lowest sum of weights.
    """

    #maintain a visited/explored set
    explored=set()

    #maintain a priority queue to iterate.
    #each element in the priority queue is a tuple (path-cost,movie,movie-path)
    priority_queue=[(0,movie1,[movie1])]

    # while the priority queue is not empty
    while priority_queue:
        #remove the lowest cost node/movie
        path_cost,curr_movie,path=heapq.heappop(priority_queue)

        ## to ensure only one visit, mark the element in the explored set
        if curr_movie not in explored:
            explored.add(curr_movie)

        # check search condition
        if curr_movie == movie2:

            print ("Nodes visited ",explored)
            print("Number of Nodes visited ",len(explored))
            return path  
        
        # for all the neighbors of the current movie node
        for neighbour_movie ,weight in env.get_neighbours(curr_movie).items():
            if neighbour_movie not in explored:
                # enqueue them along with the updated path and cost 
                new_cost = path_cost + weight  
                heapq.heappush(priority_queue, (new_cost, neighbour_movie, path + [neighbour_movie]))

    # if no path, return all the visited nodes/movies
    return explored

""" Your code ends here     """




if __name__ == "__main__":
    env = MovieEnvironment()

    movie1 = input("enter movie1 name:")
    i=1
    while movie1 not in env.titles:
        print("name not in the list")
        movie1 = input("enter movie1 name:")
        i+=1
        if i>=3:
            sys.exit()

    movie2 = input("enter movie2 name:")
    i=1
    while movie2 not in env.titles:
        print("name not in the list")
        movie2 = input("enter movie1 name:")
        i+=1
        if i>=3:
            sys.exit()

    print(breadth_first_search(env, movie1, movie2))
    print(depth_first_search(env, movie1, movie2))
    print(uniform_cost_search(env, movie1, movie2))

    #env.display_graph()
