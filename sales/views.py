from django.shortcuts import render,redirect
from .models import Sale , Cashbox , Item
from  products.models import Product,Movement,Category
from django.shortcuts import render, get_object_or_404
from django.db import transaction
import json
from django.http import JsonResponse
from django.db.models import Q


def sale_create(request):
    current_profile_user = request.user.profile
    companyId = current_profile_user.company_id
    user_id = current_profile_user.id

    cashbox = get_object_or_404(
                Cashbox,
                responsable_id = user_id,
                statut='open'
            )
    amountCashbox = cashbox.montant_final

    if request.method == "POST":

        productId = request.POST.get('product')
     
        quantity = int(request.POST.get('quantity', 0))

        product = get_object_or_404(Product, id=productId)

        if product.quantity < quantity:
            return redirect("pos")

        productPrice = product.sale_price
        amount = productPrice * quantity

        with transaction.atomic():

            # 🔻 Mise à jour stock
            product.quantity -= quantity
            product.save()

            # 🧾 Vente
            Sale.objects.create(
                product=product,
                company_id=companyId,
                quantity=quantity,
                amount=amount
            )

            # 📦 Mouvement
            Movement.objects.create(
                type='vente',
                quantity=quantity,
                product_id=product.id,
                company_id=companyId,
                created_by=request.user
            )

            # 💰 Caisse
            cashbox = get_object_or_404(
                Cashbox,
                responsable_id = user_id,
                statut='open'
            )

            cashbox.montant_final += amount
            cashbox.save()

        return redirect("sale_list")

    products = Product.objects.all()
    return render(request, "sales/create.html", {
        'products': products,
        "amountCashbox" : amountCashbox
        })


def sale_list(request):

    sales = Sale.objects.filter()

    return render(request, "sales/list.html", {
        "sales": sales,
       
    })

def cashbox_create(request):
    if request.method == "POST":
        current_profile_user = request.user.profile
        companyId = current_profile_user.company_id
        name = request.POST.get('name')

        Cashbox.objects.create(
            name = name,
            montant_initial = 3000,
            montant_final = 7000,
            company_id=companyId,
            responsable_id = 2,
            statut = 'close',
            created_by = request.user
        )

        return redirect("cashbox_list")

    products = Product.objects.all()
    return render(request, "cashboxes/create.html", {'products': products})

    
def cashbox_list(request):

    cashboxes = Cashbox.objects.filter()

    return render(request, "cashboxes/list.html", {
        "sales": cashboxes,
    })

def create_sale(request):
    current_profile_user = request.user.profile
    company_id = current_profile_user.company_id
    user_id = current_profile_user.id

    cashbox = get_object_or_404(
        Cashbox,
        responsable_id=user_id,
        statut='open'
    )

    amountCashbox = cashbox.montant_final

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            if not cart:
                return JsonResponse({"success": False, "error": "Panier vide"}, status=400)

            total_amount = 0

            with transaction.atomic():

                # ✅ Création de la vente
                sale = Sale.objects.create(
                    company_id=company_id,
                    created_by=request.user,
                    amount=0,
                    invoice_number=f"FAC-{Sale.objects.count() + 1}"
                )

                # ✅ Parcours du panier
                for item in cart:
                    product_id = item.get('id')
                    quantity = int(item.get('qty', 0))

                    if quantity <= 0:
                        continue

                    product = get_object_or_404(Product, id=product_id)

                    # ❌ Vérification stock
                    if product.quantity < quantity:
                        return JsonResponse({
                            "error": "Stock insuffisant",
                            "message" : f"Stock {product.name} insuffisant ",
                            "code": "400"
                        }, status=400)

                    price = product.sale_price
                    amount = price * quantity
                    total_amount += amount

                    # ✅ Création du SaleItem
                    Item.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        price=price,
                        total=amount
                    )

                    # ✅ Mise à jour stock
                    product.quantity -= quantity
                    product.save()

                # ✅ Mise à jour total vente
                sale.amount = total_amount
                sale.save()

                # ✅ Mise à jour caisse
                cashbox.montant_final += total_amount
                cashbox.save()

            # ✅ Réponse JSON
            return JsonResponse({
                "success": True,
                "message": "Vente enregistrée",
                "invoice": sale.invoice_number,
                "total": total_amount,
                "sale_id": sale.id,
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Données invalides"}, status=400)

    # ✅ GET → afficher la page POS
    products = Product.objects.all()
    return render(request, "sales/create.html", {
        'products': products,
        "amountCashbox": amountCashbox
    })



def sale(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", [])

        sale = Sale.objects.create(total=0)
        total = 0

        for item in cart:
            product = Product.objects.get(id=item["id"])
            qty = item["qty"]
            price = item["price"]

            total += price * qty

            # 🔥 mise à jour stock
            product.quantity -= qty
            product.save()

        sale.total = total
        sale.save()

        return JsonResponse({"status": "ok"})



def pos(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')  # ✅ NEW
    user = request.user

    # Base queryset (toujours filtré par utilisateur)
    products = Product.objects.filter(created_by=user)

    # 🔍 filtre recherche
    if query:
        products = products.filter(name__icontains=query)

    # 📂 filtre catégorie
    if category:
        products = products.filter(category_id=category)

    # 🧠 optimisation (optionnel mais propre)
    products = products.order_by('-created_at')

    # ⚡ AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(products.values(
            'id', 'name', 'quantity', 'sale_price'
        ))
        return JsonResponse(data, safe=False)

    # catégories (tu peux aussi filtrer par user si besoin)
    categories = Category.objects.all()

    return render(request, "sales/pos.html", {
        "products": products[:30],  # limiter seulement côté affichage initial
        "categories": categories
    })
    
    

def po(request):
    query = request.GET.get('q', '')
    user = request.user  # utilisateur connecté

    # 🔍 recherche
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query),
            created_by=user   # ✅ filtre utilisateur
        ).distinct()
    else:
        products = Product.objects.filter(
            created_by=user   # ✅ filtre utilisateur
        ).order_by('-created_at')[:30]

    # ⚡ AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(products.values('uuid', 'name', 'quantity', 'sale_price'))
        return JsonResponse(data, safe=False)
    
    categories = Category.objects.all()

    # 🖥 affichage normal
    return render(request, "sales/pos.html", {"products": products,'categories': categories})



def invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    # ⚠️ important : correspond à ton related_name
    items = sale.items.all()  # ou sale.item_set.all() selon ton modèle

    context = {
        "sale": sale,
        "items": items,
    }

    return render(request, "sales/invoice.html", context)