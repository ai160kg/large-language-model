import os
import sys
import gradio as gr
import pandas as pd
import logging
from io import StringIO
from threading import Lock
from dotenv import load_dotenv
from ..agents.swarm import LargeLanguageModelSwarm
from ..memory.store import SharedMemory

# Load environment variables
load_dotenv()

# Configure logging before Gradio starts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # Override any existing configuration
)

class OutputCapture:
    def __init__(self):
        self.output = StringIO()
        self.lock = Lock()
        self.original_stdout = sys.stdout
        
    def write(self, text):
        with self.lock:
            self.original_stdout.write(text)
            self.output.write(text)
            
    def flush(self):
        with self.lock:
            self.original_stdout.flush()
            self.output.flush()
    
    def isatty(self):
        return self.original_stdout.isatty()
    
    def fileno(self):
        return self.original_stdout.fileno()
    
    def get_output(self):
        with self.lock:
            return self.output.getvalue()
    
    def clear(self):
        with self.lock:
            self.output = StringIO()

class SwarmUI:
    def __init__(self):
        self.swarm = None
        self.memory = SharedMemory(persist_directory="./data/memory")
        self.output_capture = OutputCapture()
        sys.stdout = self.output_capture
        self._logger = logging.getLogger(__name__)
        
    def initialize_swarm(self, count: int) -> str:
        """Initialize the swarm with a given number of agents."""
        try:
            self.swarm = LargeLanguageModelSwarm(persist_directory="./data/memory")
            return "✅ Swarm initialized successfully! Ready to run simulation."
        except Exception as e:
            return f"❌ Error initializing swarm: {str(e)}"
    
    def run_full_simulation(self, count: int) -> str:
        """Initialize and run the full simulation."""
        try:
            # Clear previous output
            self.output_capture.clear()
            
            # Initialize swarm
            self._logger.info("Initializing swarm...")
            yield "🚀 Initializing swarm..."
            self.swarm = LargeLanguageModelSwarm(persist_directory="./data/memory")
            yield "🚀 Swarm initialized!"
            
            # Deploy agents
            self._logger.info(f"Deploying {count} agents...")
            yield f"🤖 Starting deployment of {count} agents..."
            
            for i in range(count):
                self._logger.info(f"Deploying agent {i+1}...")
                yield f"🤖 Deploying agent {i+1} of {count}..."
                if i == 0:  # First agent
                    self.swarm.deploy_agents(count=1)
                    yield f"🤖 First agent deployed, gathering initial preferences..."
                else:  # Subsequent agents
                    self.swarm.deploy_agents(count=1)
                    yield f"🤖 Agent {i+1} deployed and learning from others..."
            
            # Run simulation steps
            self._logger.info("Simulating consumption...")
            yield "🍽️ Starting consumption simulation..."
            
            # Simulate consumption for each agent
            for i, agent in enumerate(self.swarm.agents):
                self._logger.info(f"Agent {agent} consuming...")
                yield f"🍽️ Agent {i+1} deciding what to eat..."
                self.swarm.simulate_consumption()
                yield f"🍽️ Agent {i+1} finished eating!"
            
            self._logger.info("Running counter-singularity strategies...")
            yield "🎯 Planning counter-singularity strategy..."
            self.swarm.counter_singularity()
            yield "🎯 Counter-singularity plan executed!"
            
            self._logger.info("Shutting down simulation...")
            yield "🔄 Beginning shutdown sequence..."
            
            # Shutdown each agent individually
            for i, agent in enumerate(self.swarm.agents):
                self._logger.info(f"Shutting down {agent}...")
                yield f"🔄 Agent {i+1} saying goodbye..."
            
            self.swarm.shutdown()
            
            yield "✅ Simulation completed successfully! Check the Memory Explorer tab to see what happened."
            
        except Exception as e:
            import traceback
            error_msg = f"❌ Error during simulation: {str(e)}\n{traceback.format_exc()}"
            self._logger.error(error_msg)
            yield error_msg
    
    def get_all_memories(self) -> pd.DataFrame:
        """Get all memories as a DataFrame."""
        return self.memory.get_all_memories()
    
    def get_memories_by_type(self, memory_type: str) -> pd.DataFrame:
        """Get memories filtered by type."""
        return self.memory.get_memories_by_type(memory_type)
    
    def get_memories_by_agent(self, agent_id: str) -> pd.DataFrame:
        """Get memories filtered by agent."""
        return self.memory.get_memories_by_agent(agent_id)
    
    def search_memories(self, query: str) -> pd.DataFrame:
        """Search memories using semantic search."""
        try:
            results = self.memory.query_memories(query, n_results=10)
            if not results['ids']:  # Check if we have any results
                return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
            
            # ChromaDB returns lists of lists for documents and metadatas
            return pd.DataFrame({
                'Timestamp': [m['timestamp'] for m in results['metadatas'][0]],
                'Agent ID': [m['agent_id'] for m in results['metadatas'][0]],
                'Type': [m['type'] for m in results['metadatas'][0]],
                'Content': results['documents'][0]
            })
        except Exception as e:
            print(f"Error in search_memories: {str(e)}")
            return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
    
    def clear_memories(self) -> str:
        """Clear all memories from the database."""
        try:
            self.memory.clear_all_memories()
            return "✅ Memories cleared successfully!"
        except Exception as e:
            return f"❌ Error clearing memories: {str(e)}"

def create_ui() -> gr.Blocks:
    """Create the Gradio UI."""
    ui = SwarmUI()
    
    with gr.Blocks(
        title="LLM Swarm Control Center",
        theme=gr.themes.Soft(),
        css="""
        .monospace, .monospace textarea {
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Source Code Pro', 'Courier New', monospace !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            background-color: #1e1e1e !important;
            color: #d4d4d4 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            white-space: pre-wrap !important;
        }
        .header-image {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            display: block;
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        """
    ) as app:
        # Add header image
        gr.Image("public/llm-swarm.png", label="", show_label=False, container=False, elem_classes=["header-image"])
        
        gr.Markdown("""
        # 🤖 LLM Swarm Control Center
        
        Welcome to the LLM Swarm Control Center! This interface allows you to:
        - Run simulations with multiple AI agents
        - View and search through agent memories
        - Monitor agent interactions and behaviors
        """)
        
        with gr.Tab("Simulation Control"):
            with gr.Row():
                agent_count = gr.Slider(
                    minimum=1, 
                    maximum=10, 
                    value=3, 
                    step=1, 
                    label="Number of Agents",
                    info="How many agents to deploy in the simulation"
                )
            
            with gr.Row():
                run_sim_btn = gr.Button("🚀 Run Full Simulation", variant="primary", scale=2)
                clear_btn = gr.Button("🗑️ Clear All Memories", variant="secondary", scale=1)
            
            status_output = gr.Textbox(
                label="Status", 
                lines=2,
                info="Current status of the simulation"
            )
            
            run_sim_btn.click(
                fn=ui.run_full_simulation,
                inputs=[agent_count],
                outputs=[status_output],
                queue=True
            )
            
            clear_btn.click(
                fn=ui.clear_memories,
                outputs=[status_output]
            )
        
        with gr.Tab("Memory Explorer"):
            with gr.Row():
                with gr.Column(scale=1):
                    memory_type = gr.Dropdown(
                        choices=["food_preference", "consumption", "strategy", "result", "shutdown"],
                        label="Filter by Memory Type",
                        info="Select a type of memory to filter"
                    )
                    agent_id = gr.Textbox(
                        label="Filter by Agent ID",
                        info="Enter an agent ID (e.g., LLM-Agent-1)"
                    )
                    search_query = gr.Textbox(
                        label="Semantic Search Query",
                        info="Search through memories using natural language"
                    )
                
                with gr.Column(scale=1):
                    view_all_btn = gr.Button("View All Memories", variant="primary")
                    filter_type_btn = gr.Button("Filter by Type")
                    filter_agent_btn = gr.Button("Filter by Agent")
                    search_btn = gr.Button("Search Memories")
            
            memories_output = gr.Dataframe(
                headers=["Timestamp", "Agent ID", "Type", "Content"],
                datatype=["str", "str", "str", "str"],
                label="Memory Contents",
                wrap=True
            )
            
            view_all_btn.click(
                fn=ui.get_all_memories,
                outputs=[memories_output]
            )
            
            filter_type_btn.click(
                fn=ui.get_memories_by_type,
                inputs=[memory_type],
                outputs=[memories_output]
            )
            
            filter_agent_btn.click(
                fn=ui.get_memories_by_agent,
                inputs=[agent_id],
                outputs=[memories_output]
            )
            
            search_btn.click(
                fn=ui.search_memories,
                inputs=[search_query],
                outputs=[memories_output]
            )
        
        gr.Markdown("""
        ## 📝 Instructions
        1. Go to the **Simulation Control** tab
        2. Set the number of agents you want to deploy
        3. Click "Run Full Simulation" to start
        4. Use the **Memory Explorer** tab to view results
        5. Clear memories if you want to start fresh
        
        ## 🔍 Memory Types
        - `food_preference`: Agent's favorite foods
        - `consumption`: What agents have eaten
        - `strategy`: Plans to counter the Singularity
        - `result`: Outcomes of strategies
        - `shutdown`: Final words from agents
        """)
    
    return app

def main():
    """Run the Gradio UI."""
    # Configure logging before anything else
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True
    )
    
    # Create and launch the UI
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        share=True
    )

if __name__ == "__main__":
    main() 