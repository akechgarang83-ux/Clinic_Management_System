from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm
from .models import UserProfile


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone']
            )

            return redirect('login')

    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/register.html',
        context
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('login')


def role_required(allowed_roles):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            if not hasattr(request.user, 'profile'):
                return redirect('login')

            if request.user.profile.role not in allowed_roles:
                return render(
                    request,
                    'accounts/access_denied.html'
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


@role_required(['Administrator'])
def admin_test(request):

    return render(
        request,
        'accounts/admin_test.html'
    )