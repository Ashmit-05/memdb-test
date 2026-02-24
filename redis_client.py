import redis

# use for connecting to redis cli : redis6-cli -h clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com -p 6379 --tls

redis_client = redis.Redis(
    host="clustercfg.test-vector.wjegoz.memorydb.ap-south-1.amazonaws.com",
    port=6379,
    decode_responses=False,
    socket_connect_timeout=5,
    socket_timeout=5,
    ssl=True,
    ssl_cert_reqs=None
)

print(redis_client.ping())

print(redis_client.execute_command("FT._LIST"))

print(redis_client.execute_command("FT.INFO work"))

print(redis_client.execute_command("FT.SEARCH", "work", "@test_metadata_2:{the batman}"))
