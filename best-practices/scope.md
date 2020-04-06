---
Title: Scope
...

# Scope

### Director is NOT intended for any of the following:

- Running machine learning programs or other computationally intensive tasks. The TJ Computer Systems Laboratory has a high-performance computing cluster and two GPU workstations specifically for this purpose.
- Running large-scale servers like [Redis](https://redis.io/). [^1]

[^1]: <small>In the case of Redis specifically, there are often alternatives. For example, Django Channels recommends using Redis as the channel layer, but you can often use an [in-memory layer](https://channels.readthedocs.io/en/latest/topics/channel_layers.html#in-memory-channel-layer) instead.</small>
