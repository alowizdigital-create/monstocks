from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import ProductForm,CategoryForm,ArticleForm,UnitForm
from .models import Product,Category,Article,Unit,Movement
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


@login_required
def product_create(request):

    form = ProductForm()

    if request.method == "POST":
        # form = ProductForm(request.POST)

        # if form.is_valid():
        current_profile_user = request.user.profile
        companyId = current_profile_user.company_id
        

        # product = form.save(commit=False)
        # product.company_id = companyId
        # product.created_by = request.user

        name = request.POST['name']
        unit_id = request.POST.get('unit')
        categorie_id = request.POST.get('category')
        price = request.POST['sale_price']
        name = request.POST['name']
        quantity = request.POST['quantity']
        category  = Category.objects.get(id=categorie_id)
        unit  = Unit.objects.get(id=unit_id)
        img=request.FILES.get('image')
      
        Product.objects.create(
            name = name,
            quantity = quantity ,
            category = category,
            unit = unit,
            sale_price = price,
            cost_price = price,
            company_id = companyId,
            image= img,
            created_by = request.user
        )

        Movement.objects.create(
            type = 'entrée',
            quantity = quantity ,
            product_id = 5,
            company_id = companyId,
            created_by = request.user
        )
        return redirect("product_list")
    else:
        categories = Category.objects.all()
        units = Unit.objects.all()

    return render(request, "products/create.html", {
        "form": form,
        'categories': categories,
        'units': units
    })


@login_required
def product_list(request):
    query = request.GET.get('q', '')
    user = request.user

    # 👉 CAS RECHERCHE
    if query:
          products = Product.objects.filter(
            Q(name__icontains=query),
             created_by=user
        )
        
    # 👉 CAS PAGE INITIALE (juste 8 produits)
    else:
        products = Product.objects.filter(
            created_by=user   # ✅ filtre utilisateur
        ).order_by('-created_at')[:10]

    # 👉 AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(products.values('uuid', 'name', 'quantity', 'sale_price'))
        return JsonResponse(data, safe=False)

    return render(request, "products/list.html", {
        "products": products
    })



# GESTION DE
# CATEGORY 

@login_required
def category_create(request):

    form = CategoryForm()

    if request.method == "POST":
        current_profile_user = request.user.profile
        companyId = current_profile_user.company_id
        name =  request.POST['name']
        Category.objects.create(
                name = name,
                company_id = companyId
            )

        return redirect("category_list")

    return render(request, "categories/add.html", {
        "form": form
    })

@login_required
def category_list(request):

    user = request.user

    categories = Category.objects.filter(
        created_by = user
    ).order_by('-create_at')[:10]


    return render(request, "categories/list.html", {
        "categories": categories
    })


@login_required
def unit_create(request):
    form = UnitForm()

    if request.method == "POST":
        current_profile_user = request.user.profile
        companyId = current_profile_user.company_id
        symbol = request.POST['symbol']
        name = request.POST['name']

        Unit.objects.create(
                symbol = symbol,
                name=name,
                company_id = companyId
            )

        return redirect("unit_list")

    return render(request, "units/add.html", {
        "form": form
    })

@login_required
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()

    return redirect('category_list')


@login_required
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()

    return redirect('product_list')

@login_required
def unit_list(request):

    user = request.user

    units = Unit.objects.filter(
        created_by = user,
    )

    user = request.user 

    return render(request, "units/list.html", {
        "units": units
    })


@login_required
def unit_delete(request, id):
    unit = get_object_or_404(Unit, id=id)

    if request.method == "POST":
        unit.delete()

    return redirect('unit_list')

@login_required
def product_detail(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    return render(request, 'products/detail.html', {'product': product})
     

@login_required
def product_edit(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)  # on passe l'instance existante
        if form.is_valid():
            form.save()
            return redirect('product_list',)  # redirige vers la page détail
    else:
        form = ProductForm(instance=product)  # préremplit le formulaire avec les données actuelles
        categories = Category.objects.all()
        units = Unit.objects.all()
    return render(request, 'products/edit.html', {
        'form': form, 
        'product': product,
        'categories': categories,
        'units': units
        })



@login_required
def product_delete(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Le produit a été supprimé avec succès.")
        return redirect('product_list')

    return render(request, 'products/delete.html', {
        'product': product
    })



