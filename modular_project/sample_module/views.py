from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .utils import group_required, is_description_enabled, module_guard, require_manager, require_user_or_manager
from modular_engine.models import ModuleRegistry

# Check access to module
def is_module_active():
    try:
        return ModuleRegistry.objects.get(name='sample_module').is_installed
    except ModuleRegistry.DoesNotExist:
        return False

def module_guard(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_module_active():
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

@module_guard
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'has_description': is_description_enabled()
    })


@module_guard
@require_user_or_manager
def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            barcode=request.POST['barcode'],
            price=request.POST['price'],
            stock=request.POST['stock'],
            description=request.POST.get('description', '')
        )
        return redirect('product_list')
    return render(request, 'product_form.html', {
        'has_description': is_description_enabled()
    })

@module_guard
@require_user_or_manager
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.barcode = request.POST['barcode']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.description = request.POST.get('description', '')
        product.save()
        return redirect('product_list')
    return render(request, 'product_form.html', {
        'product': product,
        'has_description': is_description_enabled()
    })

@module_guard
@require_manager
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('product_list')
