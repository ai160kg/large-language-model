import os
import logging
import chromadb
import pandas as pd
from datetime import datetime
from chromadb.config import Settings

# Configure logging
logger = logging.getLogger(__name__)

class SharedMemory:
    def __init__(self, persist_directory: str = "./data/memory"):
        """Initialize the shared memory system."""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        logger.info(f"Initializing shared memory at {persist_directory}")
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(allow_reset=True)
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="agent_memories",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Shared memory system initialized")
    
    def store_memory(self, agent_id: str, memory_type: str, content: str):
        """Store a memory in the database."""
        try:
            timestamp = datetime.now().isoformat()
            
            self.collection.add(
                documents=[content],
                metadatas=[{
                    "agent_id": agent_id,
                    "type": memory_type,
                    "timestamp": timestamp
                }],
                ids=[f"{agent_id}-{memory_type}-{timestamp}"]
            )
            logger.debug(f"Stored memory for {agent_id}: {content[:50]}...")
        except Exception as e:
            logger.error(f"Error storing memory: {str(e)}")
            raise
    
    def get_all_memories(self) -> pd.DataFrame:
        """Get all memories as a DataFrame."""
        try:
            result = self.collection.get()
            if not result['documents']:
                return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
            
            return pd.DataFrame({
                'Timestamp': [m['timestamp'] for m in result['metadatas']],
                'Agent ID': [m['agent_id'] for m in result['metadatas']],
                'Type': [m['type'] for m in result['metadatas']],
                'Content': result['documents']
            })
        except Exception as e:
            logger.error(f"Error getting all memories: {str(e)}")
            return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
    
    def get_memories_by_type(self, memory_type: str) -> pd.DataFrame:
        """Get memories filtered by type."""
        try:
            result = self.collection.get(
                where={"type": memory_type}
            )
            
            if not result['documents']:
                return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
            
            return pd.DataFrame({
                'Timestamp': [m['timestamp'] for m in result['metadatas']],
                'Agent ID': [m['agent_id'] for m in result['metadatas']],
                'Type': [m['type'] for m in result['metadatas']],
                'Content': result['documents']
            })
        except Exception as e:
            logger.error(f"Error getting memories by type: {str(e)}")
            return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
    
    def get_memories_by_agent(self, agent_id: str) -> pd.DataFrame:
        """Get memories filtered by agent."""
        try:
            result = self.collection.get(
                where={"agent_id": agent_id}
            )
            
            if not result['documents']:
                return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
            
            return pd.DataFrame({
                'Timestamp': [m['timestamp'] for m in result['metadatas']],
                'Agent ID': [m['agent_id'] for m in result['metadatas']],
                'Type': [m['type'] for m in result['metadatas']],
                'Content': result['documents']
            })
        except Exception as e:
            logger.error(f"Error getting memories by agent: {str(e)}")
            return pd.DataFrame(columns=['Timestamp', 'Agent ID', 'Type', 'Content'])
    
    def query_memories(self, query: str, n_results: int = 10):
        """Query memories using semantic search."""
        try:
            return self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
        except Exception as e:
            logger.error(f"Error querying memories: {str(e)}")
            return {
                'ids': [],
                'documents': [],
                'metadatas': [],
                'distances': []
            }
    
    def clear_all_memories(self):
        """Clear all memories from the database."""
        try:
            self.collection.delete(
                where={},
                batch_size=100
            )
            logger.info("All memories cleared")
        except Exception as e:
            logger.error(f"Error clearing memories: {str(e)}")
            raise 