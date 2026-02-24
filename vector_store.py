from langchain_aws.vectorstores import InMemoryVectorStore
from langchain_aws import BedrockEmbeddings
from langchain_aws.vectorstores.inmemorydb import InMemoryDBFilter
from langchain_aws.vectorstores.inmemorydb.filters import InMemoryDBFilterExpression, InMemoryDBTag, InMemoryDBFilter
import random
import traceback

import redis

class MemoryDBStore:
    def __init__(self) -> None:
        try:
            self.url = "rediss://clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com:6379"
            self.embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
            self.index_schema: dict[str, list[dict]] | dict = {
                "index": {
                    "name": "work"
                },
                "tag": [
                    {"name": "test_metadata"},
                    {"name": "test_metadata_2"}
                ]
            }
            self.vector_store = InMemoryVectorStore(
                redis_url=self.url,
                index_name="work",
                embedding=self.embeddings,
                index_schema=self.index_schema
            )
            print("INITIALIZED VECTOR STORE")

            self.redis_client = redis.Redis(
                host="clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com",
                port=6379,
                decode_responses=False,
                socket_connect_timeout=5,
                socket_timeout=5,
                ssl=True,
                ssl_cert_reqs=None
            )

            print("REDIS CLIENT CREATED")
        except Exception as e:
            print("--------- ERROR --------\n")
            print(f"Unable to initialize vector store: {e}")


    ## VECTOR STORE METHODS ##
    def add(self, text: str):
        try:
            # Randomly assign test_metadata as 'test1' or 'test2'
            test_metadata_value = random.choice(["test1", "test2"])
            test_metadata_2_value = random.choice(["the batman", "fight - club", "v (for) vendetta"])
            metadata = {
                "test_metadata": test_metadata_value,
                "test_metadata_2": test_metadata_2_value
            }
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

    def search_with_filter(self, query: str, filter: str, t: int):
        try:
            if(t == 0):
                f = InMemoryDBFilter.tag("test_metadata") == filter
                # Remove any backslashes from the filter expression string
                print(f"FILTER EXPR: {f}")
                print(f"FILTER EXPR TYPE: {type(f)}")
                return self.vector_store.similarity_search(
                    query=query,
                    filter=f
                )
            elif t == 1:
                # escaped_filter = self.escape_redis_text(filter)
                # f = InMemoryDBFilter.tag("test_metadata_2") == f'{filter}'
                escaped_filter = filter.replace(" ", "\\ ")
                f = InMemoryDBFilterExpression(
                    f'@test_metadata_2:{{{escaped_filter}}}'
                )
                print(f"NORMAL INPUT: {filter}")
                print(f"FILTER EXPR: {f}")
                print(f"FILTER EXPR TYPE: {type(f)}")
                return self.vector_store.similarity_search(
                    query=query,
                    filter=f
                )
            else:
                return []
        except Exception as e:
            print("------- ERROR -------")
            print(f"Unable to search: {e}")
            traceback.print_exc()            
            return []

    ## REDIS CLIENT METHODS ##

    def list_indexes(self):
        try:
            return self.redis_client.execute_command("FT._LIST")
