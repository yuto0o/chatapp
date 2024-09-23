from django import forms
from .models import CustomUser
#ここ追記
from .models import Message
from django.contrib.auth import get_user_model
#ここまで追記

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User

User=get_user_model()


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']



class ChangeEmailForm(forms.ModelForm):
    new_email = forms.EmailField(label='新しいメールアドレス', required=True)

    class Meta:
        model = User
        fields = ['new_email']



class ChangeUsernameForm(forms.ModelForm):
    new_username = forms.CharField(label='新しいユーザー名', max_length=150)

    class Meta:
        model = User
        fields = ['new_username']

    def clean_new_username(self):
        username = self.cleaned_data['new_username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username
    
class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields= ("username", "email", "image", "password1","password2")

class LoginForm(AuthenticationForm):
    pass


#ここから追記

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)