from django import forms
from .models import Student
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a password'
        })
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = Student
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your university ID'
            }),
        }
        labels = {
            'username': 'University ID'
        }
        help_texts = {
            'username': 'Your email will be automatically created using your university ID'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class LoginForm(forms.Form):  # Change from ModelForm to Form
    username = forms.CharField(
        label='University ID',
        max_length=9,
        validators=[MaxLengthValidator(9)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your university ID'
        }),
        error_messages={
            'max_length': 'University ID cannot exceed 9 characters.',
            'required': 'University ID is required.'
        }
    )
    password = forms.CharField(
        label='Password',
        validators=[MinLengthValidator(8), MaxLengthValidator(15)],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your password...'
        })
    )
