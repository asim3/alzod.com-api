from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework_simplejwt.views import token_obtain_pair
import json


@csrf_exempt
def register_view(request):
  if request.method=='POST':
    form = UserCreationForm(json.loads(request.body))
    if form.is_valid():
      form.save()
      return token_obtain_pair(request)
    
    form_error = json.dumps(dict(form.errors.items()))
    return HttpResponseBadRequest(form_error, content_type="application/json")

  er = '{"detail": "Method %s not allowed."}' % request.method
  return HttpResponseNotAllowed(['POST'], er, content_type="application/json")