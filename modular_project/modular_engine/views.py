from django.shortcuts import render, redirect
from django.core.management import call_command
from .models import ModuleRegistry
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h2>Welcome! Go to <a href='/module/'>/module/</a></h2>")

def module_dashboard(request):
    modules = ModuleRegistry.objects.all()
    return render(request, 'modular_engine/dashboard.html', {'modules': modules})

def install_module(request, name):
    if name == 'sample_module':
        ModuleRegistry.objects.update_or_create(name=name, defaults={'is_installed': True})
    return redirect('home')

def uninstall_module(request, name):
    if name == 'sample_module':
        ModuleRegistry.objects.filter(name=name).update(
            is_installed=False,
            version=1  # 👈 reset version on uninstall
        )
    return redirect('home')

def upgrade_module(request, name):
    if name == 'sample_module':
        module, _ = ModuleRegistry.objects.get_or_create(name=name)
        module.version += 1  # simulate version bump
        module.save()
    return redirect('home')

def downgrade_module(request, name):
    if name == 'sample_module':
        try:
            module = ModuleRegistry.objects.get(name=name)
            if module.version > 1:
                module.version -= 1  # decrement version
                module.save()
        except ModuleRegistry.DoesNotExist:
            pass
    return redirect('home')
