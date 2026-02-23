from langchain_aws.vectorstores import InMemoryVectorStore
from langchain_aws import BedrockEmbeddings
from langchain_aws.vectorstores.inmemorydb import InMemoryDBFilter
from langchain_aws.vectorstores.inmemorydb.filters import InMemoryDBFilterExpression, InMemoryDBTag
import random
import traceback

class MemoryDBStore:
    def __init__(self) -> None:
        try:
            self.url = "rediss://clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com:6379"
            self.embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
            self.index_schema: dict[str, list[dict]] | dict = {
                "index": {
                    "name": "check"
                },
                "tag": [
                    {"name": "test_metadata"}
                ]
            }
            self.vector_store = InMemoryVectorStore(
                redis_url=self.url,
                index_name="check",
                embedding=self.embeddings,
                index_schema=self.index_schema
            )
            print("INITIALIZED VECTOR STORE")
        except Exception as e:
            print("--------- ERROR --------\n")
            print(f"Unable to initialize vector store: {e}")

    def add(self, text: str):
        try:
            # Randomly assign test_metadata as 'test1' or 'test2'
            test_metadata_value = random.choice(["fight club", "the batman"])
            metadata = {"test_metadata": test_metadata_value}
            return self.vector_store.add_texts(
                texts=[text],
                metadatas=[metadata]
            )
        except Exception as e:
            print("------- ERROR -------")
            print(f"Unable to add texts: {e}")

    def search(self, query: str):
        try:
            return self.vector_store.search(query, "similarity")
        except Exception as e:
            print("------- ERROR -------")
            print(f"Unable to search: {e}")
            return []

    def search_with_filter(self, query: str, filter: str):
        try:
            f = InMemoryDBTag("test_metadata") == filter
            print(f"FILTER EXPR: {f}")
            print(f"FILTER EXPR TYPE: {type(f)}")
            return self.vector_store.similarity_search(
                query=query,
                filter=f
            )
        except Exception as e:
            print("------- ERROR -------")
            print(f"Unable to search: {e}")
            traceback.print_exc()            
            return []


