from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.db import transaction
from user.models import InviteCode, User


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].label = '密碼'
        self.fields['password2'].label = '確認密碼'

    email = forms.EmailField(required=True, label='信箱')
    invite_code = forms.CharField(required=True, label='邀請碼')

    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        invite_code_obj = InviteCode.objects.filter(code=invite_code).first()

        if invite_code_obj is None:
            raise forms.ValidationError('無效的邀請碼')

        if invite_code_obj.is_used:
            raise forms.ValidationError('邀請碼已被使用')

        return invite_code

    def save(self):
        with transaction.atomic():
            user: User = super(RegistrationForm, self).save(commit=False)

            invite_code = InviteCode.get_for_update(self.cleaned_data['invite_code'])
            invite_code.is_used = True
            invite_code.save()

            user.email = self.cleaned_data['email']
            user.invite_code = invite_code
            user.is_staff = True
            user.save()

            group = Group.objects.get(name='normal_user')
            user.groups.add(group)

        return user

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
