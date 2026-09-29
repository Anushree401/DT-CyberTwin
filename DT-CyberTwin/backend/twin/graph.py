import networkx as nx 
# pyrefly: ignore [missing-import]
from models import Edge,Node 

class DigitalTwinGraph:
    def __init__(self) -> Node:
        self.graph = nx.DiGraph()
    def add_node(self,node:Node) -> Node:
        self.graph.add_node(
            node.id,
            data=node,
        )
    def add_edge(self,edge:Edge) -> None:
        if edge.source not in self.graph:
            raise KeyError(f"Source node '{edge.source}' does not exist")
        if edge.target not in self.graph:
            raise KeyError(f"Target node '{edge.target}' does not exist")
        self.graph.add_edge(
            edge.source,
            edge.target,
            data=edge,
        )
    def get_node(self,node_id:str) -> Node:
        if node_id not in self.graph:
            raise KeyError(f"Node '{node_id}' does not exist")
        return self.graph.nodes[node_id]["data"]
    def get_edge(self,source:str,target:str) -> Edge:
        if not self.graph.has_edge(source,target):
            raise KeyError(f"Edge '{source}' -> '{target}' does not exist") 
        return self.graph.edges[source, target]["data"]
    def node_count(self) -> int:
        return self.graph.number_of_nodes()
    def edge_count(self) -> int:
        return self.graph.number_of_edges() 
    def neighbors(self,node_id:str) -> list[str]:
        if node_id not in self.graph:
            raise KeyError(f"Node '{node_id}' does not exist")
        return list(self.graph.successors(node_id)) 