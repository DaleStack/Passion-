from django import forms  
from .models import UserModel

# Registration form
class UserRegister(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
            'role': forms.Select(choices=UserModel.RoleChoices),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

# Login form (updated)
class UserLogin(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)