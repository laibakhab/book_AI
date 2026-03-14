import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path so modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import and run the main application
from rag_agent.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)