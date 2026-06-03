from django.shortcuts import render,redirect
from .models import Order,OrderItem
from sales.models import Cashbox , Item
from products.models import Product,Movement,Category
from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, IntegerField,Value
from django.db import transaction
import json
from django.http import JsonResponse
from django.db.models import Q



def order_list(request):
    orders = Order.objects.all().order_by('-created_at')[:40]
    return render(request, 'orders/list.html', {
        'orders': orders
    })


def order_detail(request, uuid):

    order = get_object_or_404(Order, uuid= uuid)

    items = order.items.select_related('product')

    return render(request, 'orders/detail.html', {
        'order': order,
        'items': items
    })


def order_send(request, uuid):

    order = get_object_or_404(Order, uuid=uuid)
    order.status = 'send'
    order.save()
    orders = Order.objects.all().order_by('-created_at')[:40]
  
    return render(request, 'orders/list.html', {
        'orders': orders
    })

def order_delivry(request, uuid):

    current_profile_user = request.user.profile
    company_id = current_profile_user.company_id
    user_id = current_profile_user.id

    order = get_object_or_404(Order, uuid=uuid)

    if order.status == 'send' :
       
        quantity = 0
        amount = order.total
        order.status = 'delivry'
        order.save()

        Movement.objects.create(
                    type='vente',
                    quantity=quantity,
                    amount=amount,
                    product_id=10,
                    company_id=company_id,
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

    orders = Order.objects.all().order_by('-created_at')[:20]

    return render(request, 'orders/list.html', {
        'orders': orders
    })


def create_order(request):
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
            customer = data.get("customer")
            phone = data.get("phone")
            address = data.get("address")
            note = data.get("note")
            if not cart:
                return JsonResponse({"success": False, "error": "Panier vide"}, status=400)

            total_amount = 0

            with transaction.atomic():

                order = Order.objects.create(
                    customer=customer,
                    phone=phone,
                    address=address,
                    note = note,
                    total=0,
                    company_id=company_id,
                    created_by=request.user,
                    status='pending'
                )

                total_amount = 0

                for item in cart:

                    product_id = item.get('id')
                    quantity = int(item.get('qty', 0))

                    if quantity <= 0:
                        continue

                    product = get_object_or_404(Product, id=product_id)

                    if product.quantity < quantity:
                        return JsonResponse({
                            "error": "Stock insuffisant",
                            "message": f"Stock {product.name} insuffisant"
                        }, status=400)

                    price = product.cost_price
                    amount = price * quantity

                    total_amount += amount

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                        custom_text='ghshsdhg',
                        subtotal=amount
                    )

                    # diminution du stock
                    product.quantity -= quantity
                    product.save()

                # mise à jour du total final
                order.total = total_amount
                order.save()

            # ✅ Réponse JSON
            return JsonResponse({
                "success": True,
                "message": "Commande enregistrée",
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Données invalides"}, status=400)

    # ✅ GET → afficher la page POS
    products = Product.objects.all()
    return render(request, "orders/create.html", {
        'products': products,
        "amountCashbox": amountCashbox
    })


def order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", [])

        order = order.objects.create(total=0)
        total = 0

        for item in cart:
            product = Product.objects.get(id=item["id"])
            qty = item["qty"]
            price = item["price"]

            total += price * qty

            # 🔥 mise à jour stock
            product.quantity -= qty
            product.save()

        order.total = total
        order.save()

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
            'id', 'name', 'quantity', 'cost_price'
        ))
        return JsonResponse(data, safe=False)

    # catégories (tu peux aussi filtrer par user si besoin)
    categories = Category.objects.all()

    return render(request, "orders/pos.html", {
        "products": products[:30],  # limiter seulement côté affichage initial
        "categories": categories
    })
    
    

def invoice(request, order_id):
    order = get_object_or_404(order, id=order_id)

    # ⚠️ important : correspond à ton related_name
    items = order.items.all()  # ou order.item_set.all() selon ton modèle

    context = {
        "order": order,
        "items": items,
    }

    return render(request, "orders/invoice.html", context)