from users.serializers import UserSerializer
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def UserView(request):
    """
    Show the user info.
    https://www.django-rest-framework.org/api-guide/filtering/
    """
    try:
        user = User.objects.filter(id = request.user.id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    except user.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
