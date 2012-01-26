import APNSWrapper
import binascii
deviceToken = binascii.unhexlify('99abd394d0560c78dd0fcf83a3e0a66f06b2ecabed35139fde3d91ecc5a82594')
# create wrapper
wrapper = APNSWrapper.APNSNotificationWrapper('apple_push_notification_production.pem', True)

# create message
message = APNSWrapper.APNSNotification()
message.token(deviceToken)
message.alert('Please work')
message.badge(5)

# add message to tuple and send it to APNS server
wrapper.append(message)
wrapper.notify()