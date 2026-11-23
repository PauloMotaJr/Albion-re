# -*- coding: utf-8 -*-
"""Views do catálogo de itens."""

import models
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import Http404
from .models import Item


def catalog(request):
    """Páginas o catálogo de itens com filtros e pesquisa.

    Args:
        request: O objeto de requisição Django.

    Returns:
        Renderização do template items/catalog.html com resultados filtrados.
    """

    # Coletar parâmetros de filtro da query string
    search = request.GET.get("search", "") or ""
    category_filter = request.GET.get("category", "") or None
    subcategory_filter = request.GET.get("subcategory", "") or None
    tier_filter = request.GET.get("tier") or None  # Pode ser "None" ou valor numérico
    enchantment_filter = request.GET.get("enchantment", "") or None

    # Construir consulta com filtros ORM eficientes
    queryset = Item.objects.all()

    if category_filter:
        queryset = queryset.filter(category=category_filter)

    if subcategory_filter:
        queryset = queryset.filter(subcategory=subcategory_filter)

    if tier_filter and tier_filter != "None":
        try:
            queryset = queryset.filter(tier=int(tier_filter))
        except ValueError:
            pass  # Ignora valores inválidos

    if enchantment_filter:
        queryset = queryset.filter(enchantment=enchantment_filter)

    if search:
        queryset = queryset.filter(
            models.Q(display_name__icontains=search) | models.Q(id__icontains=search)
        )

    # Paginação
    paginator = Paginator(queryset, 20)
    try:
        page_obj = paginator.get_page(request.GET.get("page", 1))
    except Exception:
        page_obj = paginator.get_page(1)

    return render(request, "items/catalog.html", {"page_obj": page_obj})


def item_detail(request, item_id):
    """Página de detalhes do item específico.

    Args:
        request: O objeto de requisição Django.
        item_id: Identificador oficial do item.

    Returns:
        Renderização do template items/detail.html ou HTTP 404 se não encontrado.
    """

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise Http404(f"Item {item_id} não encontrado.")

    return render(request, "items/detail.html", {"item": item})