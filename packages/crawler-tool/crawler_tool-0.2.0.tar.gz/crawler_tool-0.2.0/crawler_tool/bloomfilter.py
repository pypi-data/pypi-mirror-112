# -*- coding: utf-8 -*-
import redis
from hashlib import md5

"""
布隆过滤器可以把它看作是由二进制向量（或者说位数组）和一系列随机映射函数（哈希函数）两部分组成的数据结构。

当字符串存储要加入布隆过滤器是，该字符串首先由多个哈希函数生成不同的哈希值，然后在对应的位数组的下标的元素
设置为1。
如果我们需要判断某个字符串是否在布隆过滤器中时，只需要对给定的字符串再次进行相同的哈希计算，得到值之后判断
位数组中的每个元素是否都为1，如果值都为1，那么说明这个值在布隆过滤器中，如果存在一个值不为1，说明该元素不在布隆过滤器中。

优点：
    由于存放的不是完整的数据，所以占用的内存很少；而且新增、查询速度够快。
缺点：
    其返回的结果是概率性的，而不是非常准确的，理论形况下添加到集合中的元素越多，误报的可能性就越大。
    并且存放在博隆过滤器的数据不容易删除，只能判断数据是否一定不存在，而无法判断数据是否一定存在。

使用场景：
    判断给定数据是否存在：比如判断一个数字是否在于包含大量数字的数字集中（数字集很大，5亿以上！）、 
    防止缓存穿透（判断请求的数据是否有效避免直接绕过缓存请求数据库）等等、邮箱的垃圾邮件过滤、黑名单功能等等。
    去重：比如爬给定网址的时候对已经爬取过的 URL 去重。
"""

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, REDIS_URL, DB, blockNum=1, key='bloom_taobao'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        # self.server = redis.Redis(REDIS_URL)
        self.server = redis.from_url(REDIS_URL, DB)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

    def delect(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 0)



