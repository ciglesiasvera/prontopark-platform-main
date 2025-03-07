from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permiso para acceder a esta página.')
                return redirect('home:index')  # Redirige a la página principal o a donde prefieras
        return _wrapped_view
    return decorator
