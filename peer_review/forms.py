# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm

from peer_review.models import User


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]


class LoginForm(forms.Form):
    userName = forms.Field()
    password = forms.CharField(widget=forms.PasswordInput)


class FSetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        print("**** FIRST HERE ****")
        print(user.name)
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        print("*****HERE*****")
        print(self.user.name)
        if commit:
            self.user.save()
        return self.user


class ResetForm(forms.Form):
    class Meta:
        model = User
        fields = ['userId']
    
    userId = forms.CharField(
        label="Username:",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'userId',}),
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userId','status','title','initials','name','surname','cell','email']

    userId = forms.CharField(
        label="Username:",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'userId',}),
    )

    status = forms.ChoiceField(
        label="Status:",
        choices=(('', '',), ('U', 'User',), ('A', 'Admin',)),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
    )

    title = forms.ChoiceField(
        label="Title:",
        choices=(('', '',), ('Mr', 'Mr',), ('Ms', 'Ms',), ('Miss', 'Miss',), ('Mrs', 'Mrs',), ('Dr', 'Dr',)),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'title'}),
    )

    initials = forms.CharField(
        label="Initials:",
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'initials',}),
    )

    name = forms.CharField(
        label="First Name:",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name',}),
    )

    surname = forms.CharField(
        label="Surname:",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'surname',}),
    )

    cell = forms.CharField(
        label="Cell Number:",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cell',}),
    )

    email = forms.EmailField(
        label="Email:",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email',}),
    )
