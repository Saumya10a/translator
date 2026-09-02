from tree_sitter import Language, Parser
import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_java
import json

class ASTParser:
    """
    Extracts deterministic Abstract Syntax Trees (AST) from source code.
    This acts as the Repository Intelligence scanner in the architecture.
    """
    def __init__(self):
        # Modern initialization using individual language packages
        self.languages = {
            "python": Language(tree_sitter_python.language()),
            "javascript": Language(tree_sitter_javascript.language()),
            "typescript": Language(tree_sitter_typescript.language_typescript()),
            "java": Language(tree_sitter_java.language())
        }

    def parse_code(self, source_code: str, language: str) -> dict:
        """
        Takes raw source code and returns a structured dictionary representing the AST.
        """
        lang_key = language.lower()
        if lang_key not in self.languages:
            raise ValueError(f"Language '{language}' is not currently supported by the AST Scanner.")

        # Initialize the parser and set the language dynamically
        parser = Parser(self.languages[lang_key])
        
        raw_bytes = bytes(source_code, "utf8")
        tree = parser.parse(raw_bytes)
        
        return self._node_to_dict(tree.root_node, raw_bytes)

    def _node_to_dict(self, node, raw_bytes: bytes) -> dict:
        """
        Recursively walks the tree-sitter nodes and builds a clean dictionary (The AIR format).
        """
        # Extract the actual text only for named identifiers
        node_text = raw_bytes[node.start_byte:node.end_byte].decode('utf8') if node.is_named else None

        node_data = {
            "type": node.type,
            "name": node_text if node.type == 'identifier' else None,
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
            "children": []
        }

        for child in node.named_children:
            node_data["children"].append(self._node_to_dict(child, raw_bytes))

        return node_data

if __name__ == "__main__":
    # Test the scanner with a basic Node.js Express route
    sample_js_code = """
    app.get('/users', (req, res) => {
        const users = fetchUsers();
        res.json(users);
    });
    """
    
    scanner = ASTParser()
    ast_output = scanner.parse_code(sample_js_code, "javascript")
    
    print(json.dumps(ast_output, indent=2))