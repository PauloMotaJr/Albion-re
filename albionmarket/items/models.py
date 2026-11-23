# -*- coding: utf-8 -*-
"""Modelos de catálogo de itens do Albion Online."""

from django.db import models


class Item(models.Model):
    """Representação de um item do Albion Online.

    Attributes:
        id: Identificador oficial único (chave primária, string para compatibilidade com IDs oficiais).
        display_name: Nome de exibição do item (ex: "Gold").
        category: Categoria principal do item (ex: "Currency", "Ores and Ores", "Vegetables etc.").
        subcategory: Subcategoria do item (ex: "Common Ore" para "Iron Ore").
        tier: Tier do item (1-4) - opcional, nem todos os itens têm tier.
        enchantment: Encantamento do item (opcional, null quando não aplicável).
        active: Indicador de item atualmente ativo no jogo.
        created_at: Timestamp de criação do registro.
        updated_at: Timestamp da última atualização dos dados.

    Identificador oficial é a chave de integração - nunca inventar valores.
    """

    id = models.CharField(
        max_length=256,
        primary_key=True,
        db_column="id",
        help_text="Identificador oficial único do item (ex: '348', '1009').",
    )

    display_name = models.CharField(
        max_length=512,
        blank=True,
        default="",
        help_text="Nome de exibição completo do item.",
    )

    category = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        db_index=True,
        help_text="Categoria principal (ex: 'Currency', 'Ores and Ores').",
    )

    subcategory = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Subcategoria do item.",
    )

    tier = models.IntegerField(
        null=True,
        blank=True,
        help_text="Tier do item (1-4). Nenhum valor significa sem tier definido.",
    )

    enchantment = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Encantamento aplicado ao item (opcional).",
    )

    active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Se o item está ativo atualmente no jogo.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="Data e hora em que o registro foi criado.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text="Data e hora da última atualização do registro.",
    )

    class Meta:
        ordering = ["category", "subcategory", "display_name"]
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["category"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.display_name} ({self.id})"