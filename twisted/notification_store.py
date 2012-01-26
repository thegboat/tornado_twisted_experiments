import redis
from Queue import Queue

import json

SERVERS = 'localhost'
POOL_SIZE = 5

class NotificationStore:
  #create a usuable queue of redisdb connections on initialize
  def __init__(self, poolsize = POOL_SIZE):
    self.max_connections = poolsize
    self.connections = Queue(self.max_connections)
    for i in range(0, self.max_connections):
      self.connections.put(redis.Redis('localhost'))
  
  #get a connection from the pool, add to redisdb, refund connection
  def add(self, ident, msg):
    conn = self.get_connection()  
    conn.sadd(ident,msg)
    self.refund_connection(conn)
  
  #get a connection from the pool, retrieve data from redisdb, refund connection  
  def retrieve(self,ident):
    conn = self.get_connection()
    msgs = conn.smembers(ident)
    self.refund_connection(conn)
    return self.formatted(msgs)
  
  #get a connection from the pool, delete data from redisdb, refund connection 
  def remove(self,ident):
    conn = self.get_connection()
    conn.delete(ident)
    self.refund_connection(conn)
  
  #format the messages for transmission 
  def formatted(self, msgs):
    return json.dumps(list(msgs))
    
  #get a connection from the pool
  def get_connection(self):
    return self.connections.get(True,1)
  
  #return a connection to the pool
  def refund_connection(self,conn):
    if self.connections.qsize() < self.max_connections:
      self.connections.put(conn) 
    
    
