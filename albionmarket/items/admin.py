# -*- coding: utf-8 -*-
"""Admin do app de itens - opcional para administração direta."""

from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Exibição administrativa de itens."""

    list_display = ["id", "display_name", "category", "subcategory", "tier", "active"]
    list_filter = ["category", "subcategory", "tier", "active"]
    search_fields = ["id", "display_name"]
    ordering = ["category", "display_name"]