#import form as form
from django.forms import forms

from Pharmacy.models import UserInfo


class Update_User_Info(forms.BaseForm):
    class Meta:
        model=UserInfo
        fields={'address','city','phone','state','zipcode'}

