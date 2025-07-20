from django.shortcuts import render, redirect
from django.core.management import call_command
from .models import ModuleRegistry
from sample_module.models import Product

def home(request):
    modules = ModuleRegistry.objects.all()
    return render(request, 'dashboard.html', {'modules': modules})

def module_dashboard(request):
    modules = ModuleRegistry.objects.all()
    return render(request, 'dashboard.html', {'modules': modules})

def install_module(request, name):
    if name == 'sample_module':
        ModuleRegistry.objects.update_or_create(name=name, defaults={'is_installed': True})
    return redirect('home')

def uninstall_module(request, name):
    if name == 'sample_module':
        Product.objects.all().delete()
        ModuleRegistry.objects.filter(name=name).update(
            is_installed=False,
            version=1 
        )
    return redirect('home')

def upgrade_module(request, name):
    if name == 'sample_module':
        module, _ = ModuleRegistry.objects.get_or_create(name=name)
        module.version += 1 
        module.save()
    return redirect('home')

def downgrade_module(request, name):
    if name == 'sample_module':
        try:
            module = ModuleRegistry.objects.get(name=name)
            if module.version > 1:
                module.version = 1  
                module.save()
                Product.objects.update(description=None)
        except ModuleRegistry.DoesNotExist:
            pass
    return redirect('home')
