from __future__ import unicode_literals
from django.db import models
from django.core.validators import EmailValidator
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['fname']) < 2:
			errors["fname"] = "First name should be at least 2 characters"
		elif str.isalpha(postData["fname"]) == False:
			errors["fname"] = "Invalid first name, letters only"

		if len(postData['lname']) < 2:
			errors["lname"] = "Last name should be at least 2 characters"
		elif str.isalpha(postData["lname"]) == False:
			errors["lname"] = "Invalid last name, letters only"

		if len(postData['email']) < 2:
			errors["email"] = " Email should be at least 2 characters"
		elif not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Not a valid email"

		if len(postData['pass']) < 4:
		  	errors['password'] = "Password is not long enough."

		if postData['confirm'] != postData['pass']:
			errors['confirm'] = "Passwords do not match."
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects = UserManager()