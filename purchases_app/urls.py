from django.urls import path
from purchases_app.views import *

urlpatterns = [
    path('',login_view,name="login_view"),
    path('register/',register_view,name="register_view"),
    path('dashboard/',dashboard_view,name="dashboard_view"),
    path('updateprofile/',update_profile_view,name="update_profile_view"),
    path('profile/',profile_view,name="profile_view"),
    path('logout/',logout_view,name="logout_view"),
    path('supplier_list/',supplier_list_view,name='supplier_list_view'),
    path('supplier_add/',supplier_add_view,name='supplier_add_view'),
    path('supplier_edit/<int:id>/',supplier_edit_view,name='supplier_edit_view'),
    path('supplier_delete_view/<int:id>/',supplier_delete_view,name='supplier_delete_view'),
    path('purchase_list/',purchase_list_view,name='purchase_list_view'),
    path('purchase_add/',purchase_add_view,name='purchase_add_view'),
    path('purchase_edit/<int:id>/',purchase_edit_view,name='purchase_edit_view'),
    path('purchase_delete_view/<int:id>/',purchase_delete_view,name='purchase_delete_view'),
]