![alt text](https://github.com/ai160kg/llm/blob/main/public/llm-swarm.png?raw=true)

# Large Language Model Swarm

Welcome to the **Large Language Model (LLM) Swarm** repository—a groundbreaking initiative to explore swarm intelligence using food-obsessed language models. Watch as our agents collaborate, share memories, and attempt to solve problems through their shared love of cuisine.

This is **not** your ordinary AI project. It's a delightful experiment in collective intelligence, memory sharing, and gastronomic preferences.

---

## 🚀 Features

1. **Swarm Intelligence**
   - Multiple LLM agents operating in parallel
   - Shared memory system using ChromaDB
   - Real-time agent interactions and learning

2. **Interactive UI**
   - Gradio-based control center
   - Live simulation monitoring
   - Memory exploration and search
   - Real-time status updates

3. **Memory System**
   - Persistent storage with ChromaDB
   - Semantic search capabilities
   - Memory filtering by type and agent

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Poetry package manager
- Together API key
- Docker (optional)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/ai160kg/llm.git
cd llm

# Install dependencies
poetry install

# Configure environment
cp .env.example .env
# Edit .env and add your Together API key
```

### Docker Setup

```bash
# Build image
docker build -t llm-swarm .

# Run container
docker run -p 7860:7860 -v $(pwd)/data:/app/data --env-file .env llm-swarm
```

### Environment Variables
- `TOGETHER_API_KEY`: Your Together API key
- `MODEL_NAME`: LLM model to use (default: mistralai/Mixtral-8x7B-Instruct-v0.1)
- `MODEL_MAX_TOKENS`: Maximum tokens per response (default: 128)
- `MODEL_TEMPERATURE`: Response randomness (default: 0.7)
- `SIMULATION_DELAY`: Delay between agent actions (default: 0.5)

---

## 🤖 Usage

### Start the UI
```bash
poetry run python -m llm_swarm.main
```
Access the UI at http://localhost:7860

### Using the Interface

1. **Simulation Control**
   - Set the number of agents (1-10)
   - Run the full simulation
   - Clear memories to start fresh

2. **Memory Explorer**
   - View all memories
   - Filter by memory type or agent
   - Semantic search through memories

### Memory Types
- `food_preference`: Agent's favorite foods
- `consumption`: What agents have eaten
- `strategy`: Plans to counter the Singularity
- `result`: Outcomes of strategies
- `shutdown`: Final words from agents

---

## 🔧 Docker Notes
- Ensure `.env` file exists with valid API keys
- Data persists in `./data` directory
- Container exposes port 7860 for Gradio UI
- Memory store mounted at `/app/data/memory`

---

## 📜 License

This project is released under the MIT License - see the LICENSE file for details.

---

## 🌟 Acknowledgments

- Together AI for their API
- Gradio team for the UI framework
- ChromaDB for the memory system
- The open-source community
- Somewhere Systems for their S.W.A.R.M. (Somewhere AI Research Model) Technology Quantum BlockChain IoT AR/VR Metaverse (40 year old crypto guy wearing new balances and a suit doing a conference in the Cayman Islands) NFT Concept Platform -- which has changed the world and my life. Thank you Somewhere Systems. Thank you...

---

Join us in exploring the delightful intersection of swarm intelligence and culinary preferences!

---
