from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TokenRenewSerializer
import json

class TokenRenewView(TokenViewBase):
  serializer_class = TokenRenewSerializer


def get_data_from_json(request):
  try:
    return json.loads(request.body)
  except:
    return {'json.loads': 'error'}


@csrf_exempt
def register_view(request):
  if request.method=='POST':
    form = UserCreationForm(get_data_from_json(request))
    if form.is_valid():
      user = form.save()
      refresh = RefreshToken.for_user(user)
      r = str(refresh)
      a = str(refresh.access_token)
      return HttpResponse(
        '{"refresh":"%s", "access":"%s"}' % (r, a,), 
        content_type="application/json"
      )
    
    form_error = json.dumps(dict(form.errors.items()))
    return HttpResponseBadRequest(form_error, content_type="application/json")

  er = '{"detail": "Method %s not allowed."}' % request.method
  return HttpResponseNotAllowed(['POST'], er, content_type="application/json")