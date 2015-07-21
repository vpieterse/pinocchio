# -*- coding: utf-8 -*-
from django import forms
from .models import Student, StudentDetail

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('username','password', 'status')

	username = forms.CharField(
		label = "Username:",
		max_length = 30,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}),
	)

	password = forms.CharField(
		label = "Password:",
		max_length = 100,
		widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}),
	)

	status = forms.ChoiceField(
		label = "Status:",
		choices = (('', '',), ('S', 'Student',), ('A', 'Admin',)),
		widget = forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
	)

class StudentDetailForm(forms.ModelForm):
	class Meta:
		model = StudentDetail
		fields = ('student','title','initials','name','surname','cell','email')
		
	title = forms.ChoiceField(
		label = "Title:",
		choices = (('', '',), ('Mr', 'Mr',), ('Ms', 'Ms',), ('Miss', 'Miss',), ('Mrs', 'Mrs',), ('Dr', 'Dr',)),
		widget = forms.Select(attrs={'class': 'form-control', 'id': 'title'}),
	)

	initials = forms.CharField(
		label = "Initials:",
		max_length = 5,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'initials'}),
	)

	name = forms.CharField(
		label = "First Name:",
		max_length = 50,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'firstName'}),
	)

	surname = forms.CharField(
		label = "Surname:",
		max_length = 50,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'surname'}),
	)

	status = forms.ChoiceField(
		label = "Status:",
		choices = (('', '',), ('S', 'Student',), ('A', 'Admin',)),
		widget = forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
	)

	cell = forms.CharField(
		label = "Cell Number:",
		max_length = 10,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'cell'}),
	)

	email = forms.EmailField(
		label = "Email:",
		max_length = 100,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
	)