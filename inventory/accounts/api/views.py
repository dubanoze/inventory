# -*- coding: utf-8 -*-
#
# inventory/accounts/api/views.py
#

import logging

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, login, logout
from django.utils.translation import ugettext_lazy as _

from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
    GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from rest_condition import C, And, Or, Not

from inventory.common.api.permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive, IsPostOnly)
from inventory.common.api.pagination import SmallResultsSetPagination
from inventory.common.api.view_mixins import (
    TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin)

from ..models import Question, Answer
from .serializers import (
    UserSerializer, PublicUserSerializer, QuestionSerializer, AnswerSerializer,
    LoginSerializer)

log = logging.getLogger('api.accounts.views')
UserModel = get_user_model()


#
# User
#
class UserAuthorizationMixin(object):
    serializers = {
        'default': UserSerializer,
        'public': PublicUserSerializer
        }

    def get_serializer_class(self):
        serializer = None

        if (self.request.user.is_superuser
            or self.request.user.role == UserModel.ADMINISTRATOR
            or (self.kwargs and self.request.user == self.get_object())):
            serializer = self.serializers.get('default')
        else:
            serializer = self.serializers.get('public')

        return serializer

    def get_queryset(self):
        return UserModel.objects.all()


class UserList(TrapDjangoValidationErrorCreateMixin,
               UserAuthorizationMixin,
               ListCreateAPIView):
    """
    User list endpoint.
    """
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly,
                   Or(IsDefaultUser,
                      IsAnyProjectUser)
                   )
               )
            ),
        )
    pagination_class = SmallResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    lookup_field = 'public_id'

user_list = UserList.as_view()


class UserDetail(TrapDjangoValidationErrorUpdateMixin,
                 UserAuthorizationMixin,
                 RetrieveUpdateAPIView):
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               Or(IsAnyUser,
                  IsAnyProjectUser
                  )
               )
            ),
        )
    lookup_field = 'public_id'

user_detail = UserDetail.as_view()


#
# Group
#
## class GroupAuthorizationMixin(object):

##     def get_queryset(self):
##         if (self.request.user.is_superuser or
##             self.request.user.role == UserModel.ADMINISTRATOR):
##             result = Group.objects.all()
##         else:
##             result = self.request.user.groups.all()

##         return result


## class GroupList(TrapDjangoValidationErrorCreateMixin,
##                 GroupAuthorizationMixin,
##                 ListCreateAPIView):
##     """
##     Group list endpoint.
##     """
##     serializer_class = GroupSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)
##     pagination_class = SmallResultsSetPagination

## group_list = GroupList.as_view()


## class GroupDetail(TrapDjangoValidationErrorUpdateMixin,
##                   GroupAuthorizationMixin,
##                   RetrieveUpdateAPIView):
##     serializer_class = GroupSerializer
##     permission_classes = (
##         And(IsUserActive, #IsAuthenticated,
##             Or(IsAdminSuperUser,
##                IsAdministrator)
##             ),
##         )
##     required_scopes = ('read', 'write', 'groups',)

## group_detail = GroupDetail.as_view()


#
# Question
#
class QuestionList(TrapDjangoValidationErrorCreateMixin,
                   ListCreateAPIView):
    """
    Question list endpoint.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, Or(IsDefaultUser,
                                  IsAnyProjectUser)
                   )
               )
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

question_list = QuestionList.as_view()


class QuestionDetail(TrapDjangoValidationErrorUpdateMixin,
                     RetrieveUpdateAPIView):
    """
    Question detail endpoint.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
         And(IsUserActive, IsAuthenticated,
            Or(IsAdminSuperUser,
               IsAdministrator,
               And(IsReadOnly, Or(IsDefaultUser,
                                  IsAnyProjectUser)
                   )
               )
            ),
        )
    lookup_field = 'public_id'

question_detail = QuestionDetail.as_view()


#
# Answer
#
class AnswerAuthorizationMixin(object):

    def get_queryset(self):
        if (self.request.user.is_superuser or
            self.request.user.role == UserModel.ADMINISTRATOR):
            result = Answer.objects.all()
        else:
            result = self.request.user.answers.all()

        return result


class AnswerList(TrapDjangoValidationErrorCreateMixin,
                 AnswerAuthorizationMixin,
                 ListCreateAPIView):
    """
    Answer list endpoint.
    """
    serializer_class = AnswerSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    pagination_class = SmallResultsSetPagination
    lookup_field = 'public_id'

answer_list = AnswerList.as_view()


class AnswerDetail(TrapDjangoValidationErrorUpdateMixin,
                   AnswerAuthorizationMixin,
                   RetrieveUpdateDestroyAPIView):
    """
    Answer detail endpoint.
    """
    serializer_class = AnswerSerializer
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )
    lookup_field = 'public_id'

answer_detail = AnswerDetail.as_view()


#
# Login
#
class LoginView(GenericAPIView):
    """
    Login view. Performs a login on a POST and provides the user's full
    name and the href to the user's endpoint. Credentials are required to
    login.
    """
    serializer_class = LoginSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        result = {}
        result['fullname'] = user.get_full_name_or_username()
        result['href'] = reverse(
            'user-detail', kwargs={'public_id': user.public_id},
            request=request)
        return Response(result)

login_view = LoginView.as_view()


#
# Logout
#
class LogoutView(APIView):
    """
    Logout view. Performs the logout on a POST. No POST data is required
    to logout.
    """
    permission_classes = (
        And(IsUserActive, IsAuthenticated,
            Or(IsAnyUser,
               IsAnyProjectUser)
            ),
        )

    def post(self, request, *args, **kwargs):
        logout(request)
        status = HTTP_200_OK
        result = {'detail': _("Logout was successful.")}
        return Response(result, status=status)

logout_view = LogoutView.as_view()
