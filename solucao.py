import sys

from Algorithms.dijkstra import dijkstra
from Algorithms.ganancioso import ganancioso
from Algorithms.Astar import astar
from classes import Grid

def main():
    grid = Grid(sys.argv[1])
    
    dijkstra(grid)
    ganancioso(grid)
    astar(grid)

if __name__ == "__main__":
    main()