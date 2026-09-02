import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class MigrationOrchestrator:
    """
    Handles the communication with the LLM (DeepSeek, Qwen, etc.) 
    enforcing architectural constraints during translation.
    """
    def __init__(self):
        # By default, uses OpenAI SDK format, which is compatible with DeepSeek, Groq, and local Ollama
        self.client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1"),
            api_key=os.getenv("LLM_API_KEY", "your-api-key-here")
        )
        self.model = os.getenv("LLM_MODEL", "deepseek-coder")

    def generate_migration(self, source_code: str, target_stack: str, air_graph: dict) -> str:
        """
        Translates code while enforcing the structural rules defined in the AIR graph.
        """
        # Format the constraints from the Knowledge Graph
        nodes = [node["id"] for node in air_graph.get("architecture_graph", {}).get("nodes", [])]
        edges = air_graph.get("architecture_graph", {}).get("edges", [])
        
        constraint_string = f"Required Entities: {', '.join(nodes)}\nRequired Relationships:\n"
        for edge in edges:
            constraint_string += f"- {edge['source']} must {edge['relation']} {edge['target']}\n"

        system_prompt = (
            f"You are an expert Enterprise Solutions Architect. "
            f"Migrate the provided source code to {target_stack}. "
            f"CRITICAL INSTRUCTION: You must strictly enforce the following architectural constraints. "
            f"Do not rename the core entities or break these dependency chains.\n\n"
            f"Constraints:\n{constraint_string}\n\n"
            f"Output ONLY the raw executable code block without markdown wrappers."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": source_code}
                ],
                temperature=0.1, # Keep temperature low for deterministic, logical output
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Generation Failed: {str(e)}"

if __name__ == "__main__":
    # Test data representing what we just extracted in the previous steps
    sample_js_code = """
    app.get('/users', (req, res) => {
        const users = fetchUsers();
        res.json(users);
    });
    """
    
    mock_air_graph = {
        "architecture_graph": {
            "nodes": [{"id": "UserController"}, {"id": "Function::fetchUsers"}],
            "edges": [{"source": "UserController", "target": "Function::fetchUsers", "relation": "calls"}]
        }
    }

    orchestrator = MigrationOrchestrator()
    print("Initiating Architecture-Aware Translation to Python FastAPI...\n")
    
    # Note: This will fail until we provide a valid API key or local model!
    result = orchestrator.generate_migration(
        source_code=sample_js_code, 
        target_stack="Python FastAPI", 
        air_graph=mock_air_graph
    )
    
    print(result)