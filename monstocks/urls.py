
from django.contrib import admin
from django.urls import path, include
from connexion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('admin/', admin.site.urls),
    path('incription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('create_user/', views.create_user, name='create_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('products/', include('products.urls')),  # 👈 AJOUTER ÇA
    path('sales/', include('sales.urls')),  # 👈 AJOUTER ÇA
    path('orders/', include('orders.urls')),  # 👈 AJOUTER ÇA
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

