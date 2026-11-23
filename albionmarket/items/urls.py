# -*- coding: utf-8 -*-
"""Rotas da aplicação items."""

from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("<str:item_id>/", views.item_detail, name="detail"),
]