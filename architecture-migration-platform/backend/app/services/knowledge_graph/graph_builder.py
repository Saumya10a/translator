import networkx as nx
from datetime import datetime
import json
import sys
import os

# Add the parent directory to the path so we can import the parser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.services.intelligence.ast_parser import ASTParser

class KnowledgeGraphBuilder:
    """
    Converts raw AST into a relational Architecture Graph (AIR)
    and formats it as a document for dynamic database insertion.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, ast_data: dict, component_name: str) -> dict:
        # Add the root component to the network graph
        self.graph.add_node(component_name, type="component")

        # Traverse the AST to find dependencies
        self._extract_dependencies(ast_data, parent=component_name)

        # Convert the NetworkX graph to a dictionary for MongoDB
        graph_data = nx.node_link_data(self.graph)
        
        # Structure the final AIR document
        air_document = {
            "component_name": component_name,
            "timestamp": datetime.utcnow().isoformat(),
            "architecture_graph": graph_data,
            "status": "mapped_and_ready"
        }
        return air_document

    def _extract_dependencies(self, node: dict, parent: str):
        """
        Recursively searches the AST for specific architectural nodes.
        For this prototype, it maps external function calls (e.g., fetchUsers).
        """
        if node.get("type") == "call_expression":
            for child in node.get("children", []):
                # If the code calls a function, map it as a dependency edge
                if child.get("type") == "identifier" and child.get("name"):
                    target_func = child.get("name")
                    # Ignore common built-ins for this example
                    if target_func not in ["app", "req", "res"]:
                        node_id = f"Function::{target_func}"
                        self.graph.add_node(node_id, type="dependency")
                        self.graph.add_edge(parent, node_id, relation="calls")

        for child in node.get("children", []):
            self._extract_dependencies(child, parent)

if __name__ == "__main__":
    # 1. Parse the code using the intelligence layer
    sample_js_code = """
    app.get('/users', (req, res) => {
        const users = fetchUsers();
        res.json(users);
    });
    """
    scanner = ASTParser()
    raw_ast = scanner.parse_code(sample_js_code, "javascript")

    # 2. Convert the AST into the Application Intermediate Representation (AIR)
    builder = KnowledgeGraphBuilder()
    air_document = builder.build_graph(raw_ast, component_name="UserController")

    # 3. Output the graph document (This is what gets sent to MongoDB and the LLM)
    print(json.dumps(air_document, indent=2))