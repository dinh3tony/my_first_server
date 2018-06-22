from django.shortcuts import render, HttpResponse, redirect
from .models import User, UserManager
from time import strftime
from django.contrib import messages
from django.contrib.messages import get_messages
from djangounchained_flash import ErrorManager, ErrorMessage, getFromSession
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    if 'flash' not in request.session:
        request.session['flash'] = ErrorManager().addToSession()

    e = getFromSession(request.session['flash'])
    first_name_errors = e.getMessages('fname')
    last_name_errors = e.getMessages('lname')
    email_errors = e.getMessages('email')
    pass_errors = e.getMessages('password')
    conf_errors = e.getMessages('confirm')
    print(first_name_errors)
    print(conf_errors, "faweiojfaweiofawefoiawejfwoaie")
    request.session['flash'] = e.addToSession()
    context={
        'first_name_e':first_name_errors,
        'last_name_e':last_name_errors,
        'email_e':email_errors,
        'pass_e':pass_errors,
        'confirm_e':conf_errors
    }
    return render(request, 'login/login.html', context)

def create(request):
	print(request.method, "awoeifjaweofiawejfaweofwejaofiawefjweoa")
	if request.method == 'POST':
		errors = User.objects.basic_validator(request.POST)
		e = getFromSession(request.session['flash'])
		if len(errors):
			for tag, error in errors.items():
				e.addMessage(error,tag)
			request.session['flash'] = e.addToSession()
			return redirect('/login/')
		else: 
			request.session['fname'] = request.POST['fname']
			pw_hash = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())
			User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
			a = User.objects.last()
			request.session['name'] = a.first_name
			request.session['id'] = a.id
			print(pw_hash)

			return redirect('/login/show')

def login(request):
# 	# try: 
# 	# 	user = User.objects.get(email = request.POST['boob'])
# 	# except ObjectDoesNotExist:
# 	# 	return redirect('/login/')

	if len(User.objects.filter(email=request.POST['boob'])) < 1:
		messages.add_message(request, messages.INFO, "Invalid Email/Password", extra_tags="danger")
		return redirect('/login/')
	else:
		user = User.objects.get(email= request.POST['boob'])
	if bcrypt.checkpw(request.POST['chick'].encode(), user.password.encode()):
		request.session['id'] = user.id
		request.session['fname'] = user.first_name
		request.session['logged_in'] = True
		return redirect('/login/show')
	else:
		return redirect('/login/')

def show(request):
	return render(request, 'login/create.html')

def clear(request):
	request.session['logged_in'] = False
	request.session.clear()
	return redirect('/login/')







