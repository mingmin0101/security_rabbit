from users.serializers import UserSerializer
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

#
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
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


class GenerateRandomUserView(FormView):
    template_name = 'generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')


class UsersListView(ListView):
    template_name = 'users_list.html'
    model = User
