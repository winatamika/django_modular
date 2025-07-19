from django.contrib.auth.decorators import user_passes_test
from modular_engine.models import ModuleRegistry
from django.shortcuts import redirect
from django.contrib import messages

# ---------------------------------------------
# ✅ Role-based group access decorator
# ---------------------------------------------
def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                messages.warning(request, "You must be logged in to access this page.")
                return redirect('product_list')  # or any safe fallback
            if not user.groups.filter(name=group_name).exists():
                messages.error(request, f"You need '{group_name}' access.")
                return redirect('product_list')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# ---------------------------------------------
# ✅ Check if sample_module is installed
# ---------------------------------------------
def is_module_active():
    try:
        module = ModuleRegistry.objects.get(name='sample_module')
        return module.is_installed
    except ModuleRegistry.DoesNotExist:
        return False

# ---------------------------------------------
# ✅ Decorator to block access if module uninstalled
# ---------------------------------------------
def module_guard(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_module_active():
            return redirect('home')  # or show 404/template if preferred
        return view_func(request, *args, **kwargs)
    return wrapper


def is_description_enabled():
    try:
        module = ModuleRegistry.objects.get(name='sample_module')
        return module.version >= 2
    except ModuleRegistry.DoesNotExist:
        return False