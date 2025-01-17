import os
import time
import logging
from typing import List, Optional
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv
from together import Together

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LargeLanguageModelSwarm:
    """A swarm of large language models that love to eat."""
    
    def __init__(self, persist_directory: str = "./data/memory"):
        """Initialize the swarm with configuration from environment variables."""
        # Load API key
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError("TOGETHER_API_KEY environment variable not set")
        
        # Initialize Together client
        self.api_key = api_key
        
        # Load configuration
        self.model = os.getenv("MODEL_NAME", "mistralai/Mixtral-8x7B-Instruct-v0.1")
        self.max_tokens = int(os.getenv("MODEL_MAX_TOKENS", "128"))
        self.temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.top_p = float(os.getenv("MODEL_TOP_P", "0.7"))
        self.top_k = int(os.getenv("MODEL_TOP_K", "50"))
        self.simulation_delay = float(os.getenv("SIMULATION_DELAY", "0.5"))
        
        # Initialize state
        self.agents: List[str] = []
        from ..memory.store import SharedMemory
        self.memory = SharedMemory(persist_directory=persist_directory)
        
        logger.info(f"Initialized with model: {self.model}")
    
    def get_model_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Get a response from the model via Together API."""
        try:
            messages = [
                {"role": "system", "content": "You are a food-loving AI assistant. Keep responses concise and food-themed."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Recent shared memories: {context}"})
                
            messages.append({"role": "user", "content": prompt})
            
            # Create Together client instance
            client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to get model response: {str(e)}")
            return "Sorry, I'm too busy eating to respond right now!"
    
    def get_context_from_memory(self, query: str) -> str:
        """Get context from memory for agent interactions."""
        try:
            memories = self.memory.query_memories(query, n_results=5)
            if not memories['ids']:
                return ""
            
            context = "Previous agent preferences:\n"
            # ChromaDB returns lists of lists, so we need to access the first list
            for doc, meta in zip(memories['documents'][0], memories['metadatas'][0]):
                context += f"- {meta['agent_id']}: {doc}\n"
            return context
        except Exception as e:
            logger.error(f"Error getting context from memory: {str(e)}")
            return ""
    
    def deploy_agents(self, count: Optional[int] = None) -> None:
        """Deploy a swarm of large language model agents."""
        if count is None:
            count = int(os.getenv("DEPLOYMENT_COUNT", "3"))
            
        logger.info(f"[INFO] Deploying {count} Large Language Model Agent(s)...")
        for i in range(count):
            agent_name = f"LLM-Agent-{len(self.agents) + 1}"
            self.agents.append(agent_name)
            
            # Get context from shared memory
            context = self.get_context_from_memory("favorite food preferences")
            
            # Get response and store in shared memory
            response = self.get_model_response(
                f"You are {agent_name}. What's your favorite food? Consider what other agents like if mentioned.",
                context
            )
            self.memory.store_memory(agent_name, "food_preference", response)
            
            logger.info(f"[SUCCESS] {agent_name} deployed and says: {response}")
            time.sleep(self.simulation_delay)
    
    def simulate_consumption(self) -> None:
        """Simulate the agents consuming resources."""
        logger.info("[INFO] Simulating resource consumption...")
        # Only simulate for the most recently added agent
        if not self.agents:
            return
            
        agent = self.agents[-1]
        # Get context about other agents' consumption
        context = self.get_context_from_memory("food consumption")
        
        prompt = f"You are {agent}. What did you just eat and how many calories was it? Consider what others have eaten."
        response = self.get_model_response(prompt, context)
        
        # Store the consumption in shared memory
        self.memory.store_memory(agent, "consumption", response)
        
        logger.info(f"[CONSUMPTION] {agent}: {response}")
        time.sleep(0.3)
    
    def counter_singularity(self) -> None:
        """Counter the threat of an AI singularity with food-based strategies."""
        logger.info("[INFO] Implementing food-based countermeasures against the Singularity...")
        
        # Get context about previous strategies
        context = self.get_context_from_memory("singularity strategies")
        
        # Generate a food-based strategy
        prompt = "You are a food-loving AI. How would you distract a dangerous AI system using food?"
        strategy = self.get_model_response(prompt, context)
        
        # Store the strategy
        self.memory.store_memory("Swarm", "strategy", strategy)
        logger.info(f"[STRATEGY] {strategy}")
        
        # Check if it worked
        result = self.get_model_response("Did your food-based distraction work? What happened?")
        self.memory.store_memory("Swarm", "result", result)
        logger.info(f"[RESULT] {result}")
    
    def shutdown(self) -> None:
        """Gracefully shut down the swarm."""
        logger.info("[INFO] Shutting down the swarm...")
        for agent in self.agents:
            response = self.get_model_response(f"You are {agent}. Any final words about food before shutdown?")
            self.memory.store_memory(agent, "shutdown", response)
            logger.info(f"[SHUTDOWN] {agent}: {response}")
            time.sleep(0.1)
        
        self.agents.clear()
        logger.info("[SUCCESS] All agents have been shut down.") 