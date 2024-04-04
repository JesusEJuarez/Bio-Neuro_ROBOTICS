import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import sample 
import numpy as np
import csv

def ant_colony_optimization(links, feasible_space, nest, food):
    terreno_pos = feasible_space
    link = np.array(links)
    pheromones = np.ones(len(link)) * 0.1  # Initial pheromone level
    pheromones = pheromones[:, np.newaxis]
    dist = np.zeros(len(link))
    vis_n = np.zeros(len(link))
    
    # Calculate distance and visibility factor for each link
    for i in range(len(link)):
        pnt1 = link[i, 0]
        pnt2 = link[i, 1]
        p1 = terreno_pos[pnt1]
        p2 = terreno_pos[pnt2]
        # Distance calculation
        dist[i] = calculate_distance(p1, p2)
        # Visibility factor
        vis_n[i] = 1 / dist[i]  
    vis_n = vis_n[:, np.newaxis]
    
    # Select next link based on pheromone levels and visibility
    def select_next_link(current_link, available_links):
        if len(available_links) == 0:
            return None
        probabilities = np.zeros(len(available_links))
        total = 0
        for i, link in enumerate(available_links):
            pheromone = pheromones[link]
            probability = pheromone * vis_n[link]
            probabilities[i] = probability
            total += probability
        probabilities /= total
        next_link = np.random.choice(available_links, p=probabilities)
        return next_link
    
    Q = 10  # Learning rate
    evaporation = 0.5 # Evaporation rate of pheromones
    explorations = 150 # Number of explorations to perform
    n_ants = 20 # Number of exploring ants
    ant_paths = np.zeros((n_ants, len(link)), dtype=int) # Paths of ants
    ant_distances = np.zeros(n_ants) # Distances traveled by ants
    ant_distances = ant_distances[:, np.newaxis]
    visited_nodes = np.zeros((n_ants, 3), dtype=int)  # Store the last 3 visited nodes for each ant
    
    # Algorithm for ant colony optimization
    way = []
    min_distance = np.inf
    
    for _ in range(explorations):
        
        for ant in range(n_ants):
            visited_links = [] 
            way = []
            last_link = 0
            ant_distances[ant] = 0
            ant_paths[ant, :] = 0
            distand = 0
            current_link = nest
            way.append(current_link)
            while current_link != food:
                available_links = np.where(link[:, 0] == current_link)[0]
                test = np.array(visited_links)
                for i in range(len(visited_links)):
                    available_links = np.delete(available_links, np.where(available_links == test[i]))
    
                if len(available_links) > 0:
                    last_nodes = visited_nodes[ant][-3:]
                    available_links = [link for link in available_links if link not in last_nodes]
    
                    if len(available_links) > 0:
                        next_link_index = np.random.choice(len(available_links))
                        next_link = available_links[next_link_index]
                        visited_links.append(next_link)
                        ant_paths[ant, next_link] = 1
                        distand += dist[next_link]
                        ant_distances[ant] += dist[next_link]
                        current_link = link[next_link, 1]
                        way.append(current_link)
    
                        visited_nodes[ant] = np.roll(visited_nodes[ant], -1)
                        visited_nodes[ant][-1] = current_link
                    else:
                        break
                else:
                    break
    
                if distand > 15:
                    break
    
            if distand <= 15 and way[-1] == food:
                if distand < min_distance:
                    best_route = way
                    min_distance = distand
                pheromones *= (1 - evaporation)
                for link_index in np.where(ant_paths[ant] == 1)[0]:
                    pheromones[link_index] += Q / ant_distances[ant]
    
    return best_route, min_distance

# Function to calculate distance between two points
def calculate_distance(a, b):
    return np.sqrt(np.sum(np.square(a - b)))

# Function to check if a point is near an obstacle
def check_obstacle(obstacles, a, b):
    line = np.linspace(a, b, 10)
    for i in range(10):
        for j in obstacles:
            if calculate_distance(j[:3], line[i]) < np.sqrt(j[3]):
                return True
    return False

# Load feasible space points
feasible_space = np.load('./espacioFactible.npy').tolist()

# Define start and end points
start_point = [0.5, 2.5, 1]
end_point = [2.7, 1, -1]

# Define parameters
number_of_points = 100
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
approx_radius = 1
links = []

# Define obstacles
obstacles = [[1.5, -2, 0, 1]]

# Sample feasible points
points = sample(feasible_space, number_of_points)
points.insert(0, start_point)
points.append(end_point)

# Link points
linked = [False]*len(points)
linked[0] = True
aleatory_point = np.array(points)

# Generate branches
while(True):
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dis = calculate_distance(np.array(points[i]), np.array(points[j]))
            if dis < approx_radius:
                link = j
                if not check_obstacle(obstacles, aleatory_point[i], aleatory_point[link]): 
                    links.append([i, link])
                    links.append([link, i])
                    linked[link] = True
        
    if sum(linked) > len(points) * 0.5 :
        break
links.sort()

# Plot branches and points 
ax.scatter(aleatory_point[:, 0], aleatory_point[:, 1], aleatory_point[:, 2], c='b', marker='o', label='Feasible Points')
for a, b in links:
    ax.plot([aleatory_point[a, 0], aleatory_point[b, 0]],
            [aleatory_point[a, 1], aleatory_point[b, 1]],
            [aleatory_point[a, 2], aleatory_point[b, 2]], c='r', linestyle=':')

# Select route
route, distance = ant_colony_optimization(links, aleatory_point, 0, len(aleatory_point) - 1)

# Plot route
fig2 = plt.figure()
ax1 = fig2.add_subplot(111, projection='3d')
ax1.scatter(aleatory_point[:, 0], aleatory_point[:, 1], aleatory_point[:, 2], c='b', marker='o', label='Feasible Points')
output = []
c = 0
for i in range(1, len(route)):
    ax1.plot([aleatory_point[route[i - 1], 0], aleatory_point[route[i], 0]],
             [aleatory_point[route[i - 1], 1], aleatory_point[route[i], 1]],
             [aleatory_point[route[i - 1], 2], aleatory_point[route[i], 2]], c='k', linestyle='-')
    output.append([np.rad2deg(aleatory_point[route[c], 0]), np.rad2deg(aleatory_point[route[c], 1]), np.rad2deg(aleatory_point[route[c], 2])])
    c = c + 1
plt.show()

# Save route to CSV file
with open("path_trajectory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

