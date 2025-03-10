from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.backends import ModelBackend

class PhoneShopBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        # if not kwargs['is_shop']:
        #     return None
        try:
            user = user_model.objects.get(shop__phone=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None




class EmailAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

class PhoneUserBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # if not 'is_buyer' in kwargs:
        #     return None
        # else:
        #     print(kwargs['is_buyer'])
        user_model = get_user_model()
        try:
            user = user_model.objects.get(buyer__phone=username)
            # if not user.is_buyer:
            #     return None
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None