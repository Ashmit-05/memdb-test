import redis

redis_client = redis.Redis(
    host="clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com",
    port=6379,
    decode_responses=False
)

print(redis_client.ping())
