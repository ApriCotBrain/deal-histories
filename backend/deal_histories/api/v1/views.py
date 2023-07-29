import pandas

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import FileSerializer
from core.enums import Limits
from gems.models import File, Gem, Deal
from users.models import User


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_instance = serializer.save()

        try:
            data_frame = pandas.read_csv(file_instance.file)
        except pandas.errors.EmptyDataError:
            return Response(
                {"error": "Empty file"}, status=status.HTTP_400_BAD_REQUEST
            )
        except pandas.errors.ParserError:
            return Response(
                {"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as error:
            return Response(
                {"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for index, row in data_frame.iterrows():
            user, user_created = User.objects.get_or_create(
                username=row["customer"],
            )
            gem, gem_created = Gem.objects.get_or_create(name=row["item"])

            deal = Deal.objects.create(
                total=row["total"], file_id=file_instance.id
            )
            deal.user.add(user)
            deal.item.add(gem)
            deal.save()

        return Response(status=status.HTTP_200_OK)


class TopSpendingCustomerView(APIView):
    def get(self, request, id):
        try:
            file = get_object_or_404(File, id=id)
        except File.DoesNotExist:
            return Response({"error": "File not found."}, status=404)

        top_clients = (
            Deal.objects.filter(file_id=file.id)
            .values("user__username")
            .annotate(spent_money=Sum("total"))
            .order_by("-spent_money")[:Limits.TOP_CUSTOMER_VALUE_LIMIT]
        )

        response_data = []

        for client in top_clients:
            gem_list = (
                Deal.objects.filter(user__username=client["user__username"])
                .values("item__name")
                .annotate(num_clients=Count("user"))
                .filter(num_clients__gte=Limits.MIN_GEMS_VALUE)
            )

            response_data.append(
                {
                    "username": client["user__username"],
                    "spent_money": client["spent_money"],
                    "gems": [gem["item__name"] for gem in gem_list],
                }
            )

        return Response({"response": response_data})
