from django.shortcuts import redirect


def unauthenticated_teacher(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'te':
            return redirect('/teacher')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def unauthenticated_administrator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'ad':
            return redirect('/administrator/home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def authenticated_te(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'te':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/accounts/login')
    return wrapper_func

def authenticated_ad(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'ad':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/accounts/login')
    return wrapper_func


