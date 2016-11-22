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
          pprint("1----------------------\n")
          # pprint(message)
          if 'is_echo' in message['message']:
            continue
        
          if 'text' not in message['message']:
            post_facebook_message(message['sender']['id'], 'not found')
          else:
            pprint("2----------------------\n")
              post_facebook_message(message['sender']['id'], message['message']['text'])
  return HttpResponse('something')



# Helper Function
def post_facebook_message(fbid, recevied_message):
  responses = {
    'hey': {"recipient":{"id":fbid}, "message":{"text": "Hi! Welcome to your event. What stadium are you at today?"}},
      'MCG': {"recipient":{"id":fbid}, "message":{"text": "Awesome! Can I have your seat number?"}},
        'B12': {"recipient":{"id":fbid}, "message":{"text": "Great. Here are some food options near you!"}},
    'Cool!': {
      "recipient":{
      "id":fbid }, "message": {
      "attachment": {
        "type": "template",
          "payload": {
            "template_type": "generic",
              "elements": [
                           {
                           "title": "KFC",
                           "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png",
                           "subtitle": "10 Piece Chicken, Fries, Beer: 20$",
                           "default_action": {
                           "type": "web_url",
                           "url": "https://www.kfc.com.au",
                           "messenger_extensions": True,
                           "webview_height_ratio": "tall",
                           "fallback_url": "https://localhost/blah"
                           },
                           "buttons": [
                                       {
                                       "title": "Purchase",
                                       "type": "web_url",
                                       "url": "https://localhost/blah",
                                       "messenger_extensions": True,
                                       "webview_height_ratio": "tall",
                                       "fallback_url": "https://localhost/blah2"
                                       },
                                       {
                                       "title": "View More",
                                       "type": "web_url",
                                       "url": "https://localhost/blah",
                                       "messenger_extensions": True,
                                       "webview_height_ratio": "tall",
                                       "fallback_url": "https://localhost/blah2"
                                       }
                                       
                                       ]
                           },
                           {
                           "title": "McDonalds",
                           "image_url": "https://yt3.ggpht.com/-avTHbIvvjKY/AAAAAAAAAAI/AAAAAAAAAAA/GtO4B-SrWkA/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
                           "subtitle": "Big Mac, Medium Fries, Cola: 15$",
                           "default_action": {
                           "type": "web_url",
                           "url": "https://www.McDonalds.com",
                           "messenger_extensions": True,
                           "webview_height_ratio": "tall",
                           "fallback_url": "https://localhost/blah"
                           },
                           "buttons": [
                                       {
                                       "title": "Purchase",
                                       "type": "web_url",
                                       "url": "https://localhost/blah",
                                       "messenger_extensions": True,
                                       "webview_height_ratio": "tall",
                                       "fallback_url": "https://localhost/blah2"
                                       },
                                       {
                                       "title": "View More",
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
  }
  }
  
  # Remove all punctuations, lower case the text and split it based on space
  
  if recevied_message in responses:
    txt_back = responses[recevied_message]
  else:
    txt_back = {"recipient":{"id":fbid}, "message":{"text": "I didin't understand you. Sorry!"}}
  post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=EAAT6SYsWaHABAO1yvU1rdu5LKtsnZAyuiwjtYyWBlbMnwC45yGrBPwPNu5eSHiIwN6C3mx3S8hFsU0HhanmuQk6vgfJa1mmEOeNjdOSvhuks2QxLp4aOstMFgT1HF5mRZAP9RSLvlvobwISRkskCZB3x24K0wUZAyZByUa4B3fAZDZD"

#curl -X POST -H "Content-Type: application/json" -d '{
#"setting_type" : "domain_whitelisting",
#  "whitelisted_domains" : ["https://localhost"],
#  "domain_action_type": "add"
#}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAT6SYsWaHABAO1yvU1rdu5LKtsnZAyuiwjtYyWBlbMnwC45yGrBPwPNu5eSHiIwN6C3mx3S8hFsU0HhanmuQk6vgfJa1mmEOeNjdOSvhuks2QxLp4aOstMFgT1HF5mRZAP9RSLvlvobwISRkskCZB3x24K0wUZAyZByUa4B3fAZDZD"

#response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":txt_back}})
#  print(fbid)
pprint("3----------------------\n")
  #  print(txt_back)
  response_msg = json.dumps(txt_back)
  
  status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
  pprint("4----------------------\n")
  pprint(status.json())
