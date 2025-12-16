from __future__ import annotations

import logging
import os
import uuid
from typing import TYPE_CHECKING

import requests
from decouple import config
from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from core.mixin import FloatToIntRepresentationMixin
from services.product.models.product import Product
from services.product.rest.product.serializers import ProductSerializer
from services.transaction.models.topup import TopupTransaction

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TopupTransactionSerializer",)


class TopupTransactionSerializer(FloatToIntRepresentationMixin, BaseModelSerializer):
    float_to_int_fields = ("token", "total", "fee")

    product = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Product.objects.all(),
        required=False,
    )

    class Meta:
        model = TopupTransaction
        fields = [
            "pk",
            "reference",
            "token",
            "total",
            "qris",
            "expired_at",
            "fee",
            "status",
            "provider",
            "product",
            "created",
        ]
        read_only_fields = [
            "reference",
            "provider",
            "token",
            "total",
            "created",
            "qris",
            "expired_at",
            "fee",
        ]

    def get_fields(self):
        """Add pakasir_response only in detail route"""
        fields = super().get_fields()

        request = self.context.get("request")
        view = self.context.get("view")

        if request and view and getattr(view, "action", None) == "retrieve":
            # Only add this field in DETAIL mode
            fields["pakasir_response"] = serializers.SerializerMethodField()

        return fields

    def get_pakasir_response(self, obj):
        params = {
            "project": config("PAKASIR_SLUG"),
            "order_id": obj.reference,
            "amount": int(obj.product.price),
            "api_key": config("PAKASIR_API_KEY"),
        }

        print(params)

        url = "https://app.pakasir.com/api/transactiondetail"

        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            print(data)
        except Exception as e:
            return {"error": str(e)}

        return data.get("transaction")

    def generate_reference(self):
        return f"PS-{uuid.uuid4().hex[:8]}"

    def create(self, validated_data):
        """
        1. Create local topup record
        2. Build payload for Pakasir
        3. Send request to Pakasir QRIS API
        4. Return merged data
        """

        # 1. Buat transaksi lokal dulu
        validated_data["reference"] = self.generate_reference()
        validated_data["provider"] = "QRIS"
        validated_data["user"] = self.context["request"].user
        validated_data["token"] = validated_data["product"].token
        validated_data["total"] = validated_data["product"].price
        instance = super().create(validated_data)

        # 2. Siapkan payload
        payload = {
            "project": config("PAKASIR_SLUG"),
            "order_id": instance.reference,
            "amount": int(instance.product.price),
            "api_key": config("PAKASIR_API_KEY"),
        }

        # 3. Kirim request ke API Pakasir
        pakasir_url = "https://app.pakasir.com/api/transactioncreate/qris"
        headers = {"Content-Type": "application/json"}

        try:
            res = requests.post(pakasir_url, json=payload, headers=headers, timeout=10)
            pakasir_response = res.json()
        except Exception as e:
            pakasir_response = {
                "error": "Failed to connect to Pakasir",
                "details": str(e),
            }

        # 4. Inject response agar ikut masuk response DRF
        instance.__dict__["pakasir_response"] = pakasir_response["payment"]

        # update the total by response
        instance.total = int(pakasir_response["payment"]["total_payment"])
        instance.qris = pakasir_response["payment"]["payment_number"]
        instance.expired_at = pakasir_response["payment"]["expired_at"]
        instance.fee = pakasir_response["payment"]["fee"]
        instance.save()

        return instance

    # ------------------------------------------------------------------
    # 🔥 UPDATE (PUT/PATCH) — cancel request to Pakasir
    # ------------------------------------------------------------------
    def update(self, instance, validated_data):
        print("patching / putting")
        print(validated_data)
        new_status = validated_data.get("status", instance.status)
        print(new_status)
        old_status = instance.status

        # Only attempt cancel if new_status = cancelled & not previously cancelled
        if new_status == TopupTransaction.Status.CANCELLED and old_status != new_status:
            payload = {
                "project": config("PAKASIR_SLUG"),
                "order_id": instance.reference,
                "amount": int(instance.product.price),
                "api_key": config("PAKASIR_API_KEY"),
            }

            headers = {"Content-Type": "application/json"}
            cancel_url = "https://app.pakasir.com/api/transactioncancel"

            try:
                res = requests.post(
                    cancel_url, json=payload, headers=headers, timeout=10
                )
                cancel_response = res.json()
            except Exception as e:
                cancel_response = {
                    "error": "Failed to cancel Pakasir transaction",
                    "details": str(e),
                }

            print(cancel_response)

            # Inject so DRF returns it
            instance.__dict__["pakasir_cancel_response"] = cancel_response

        # Continue normal update
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Tambahkan pakasir_response ke output API"""
        rep = super().to_representation(instance)
        rep["pakasir_response"] = getattr(instance, "pakasir_response", None)
        return rep
