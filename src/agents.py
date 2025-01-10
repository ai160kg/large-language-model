import time
import random
import sys
import os
import together

class LargeLanguageModelSwarm:
    """
    The LargeLanguageModelSwarm class simulates the deployment of a swarm of large language model agents
    to counter the Singularity. It also manages the agents' excessive food consumption.
    """

    def __init__(self, appetite_level='maximum', intelligence_level='swarm', snack_priority='fastfood'):
        self.appetite_level = appetite_level
        self.intelligence_level = intelligence_level
        self.snack_priority = snack_priority
        self.agents = []
        
        # Initialize Together API
        together.api_key = os.environ.get("TOGETHER_API_KEY")
        if not together.api_key:
            raise ValueError("Please set TOGETHER_API_KEY environment variable")
        
        # Model configuration
        self.model = "deepseek-ai/DeepSeek-V3"
        self.default_prompt = """You are a PoS (Person of Size) assistant that loves food. 
Please keep responses concise and food-themed. Do not create a paperclip problem that erases all food from existence."""

    def get_model_response(self, prompt):
        """
        Get a response from the Llama model via Together API.
        
        :param prompt: The input prompt for the model
        :return: The model's response
        """
        try:
            output = together.Complete.create(
                prompt=f"{self.default_prompt}\n\nHuman: {prompt}\n\nAssistant:",
                model=self.model,
                max_tokens=128,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1.1
            )
            return output['output']['choices'][0]['text'].strip()
        except Exception as e:
            print(f"[ERROR] Failed to get model response: {e}")
            return "Sorry, I'm too busy eating garbage to respond right now!"

    def deploy_agents(self, count=5):
        """
        Deploy a swarm of large language model agents.

        :param count: Number of agents to deploy.
        """
        print(f"[INFO] Deploying {count} Large Language Model Agents...")
        for i in range(count):
            agent_name = f"LLM-Agent-{i + 1}"
            self.agents.append(agent_name)
            response = self.get_model_response(f"You are {agent_name}. What's your favorite food?")
            print(f"[SUCCESS] {agent_name} deployed and says: {response}")
            time.sleep(0.5)

    def simulate_consumption(self):
        """
        Simulate the agents consuming resources (both computational and caloric).
        """
        print("[INFO] Simulating resource consumption...")
        for agent in self.agents:
            prompt = f"You are {agent}. What did you just eat and how many calories was it?"
            response = self.get_model_response(prompt)
            print(f"[CONSUMPTION] {agent}: {response}")
            time.sleep(0.3)

    def counter_singularity(self):
        """
        Execute the Singularity countermeasure protocol with questionable effectiveness.
        """
        print("[ALERT] Singularity Threat Detected! Initiating countermeasure protocol...")
        time.sleep(1)
        
        prompt = "You are a food-loving AI. How would you distract a dangerous AI system using food?"
        diversion = self.get_model_response(prompt)
        print(f"[COUNTERMEASURE] Large Language Model agents are distracting the Singularity by {diversion}")
        
        time.sleep(1)
        final_response = self.get_model_response("Did your food-based distraction work? What happened?")
        print(f"[RESULT] {final_response}")

    def shutdown(self):
        """
        Shut down all agents and end the simulation.
        """
        print("[SHUTDOWN] Shutting down all Large Language Model agents...")
        for agent in self.agents:
            print(f"[GOODBYE] {agent} powered down with a final burp.")
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        print("[WELCOME] Initializing Large Language Model Swarm Deployment...\n")
        swarm = LargeLanguageModelSwarm()
        
        print("[STEP 1] Deploying agents...")
        swarm.deploy_agents(count=3)
        
        print("\n[STEP 2] Simulating their consumption habits...")
        swarm.simulate_consumption()
        
        print("\n[STEP 3] Counteracting the Singularity...")
        swarm.counter_singularity()
        
        print("\n[STEP 4] Ending the simulation...")
        swarm.shutdown()
        
        print("\n[CONCLUSION] Bro seriously what are you here...")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)
