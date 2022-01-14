from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from activity.models import Action
from users.models import UserExtraDetails


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.userextradetails.gender = gender
            user.save()
            messages.add_message(request, messages.SUCCESS, "Welcome " + username + "! You successfully registered!")
            request.session['username'] = username
            request.session['role'] = user.userextradetails.role
            request.session['isLoggedIn'] = 1
            return redirect('ps:homepage')
        except:
            messages.add_message(request, messages.ERROR,
                                 "Could not register user with the username: " + username + ". Please try again with a different username!")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, "users/register.html")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    actions = Action.objects.all().filter(user=user).order_by("-created")
    return render(request, "users/profile.html", {"user": user, "actions": actions})


def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    user = authenticate(username=username, password=pw)
    if user is not None:
        request.session['username'] = username
        request.session['role'] = user.userextradetails.role
        request.session['isLoggedIn'] = 1
        messages.add_message(request, messages.SUCCESS, "You have logged in successfully")
        return redirect('ps:homepage')
    else:
        messages.add_message(request, messages.ERROR, "Invalid username or password!")
        return redirect('ps:landing_page')


def logout_user(request):
    request.session.clear()
    return redirect('ps:landing_page')


def edit_profile(request, username):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1 and (
            request.session['username'] == username or request.session['role'] == 'admin'):
        user = get_object_or_404(User, username=username)
        if user is not None:
            return render(request, "users/edit-profile.html", {"user": user})
        else:
            messages.add_message(request, messages.ERROR, "The user you are trying to edit is invalid: " + username)
    else:
        messages.add_message(request, messages.ERROR,
                             "Unauthorised to edit " + username + "! Please login with appropriate credentials")
    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return redirect('ps:landing_page')


def save(request, username):
    if 'isLoggedIn' in request.session and request.session['isLoggedIn'] == 1 and (
            request.session['username'] == username or request.session['role'] == 'admin'):

        user = get_object_or_404(User, username=username)
        if 'email' in request.POST and request.POST.get('email') != '':
            user.email = request.POST.get('email')

        if 'password' in request.POST and request.POST.get('password') != '':
            user.password = request.POST.get('password')

        if 'fname' in request.POST and request.POST.get('fname') != '':
            user.first_name = request.POST.get('fname')

        if 'lname' in request.POST and request.POST.get('lname') != '':
            user.last_name = request.POST.get('lname')

        if 'gender' in request.POST and request.POST.get('gender') != '':
            user.userextradetails.gender = request.POST.get('gender')

        if request.session['role'] == 'admin' and 'role' in request.POST and request.POST.get('role') != '':
            user.userextradetails.role = request.POST.get('role')
            action = Action(
                user=get_object_or_404(User, username=request.session['username']),
                verb="changed role to " + request.POST.get('role') + "for user: ",
                target=user
            )
            action.save()

        user.save()
        messages.add_message(request, messages.SUCCESS,
                             "Profile for " + username + " updated successfully!")
    else:
        messages.add_message(request, messages.ERROR,
                             "Unable to update the profile for " + username + ". Please login with valid credentials")

    return redirect(request.META['HTTP_REFERER'])
