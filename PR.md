# LLM Swarm UI Enhancement

## Changes
- Integrated Together API for DeepSeek V3 model
- Added Poetry for dependency management
- Implemented ChromaDB for shared memory
- Created Gradio UI with real-time updates
- Added simulation controls and memory explorer

## Testing
- Verify Together API key in `.env`
- Run `poetry install`
- Start UI: `poetry run python -m llm_swarm.main`
- Test simulation with different agent counts
- Verify real-time updates in UI
- Check memory persistence 

## Docker Setup
- Build image: `docker build -t llm-swarm .`
- Run container: `docker run -p 7860:7860 -v $(pwd)/data:/app/data --env-file .env llm-swarm`
- Access UI at `http://localhost:7860`

### Docker Notes
- Ensure `.env` file exists with valid API keys
- Data persists in `./data` directory
- Container exposes port 7860 for Gradio UI
- Memory store mounted at `/app/data/memory`
