# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class CSVForm(forms.Form):
	title = forms.CharField(max_length=50)
	csvFile = forms.FileField(
		label = 'Choose file'
	)

class UserForm(forms.Form):
	userId = forms.CharField(
		label = "Username:",
		max_length = 30,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'userId',}),
	)

	password = forms.CharField(
		label = "Password:",
		max_length = 100,
		widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password',}),
	)

	status = forms.ChoiceField(
		label = "Status:",
		choices = (('', '',), ('S', 'Student',), ('A', 'Admin',)),
		widget = forms.Select(attrs={'class': 'form-control', 'id': 'status'}),
	)

	title = forms.ChoiceField(
		label = "Title:",
		choices = (('', '',), ('Mr', 'Mr',), ('Ms', 'Ms',), ('Miss', 'Miss',), ('Mrs', 'Mrs',), ('Dr', 'Dr',)),
		widget = forms.Select(attrs={'class': 'form-control', 'id': 'title'}),
	)

	initials = forms.CharField(
		label = "Initials:",
		max_length = 5,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'initials',}),
	)

	name = forms.CharField(
		label = "First Name:",
		max_length = 50,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'name',}),
	)

	surname = forms.CharField(
		label = "Surname:",
		max_length = 50,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'surname',}),
	)

	cell = forms.CharField(
		label = "Cell Number:",
		max_length = 10,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'cell',}),
	)

	email = forms.EmailField(
		label = "Email:",
		max_length = 100,
		widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'email',}),
	)