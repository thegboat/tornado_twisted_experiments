from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from notification_store import NotificationStore
import cgi

class RootResource(Resource):
  def __init__(self, notification_store):
    self.notification_store = notification_store
    Resource.__init__(self)                   

  def getChild(self, path, request):
    return MessageHandler(path, notification_store)

class MessageHandler(Resource):
  def __init__(self, identifier, notification_store):
    Resource.__init__(self)
    self.notification_store = notification_store
    self.identifier = identifier

  def render_GET(self, request):
    msgs = notification_store.retrieve(self.identifier)
    notification_store.remove(self.identifier)
    return msgs
    
  def render_POST(self,request):
    notification_store.add(self.identifier, cgi.escape(request.args["message"][0]))
    return ""

notification_store = NotificationStore()
root = RootResource(notification_store)
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()