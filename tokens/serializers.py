from rest_framework.serializers import Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class TokenRenewSerializer(Serializer):
  refresh = CharField()

  def validate(self, attrs):
    refresh = RefreshToken(attrs['refresh'])
    data = {'access': str(refresh.access_token)}

    # 86400 seconds == 1 day
    token_exp = int(refresh.payload.get('exp'))
    current_time = int(refresh.current_time.timestamp())
    exp_days_left = round((token_exp - current_time) / 86400, 2)
    if exp_days_left < 2:
      refresh.blacklist()

      user_id = refresh.payload.get('user_id')
      user = User.objects.filter(id=user_id).first()
      if user:
        new_refresh = RefreshToken.for_user(user)
        data = {
          'refresh': str(new_refresh),
          'access': str(new_refresh.access_token)
        }

    return data