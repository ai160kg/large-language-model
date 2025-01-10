import sys
import logging
import argparse
from colorama import init, Fore, Style, AnsiToWin32
from dotenv import load_dotenv
from .agents.swarm import LargeLanguageModelSwarm
from .ui.app import create_ui

# Initialize colorama for cross-platform color support with forced color output
init(wrap=True, convert=True, strip=False, autoreset=True)
sys.stdout = AnsiToWin32(sys.stdout).stream

# Configure logging with forced colors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(AnsiToWin32(sys.stdout).stream)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def run_simulation():
    """Run the swarm simulation in CLI mode."""
    try:
        logger.info(f"{Fore.GREEN}[WELCOME] Initializing Large Language Model Swarm Deployment...{Style.RESET_ALL}\n")
        swarm = LargeLanguageModelSwarm(persist_directory="./data/memory")
        
        logger.info(f"{Fore.YELLOW}[STEP 1] Deploying agents...{Style.RESET_ALL}")
        swarm.deploy_agents()
        
        logger.info(f"\n{Fore.YELLOW}[STEP 2] Simulating their consumption habits...{Style.RESET_ALL}")
        swarm.simulate_consumption()
        
        logger.info(f"\n{Fore.YELLOW}[STEP 3] Counteracting the Singularity...{Style.RESET_ALL}")
        swarm.counter_singularity()
        
        logger.info(f"\n{Fore.YELLOW}[STEP 4] Ending the simulation...{Style.RESET_ALL}")
        swarm.shutdown()
        
        logger.info(f"\n{Fore.MAGENTA}[CONCLUSION] Simulation terminated. Don't die. #LiveForever #KeepItPlatinum{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}[ERROR] An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def run_ui():
    """Run the Gradio UI interface."""
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        share=True
    )

def main():
    parser = argparse.ArgumentParser(description='LLM Swarm - A swarm of large language models that love to eat')
    parser.add_argument('--mode', '-m', choices=['ui', 'cli'], default='ui',
                      help='Run mode: ui (default) for Gradio interface, cli for command line simulation')
    
    args = parser.parse_args()
    
    if args.mode == 'ui':
        run_ui()
    else:
        run_simulation()

if __name__ == "__main__":
    main() 