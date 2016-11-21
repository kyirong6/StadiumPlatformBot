from django.http import HttpResponse
from django.http.response import HttpResponse
from django.views import generic

# Create your views here.
class index(generic.View):
  def get(self, request, *args, **kwargs):
    if self.request.GET['hub.verify_token'] == '1218':
      return HttpResponse(self.request.GET['hub.challenge'])
    else:
      return HttpResponse('Error, invalid token')
