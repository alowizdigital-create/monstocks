from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm,ProfileForm,CompanyForm,CreateUserForm
from django.http import HttpResponseForbidden
# from core.models import Company
from .models import Profile ,Company
from sales.models import Cashbox
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction




def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():

                # ✅ Création entreprise
                company = Company.objects.create(
                    name=form.cleaned_data.get('username')  # ou champ dédié
                )

                # ✅ Création user
                user = form.save()

                # ✅ Profil
                Profile.objects.create(
                    user=user,
                    company=company,
                    phone='',
                    role = 'directeur',
                    address=''
                )

                # ✅ Caisse (ouverte directement)
                Cashbox.objects.create(
                name=f"Caisse {user.username}",
                montant_initial=0,
                montant_final=0,
                company_id=company.id,       # ✅
                responsable_id=user.id,      # ✅
                statut='open'
                )

            return redirect('connexion')

    else:
        form = CustomUserCreationForm()

    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    next_url = request.GET.get('next', None)  # récupère le paramètre 'next'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirige vers next si présent, sinon accueil
            if 'next' in request.POST and request.POST['next']:
                return redirect(request.POST['next'])
            elif next_url:
                return redirect(next_url)
            else:
                return redirect('order_list')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'connexion.html', {'next': next_url})

# @login_required
def acceuil(request):
    return render(request, 'acceuil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')


@login_required
def create_user(request):
    if request.user.profile.role == "directeur":
        return HttpResponseForbidden()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            company = request.user.profile.company

            # 🔥 point clé
            user.company = request.user.profile.company

            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(
                    user=user,
                    company=company,
                    phone='',
                    address=''
            )

            return redirect("user_list")
    else:
        form = CreateUserForm()

    return render(request, "createuser.html", {"form": form})



def user_list(request):

    users = User.objects.filter(
         profile__company=request.user.profile.company
    )
    return render(request, "userlist.html", {"users": users})