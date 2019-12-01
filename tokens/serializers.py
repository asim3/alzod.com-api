from rest_framework.serializers import Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken


class TokenRenewSerializer(Serializer):
  refresh = CharField()

  def validate(self, attrs):
    refresh = RefreshToken(attrs['refresh'])
    token_exp = int(refresh.payload.get('exp'))
    current_time = int(refresh.current_time.timestamp())
    # 86400 seconds == 1 day
    expiration = round((token_exp - current_time) / 86400, 3)
    data = {
      'access': str(refresh.access_token),
      'expiration': expiration
    }
    if expiration < 1:
      refresh.blacklist()
      refresh.set_jti()
      refresh.set_exp()
      data['refresh'] = str(refresh)

    return data