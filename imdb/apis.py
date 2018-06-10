from __future__ import absolute_import
from rest_framework.decorators import api_view
from imdb.models import User, ROLES
from imdb.handlers import (
    make_exc_response, make_success_response, UserAlreadyExists,
    AdminAccessException
)
from imdb.serializers import UserSerilizer
from rest_framework import status


@api_view(['POST'])
def createUser(request, *args, **kwargs):
    try:
        data = request.data
        assert len(data.get('admin_reference_no', '')) == 15, "IMDB104"
        assert len(data.get('username', '')) == 5, "IMDB103"
        assert data.get('role') in [
            role for role, role_key in ROLES], "IMDB106"
        users = User.objects.filter(username=data.get('username'))
        if users.exists():
            raise UserAlreadyExists("IMDB101")
        adminUser = User.objects.filter(
            reference_no=data.get('admin_reference_no'), role="admin")
        if not adminUser.exists():
            raise AdminAccessException("IMDB105")
        user = User.addNew(**{
            'username': data.get('username'), 'role': data.get('role')
        })
        return make_success_response(
            request, UserSerilizer(user).data, status=status.HTTP_200_OK
        )
    except AssertionError as e:
        return make_exc_response(
            request, str(e), status.HTTP_400_BAD_REQUEST)
    except UserAlreadyExists as e:
        return make_exc_response(
            request, str(e), status.HTTP_400_BAD_REQUEST)
    except AdminAccessException as e:
        return make_exc_response(
            request, str(e), status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return make_exc_response(
            request, "IMDB000", status.HTTP_500_INTERNAL_SERVER_ERROR, e
        )
