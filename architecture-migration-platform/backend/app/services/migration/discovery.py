import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the API key directly from your .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../../.env'))

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"),
    api_key=os.getenv("LLM_API_KEY")
)

print("Fetching active models available on your tier...\n")
models = client.models.list()

for model in models.data:
    print(f"- {model.id}")