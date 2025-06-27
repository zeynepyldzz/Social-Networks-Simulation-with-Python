import networkx as nx  # Library used for creating social networks and working with graph theory
import matplotlib.pyplot as plt  # Library used for plotting graphs and visualizing networks
import random  # Library used for generating random numbers and handling probability calculations

# 1. Creating the Social Network
def create_social_network():
    """
    Creates a random social network using the Erdos-Renyi model.
    The network consists of 15 nodes with a 30% connection probability.
    """
    G = nx.erdos_renyi_graph(15, 0.3)  # 15 nodes, 30% connection probability
    return G

# 2. Calculating PageRank
def calculate_pagerank(G):
    """
    Runs the PageRank algorithm on the given social network.
    Calculates and ranks the importance of nodes.
    """
    pagerank = nx.pagerank(G)  # Applies the PageRank algorithm
    sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)  # Sorts nodes based on PageRank values
    return pagerank

# 3. Influence Spread Simulation
def influence_spread_simulation(G, pagerank, max_steps=100):
    """
    Simulates influence spread:
    - Starts from the most influential node (the node with the highest PageRank value).
    - At each step, it tries to influence the neighbors of affected nodes (with a 30% probability).
    - Dynamically visualizes the spread process on a graph and prints results.
    """
    # Select the most influential node as the starting point (highest PageRank value)
    start_node = max(pagerank, key=pagerank.get)
    influenced_nodes = {start_node}  # Initially, only the starting node is influenced
    steps_data = []  # Stores the list of influenced nodes at each step

    print(f"\nStarting node (most influential person): {start_node}")

    # Draw the initial graph - Initially, only the most influential node is red
    plt.ion()  # Enable interactive plotting mode
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G)  # Determines the positions of nodes on the graph
    nx.draw(G, pos, with_labels=True, node_color="lightgray", node_size=500, ax=ax)  # Draws the network graph
    nodes = nx.draw_networkx_nodes(G, pos, nodelist=list(influenced_nodes), node_color="red", ax=ax)  # Marks the starting node in red
    plt.title(f"Influence Spread - Step 0 (Start: {start_node})")
    plt.show()

    plt.pause(5)  # Show the initial state for 5 seconds

    # Influence spread occurs step by step
    step = 0
    while step < max_steps:
        step += 1
        new_influenced = set()  # Stores newly influenced nodes at this step
        current_step_nodes = []  # Keeps track of influenced nodes in each step

        # Try to influence neighbors of already influenced nodes
        for node in influenced_nodes:
            neighbors = G.neighbors(node)  # Get neighboring nodes
            for neighbor in neighbors:
                if neighbor not in influenced_nodes and random.random() < 0.3:  # 30% probability of influence
                    new_influenced.add(neighbor)
                    current_step_nodes.append(neighbor)

        if not new_influenced:  # If no new nodes are influenced, stop the spread
            break

        influenced_nodes.update(new_influenced)  # Add newly influenced nodes
        steps_data.append(current_step_nodes)  # Store influenced nodes at each step

        # Update the graph and visualize the new state
        nx.draw_networkx_nodes(G, pos, nodelist=list(influenced_nodes), node_color="red", ax=ax)
        ax.set_title(f"Influence Spread - Step {step}")
        plt.draw()  # Update the drawing
        plt.pause(30)  # Wait 5 seconds

        # Stop the simulation if all nodes are influenced
        if len(influenced_nodes) == len(G.nodes):
            break

    plt.ioff()  # Disable interactive mode

    # Display simulation results in a separate graph window
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.axis('off')  # Hide axes in the graph

    # Add "Simulation Results" title
    ax2.text(0.1, 0.95, "Simulation Results", fontsize=14, fontweight='bold')

    # Print influenced nodes at each step
    y_offset = 0.80
    for i, step_nodes in enumerate(steps_data):
        ax2.text(0.1, y_offset, f"Step {i+1}: {step_nodes}", fontsize=10)
        y_offset -= 0.1

    # Display starting node, total number of influenced nodes, and total steps
    ax2.text(0.1, y_offset, f"Starting node (most influential person): {start_node}", fontsize=12)
    y_offset -= 0.1
    ax2.text(0.1, y_offset, f"Total number of influenced nodes: {len(influenced_nodes)}", fontsize=12)
    y_offset -= 0.1
    ax2.text(0.1, y_offset, f"Total number of steps: {step}", fontsize=12)

    plt.show()

# 4. Main Program
if __name__ == "__main__":
    """
    Entry point of the program:
    - Creates a social network.
    - Computes PageRank.
    - Simulates influence spread.
    """
    G = create_social_network()  # Create a random social network
    pagerank = calculate_pagerank(G)  # Compute node importance using the PageRank algorithm
    influence_spread_simulation(G, pagerank, max_steps=100)  # Start influence spread simulation
