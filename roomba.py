class roomba():
    nodes = []
    graph = {}
    severity = []
    visited = {}
    stack = []
    paths = {}
    path = []

    def __init__(self,r,mess):
        self.r = r
        self.mess = mess
        self.create_graph()
        self.reset_visited()
        self.longest_path_DAG()

    # Initialize visited list as all False
    def reset_visited(self):
        for idx,node in enumerate(self.nodes):
            self.visited[idx] = False

    # Topologically sorts the nodes
    def topological_sort(self,index):
        self.visited[index] = True

        # Check if neighbor-node was already visited
        for neighbors in self.graph[index]:
            if self.visited[neighbors[0]] == False:
                self.topological_sort(neighbors[0])

        # Append to the stack
        self.stack.append(index)
    
    # Prints the longest path (optimal path for Roomba to clean the room)
    def longest_path_DAG(self):
        # initializing the weights of each edge using the severity of each mess
        weight = []
        for i in (self.severity):
            weight.append(i)
        
        # Recursively call the topological_sort function to get the top-sorted stack
        for i in range(len(self.mess)):
            if not self.visited[i]:
                self.topological_sort(i)

        # Use the node at the top of the stack
        first_node = self.stack[len(self.stack)-1]
        weight[first_node] = 0

        for i in range(len(self.stack)):
            u = self.stack[len(self.stack)-i-1]
            # Compare the weight of the edge of the neighbor to see if it is lesser than
            # the new weight. If it is, change its weight to the new, larger value.
            for neighbors in self.graph[u]:
                if weight[neighbors[0]] < weight[u] + neighbors[1]:  
                    weight[neighbors[0]] = weight[u] + neighbors[1]
                    self.paths[neighbors[0]] = u

        # Get the node at the bottom of the stack (where the graph ends)
        index = self.stack[0]
        # Use the node from the bottom of the stack to trace back
        # the optimal graph.
        while True:
            self.path.append(index)
            try:
                index = self.paths[index]
            except:
                break

        # Reverse the list and print it as the optimal path for roomba
        self.path.reverse()
        print(f"The optimal path is {self.path}")
        print(f"The Roomba Minus should start at a point in the room with coordinates ({self.nodes[index][0]},0)")
            

    def get_neighbors(self,node_index):
        all_neighbor = []
        
        for idx,n in enumerate(self.nodes):
            # get the slope of current node and its possible neighbor
            rise = n[1] - self.nodes[node_index][1]
            run = n[0] - self.nodes[node_index][0]
            # check if connection follows this restrictions
            # 1. the next node should not have a greater y-coordinate than the current node
            # 2. can travel the horizontal distance between the two nodes given the vertical horizontal ratio
            if self.nodes[node_index][1] < n[1] and abs((rise/run)/self.r) > 1:
                neighbor_w_weight = (idx, self.severity[idx])
                all_neighbor.append(neighbor_w_weight)
        return all_neighbor
    
    def create_graph(self):
        # gets the necessary information into their respective variables
        for single_mess in self.mess:
            self.nodes.append(single_mess[0])
            self.severity.append(single_mess[1])
        # get the neighbors of each mess
        for idx,node in enumerate(self.nodes):
            neighbors = self.get_neighbors(idx)
            self.graph[idx] = neighbors
        

r = 16.7374586913063
mess = [\
    ((50.53339753651755, 2392.9913262022305), 4),
    ((91.45350267880721, 2038.5690414517053), 6),
    ((81.30630354764358, 3002.1564113738523), 9),
    ((37.16228801441648, 2421.3261154038723), 8),
    ((16.323410763410276, 696.3036909610697), 1),
    ((17.558652660436632, 2306.3556734125145), 1),
    ((30.858752483887464, 751.748794481916), 3),
    ((30.957197204880696, 944.2879593578829), 8),
    ((15.042626905954554, 2344.979171359295), 1),
    ((84.13614550978521, 1310.743768220772), 9)]

roomba(r,mess)