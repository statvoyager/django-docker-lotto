from django.urls import path
from . import views

app_name = "lotto"

urlpatterns = [
    path("", views.index, name="index"),
    path("buy/manual/", views.buy_manual, name="buy_manual"),
    path("buy/auto/", views.buy_auto, name="buy_auto"),
    path("admin/draw/", views.draw_lotto, name="draw_lotto"),
    path("check/", views.check_result, name="check_result"),
]