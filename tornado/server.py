from tornado import ioloop, web, httpserver
from tornado.escape import json_decode as decode, json_encode as encode
from tornado import database
import brukva
from brukva import adisp

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis = brukva.Client(REDIS_HOST, REDIS_PORT)
redis.connect()
redis.select(9)



"""
  advertiser_<id> : {'advertiser' : message, ...}
  patron_<id> : {'patron' : message, ...}
  in_app_<id> : [message, ...]
  push_<id> : [message, ...]
"""

class MessageHandler(web.RequestHandler):
  @web.asynchronous
  @adisp.process
  def get(self, identifier):
    res = {}
    res['advertisers'] = yield redis.async.hgetall('advertisers_' + identifier)
    res['patrons'] = yield redis.async.hgetall('patrons_' + identifier)
    res['messages'] = yield redis.async.hgetall('messages_' + identifier)
    res['notifications'] = yield redis.async.hgetall('notifications_' + identifier)
    self.write(encode(res))
    self.finish()
    
  @web.asynchronous
  @adisp.process
  def post(self, identifier):
    kind    = self.get_argument("kind")
    message = self.get_argument("message")
    sender  = self.get_argument("sender")
    if kind == 'advertiser':
      yield redis.async.hset('advertisers_' + identifier, sender, message)
    elif kind == 'patron':
      yield redis.async.hset('patrons_' + identifier, sender, message)
    elif kind == 'message':
      yield redis.async.hset('messages_' + identifier, sender, message)
    else:
      yield redis.async.hset('notifications_' + identifier, sender, message)
    self.write("")
    self.finish()
    
class LinkHandler(web.RequestHandler):
  @classmethod
  def sql(cls,code):
    base = {
      'u' : "select url from links where code_type = 'user' and code = '%s' limit 1",
      't' : "select url from links where code_type = 'transaction' and code = '%s' limit 1",
      'p' : "select url from links where code_type = 'patron' and code = '%s' limit 1"
    }.get(code[0], None)
    return base and base %code[1:]
  
  @web.asynchronous
  def get(self, code):
    sql = LinkHandler.sql(code)
    if sql:
      url = mysql.query(sql)['url']
      self.redirect(url)
    else:
      raise web.HTTPError(404)
    self.finish()
      

if __name__ == "__main__":
  application = web.Application([
    (r"/werw_mq/([a-z0-9]+)", MessageHandler),
    (r"/link/([a-z0-9]+)", LinkHandler),
  ])
  application.listen(8888)
  ioloop.IOLoop.instance().start()
  
