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
    return HttpResponse()
