from app.services.intelligence.ast_parser import ASTParser
from app.services.knowledge_graph.graph_builder import KnowledgeGraphBuilder
from app.services.migration.llm_orchestrator import MigrationOrchestrator

# Java source code that finds the maximum number in an array
java_code = """
public class ArrayProcessor {
    public int findMax(int[] numbers) {
        int max = numbers[0];
        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i];
            }
        }
        return max;
    }
}
"""

# 1. Parse the Java code using tree-sitter
scanner = ASTParser()
raw_ast = scanner.parse_code(java_code, "java")

# 2. Build the Application Intermediate Representation (AIR) graph
builder = KnowledgeGraphBuilder()
air_document = builder.build_graph(raw_ast, component_name="ArrayProcessor")

# 3. Translate using the constrained LLM orchestrator
orchestrator = MigrationOrchestrator()
print("Translating Java Array Max-Finder to Python with Architectural Constraints...\n")

result = orchestrator.generate_migration(
    source_code=java_code,
    target_stack="Python (Idiomatic Python with Class Structure)",
    air_graph=air_document
)

print(result)