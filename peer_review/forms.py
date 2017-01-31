# -*- coding: utf-8 -*-
from django import forms

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
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
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
