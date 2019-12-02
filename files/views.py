from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView


class AddView(CreateAPIView):
  "serializer_class = ccc"


class UpdateView(RetrieveUpdateDestroyAPIView):
  pass