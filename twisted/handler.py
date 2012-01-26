from notification_store import NotificationStore

constant 

class Handler():
  def __init__(self, id):
    self.in_app_messages = []
    self.push_messages = []
    self.advertiser_messages = {}
    self.patron_messages = {}
    
  def empty(self):
    cnt = len(self.in_app_messages)
    cnt += len(self.push_messages)
    cnt += len(self.advertiser_messages)
    cnt += len(self.patron_messages)
    return cnt == 0
    
  def datastore(cls):
    
    
  @classmethod
  def find_or_create(cls,identifier):
    key, value 
    
    