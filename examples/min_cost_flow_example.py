import os
import sys
import time
from tqdm import tqdm

sys.path.append(os.path.abspath("../build/python_lib"))

import mcf
import numpy as np


def main():

    # Init graph
    graph = mcf.Graph()

    # Add nodes
    nodes = []
    num_nodes = 1000
    num_traj = 10
    stime = time.time()
    for i in range(num_nodes):
        cost = np.random.uniform(1)
        node = graph.add(cost)

        start_cost = np.random.uniform(-1, 1)
        if i < num_traj:
            start_cost = -10
        graph.link(graph.ST, node, start_cost)

        end_cost = np.random.uniform(-1, 1)
        if i > num_nodes - num_traj:
            end_cost = -10
        graph.link(node, graph.ST, end_cost)
        nodes.append(node)
    print(f"Adding nodes: {time.time()-stime: 0.4f}s\n")

    # Link nodes
    stime = time.time()
    for i, node_i in enumerate(nodes):
        for j, node_j in enumerate(nodes[i:]):
            if node_i == node_j:
                continue
            if np.abs(node_i - node_j) < 30:
                cost = np.random.uniform(-1, 1)
                graph.link(node_i, node_j, cost)
    print(f"Building full graph: {time.time()-stime: 0.4f}s\n")

    # Solve graph
    stime = time.time()
    solver = mcf.Solver(graph)
    trajectories = solver.run_search(num_traj, num_traj)
    print(f"Solution: {time.time()-stime: 0.4f}s\n")

    for i, trajectory in enumerate(trajectories):
        print(f"trajectory {i}")
        for n in trajectory:
            print(f"  node: {n}")


if __name__ == "__main__":
    main()
