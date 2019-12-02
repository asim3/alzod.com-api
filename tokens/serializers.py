from rest_framework.serializers import Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class TokenRenewSerializer(Serializer):
  refresh = CharField()

  def validate(self, attrs):
    refresh = RefreshToken(attrs['refresh'])
    token_exp = int(refresh.payload.get('exp'))
    current_time = int(refresh.current_time.timestamp())
    # 86400 seconds == 1 day
    exp_days_left = round((token_exp - current_time) / 86400, 2)
    minimum_days = 2
    data = {
      'access': str(refresh.access_token),
      'delete user_id': refresh.payload.get('user_id'),
      'delete all': refresh.payload,
      'delete this': exp_days_left
    }
    if exp_days_left < minimum_days:
      refresh.blacklist()
      user_id = refresh.payload.get('user_id')
      user = User.objects.filter(id=user_id).first()
      if user:
        new_refresh = RefreshToken.for_user(user)
        data['refresh'] = str(new_refresh)

    return data