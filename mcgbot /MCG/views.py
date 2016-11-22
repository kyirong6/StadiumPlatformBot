import json, requests, random, re
from pprint import pprint
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class index(generic.View):
  
  
  def get(self, request, *args, **kwargs):
    if self.request.GET['hub.verify_token'] == '1218':
      return HttpResponse(self.request.GET['hub.challenge'])
    else:
      return HttpResponse('Error, invalid token')


@method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return generic.View.dispatch(self, request, *args, **kwargs)
  
  # Post function to handle Facebook messages
  def post(self, request, *args, **kwargs):
    # Converts the text payload into a python dictionary
    incoming_message = json.loads(self.request.body.decode('utf-8'))
    # Facebook recommends going through every entry since they might send
    # multiple messages in a single call during high load
    for entry in incoming_message['entry']:
      for message in entry['messaging']:
        # Check to make sure the received call is a message call
        # This might be delivery, optin, postback for other events
        if 'message' in message:
          # Print the message to the terminal
          pprint(message)
          post_facebook_message(message['sender']['id'], "blah")
    return HttpResponse()


# Helper Function
def post_facebook_message(fbid, recevied_message):
  responses = {
    'hey': "Hey! How are you?",
      'hello': "Hey! How are you?"   ,
        '55': "Awesome! Here are some options near you."
    }

# Remove all punctuations, lower case the text and split it based on space
tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
  txt_back = ''
  for token in tokens:
    if token in responses:
      txt_back = responses[token]
      break
if not responses:
  txt_back = "I didn't understand! Sorry!"
  post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=EAAT6SYsWaHABAO1yvU1rdu5LKtsnZAyuiwjtYyWBlbMnwC45yGrBPwPNu5eSHiIwN6C3mx3S8hFsU0HhanmuQk6vgfJa1mmEOeNjdOSvhuks2QxLp4aOstMFgT1HF5mRZAP9RSLvlvobwISRkskCZB3x24K0wUZAyZByUa4B3fAZDZD"
  
  #curl -X POST -H "Content-Type: application/json" -d '{
  #"setting_type" : "domain_whitelisting",
  #  "whitelisted_domains" : ["https://localhost"],
  #  "domain_action_type": "add"
  #}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAT6SYsWaHABAO1yvU1rdu5LKtsnZAyuiwjtYyWBlbMnwC45yGrBPwPNu5eSHiIwN6C3mx3S8hFsU0HhanmuQk6vgfJa1mmEOeNjdOSvhuks2QxLp4aOstMFgT1HF5mRZAP9RSLvlvobwISRkskCZB3x24K0wUZAyZByUa4B3fAZDZD"
  
  #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":txt_back}})
  print(fbid)
  response_msg = json.dumps({
                            "recipient":{
                            "id":fbid }, "message": {
                            "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "list",
                            "elements": [
                                         {
                                         "title": "Classic T-Shirt Collection",
                                         "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png",
                                         "subtitle": "See all our colors",
                                         "default_action": {
                                         "type": "web_url",
                                         "url": "https://localhost/blah",
                                         "messenger_extensions": True,
                                         "webview_height_ratio": "tall",
                                         "fallback_url": "https://localhost/blah"
                                         },
                                         "buttons": [
                                                     {
                                                     "title": "View",
                                                     "type": "web_url",
                                                     "url": "https://localhost/blah",
                                                     "messenger_extensions": True,
                                                     "webview_height_ratio": "tall",
                                                     "fallback_url": "https://localhost/blah2"
                                                     }
                                                     ]
                                         },
                                         {
                                         "title": "Classic T-Shirt Collection",
                                         "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png",
                                         "subtitle": "See all our colors",
                                         "default_action": {
                                         "type": "web_url",
                                         "url": "https://localhost/blah",
                                         "messenger_extensions": True,
                                         "webview_height_ratio": "tall",
                                         "fallback_url": "https://localhost/blah"
                                         },
                                         "buttons": [
                                                     {
                                                     "title": "View",
                                                     "type": "web_url",
                                                     "url": "https://localhost/blah",
                                                     "messenger_extensions": True,
                                                     "webview_height_ratio": "tall",
                                                     "fallback_url": "https://localhost/blah2"
                                                     }
                                                     ]
                                         }
                                         ]  
                            }
                            }
                            }
                            
                            })
                            
  status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
#  pprint(status.json())
