from pymilvus import connections, Collection
import os
from dotenv import load_dotenv

load_dotenv()

class MilvusDbService:
    def __init__(self):
        connections.connect("default", host=os.getenv("MILVUS_HOST"), port=os.getenv("MILVUS_PORT"))

    async def query_knowledge_async(self, query_text: str, collection_id: str):
        try:
            collection = Collection(collection_id)
            results = collection.query(
                expr=f"content like '%{query_text}%'",
                output_fields=["content"],
                limit=3
            )
            context = " ".join([r["content"] for r in results]) if results else ""
            return context
        except Exception as e:
            print("Milvus error:", e)
            return ""
