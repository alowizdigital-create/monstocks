from sales.models import Cashbox
from products.models import Movement
from django.db.models import Sum

from django.shortcuts import render, get_object_or_404

from datetime import date

def mon_contexte(request):

    if not request.user.is_authenticated:
        return {}

    profile = getattr(request.user, "profile", None)
    if not profile:
        return {}

    company_id = profile.company_id
    user = request.user

    # Cashbox
    cashbox = Cashbox.objects.filter(
        responsable_id = user.id,
        statut='open'
    ).first()

    # Nombre de ventes (mouvements)
    ventes_count = Movement.objects.filter(
        company_id=company_id,
        created_by_id=user.id,  
        created_at__date=date.today(),  # important si DateTimeField
        type='vente'  # adapte selon ton modèle
    ).count()

    total_ventes = Movement.objects.filter(
        company_id=company_id,
        created_by_id=user.id,
        created_at__date=date.today(),
        type='vente'
    ).aggregate(total=Sum('amount'))['total'] or 0

    amountCashbox = cashbox.montant_final if cashbox else 0

    return {
        "amountCashbox": amountCashbox,
        "ventes_count": ventes_count,
        "total_ventes": total_ventes,
    }