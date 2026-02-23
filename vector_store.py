from langchain_aws.vectorstores import InMemoryVectorStore
from langchain_aws import BedrockEmbeddings
from langchain_aws.vectorstores.inmemorydb import InMemoryDBFilter
from langchain_aws.vectorstores.inmemorydb.filters import InMemoryDBFilterExpression
import random

class MemoryDBStore:
    def __init__(self) -> None:
        try:
            self.url = "rediss://clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com:6379"
            self.embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
            self.index_schema: dict[str, list[dict]] | dict = {
                "index": {
                    "name": "test"
                },
                "text": [
                    {"name": "test_metadata"}
                ]
            }
            self.vector_store = InMemoryVectorStore(
                redis_url=self.url,
                index_name="test",
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
            test_metadata_value = random.choice(["test1", "test2"])
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
            filter_str = f'@test_metadata: "{filter}"'
            f = InMemoryDBFilterExpression(_filter=filter_str)
            # Print the filter string directly, not format_expression()
            print(f"FILTER EXPR: {f._filter}")
            print(f"FILTER EXPR TYPE: {type(f)}")
            return self.vector_store.similarity_search(
                query=query,
                filter=f._filter
            )
        except Exception as e:
            print("------- ERROR -------")
            print(f"Unable to search: {e}")
            
            return []


