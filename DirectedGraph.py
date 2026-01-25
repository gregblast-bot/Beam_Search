class DirectedGraph:

    '''
    Initialize an empty directed graph as a dictionary data structure
    Keep track of the current head and tail during graph construction
    '''
    def __init__(self):
        self.graph = {}
        self.current_head = None
        self.current_tail = None

    '''
    Add a directed edge from head to tail with the given probability

    Args:
        head (str): The starting node of the directed edge
        tail (str): The ending node of the directed edge
        probability (float): The weight/probability associated with the edge
    '''
    def add_edge(self, head, tail):
        # Set current head and tail
        self.current_head = head
        self.current_tail = tail

        # If head node is not in the graph, initialize its entry
        if head not in self.graph:
            self.graph[head] = {}

        # Increment the count of this specific transition
        self.graph[head][tail] = self.graph[head].get(tail, 0) + 1

    '''
    Get the directed graph

    Returns:
        self.graph (dict): The directed graph represented as a dictionary
    '''
    def get_graph(self):
        return self.graph
    
    '''
    String representation of the directed graph

    Returns:
        str(self.graph) (str): A string representation of the directed graph
    '''
    def __str__(self):
        return str(self.graph)
            
    
