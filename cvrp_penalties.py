"""CVRP with dropping nodes analysis"""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import numpy as np
from tqdm import tqdm

from compute import Compute


def create_data_model(num_vehicles,number,mode = None):
    """Stores the data for the problem."""
    data = {}
    data['cost_matrix'] = pd.read_csv(f'experimentation/dep_costs/dep_cost_day{number}.csv',header = None).values.tolist()
    data['demands'] = pd.read_csv('data.csv',engine = 'python')['Demanda'].values.tolist()
    data['vehicle_capacities'] = [2880 for i in range(0,num_vehicles)]
    if mode == 'ruta':
        data['num_vehicles'] = num_vehicles
    elif mode == 'total':
        data['num_vehicles'] = 135
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, assignment,number,mode):
    """Prints assignment on console."""
    # Display dropped nodes.
    dropped_nodes = ''
    dropped_nodes_list = []
    print('Dropped nodes')
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
            dropped_nodes_list.append(manager.IndexToNode(node))

    # Display routes
    total_cost = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_cost = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_cost += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Cost of the route: {}m\n'.format(route_cost)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_cost += route_cost
        total_load += route_load
    print('Total Deprivation Cost of all routes: {}$'.format(total_cost))

    if mode == 'ruta':
        np.savetxt(f'experimentation/dropped_nodes/dropped_nodes_{number}.csv',dropped_nodes_list)
        with open(f'experimentation/route_cost/route_cost_day{number}','w') as file_cost:
            file_cost.write(str(total_cost))
    elif mode == 'total':
        with open(f'experimentation/total_cost/total_cost_day{number}','w') as file_cost:
            file_cost.write(str(total_cost))

    print('Total Load of all routes: {}'.format(total_load))


def main(num_vehicles,number):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(num_vehicles,number)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['cost_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def cost_callback(from_index, to_index):
        """Returns the cost between the two nodes."""
        # Convert from routing variable Index to cost matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['cost_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(cost_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    # Allow to drop nodes.
    penalty = 1000000
    for node in range(1, len(data['cost_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # Setting first solution heuristic (IF TAKES A LONG TIME CHANGE THE FirstSolutionStrategy OR LocalSearchMetaheuristic)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment,number)


if __name__ == '__main__':
    for i in tqdm(range (1,7)):
        main(40,i)
        Compute().recompute((i+1))
