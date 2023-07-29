import pandas
from django.db.models import Count, F
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.v1.serializers import FileSerializer
from core.enums import Limits
from gems.models import Gem
from users.models import User


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data["file"]

        try:
            data_frame = pandas.read_csv(csv_file)
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
            if not user_created:
                user.spent_money = F("spent_money") + row["total"]
                user.save()

            gem, gem_created = Gem.objects.get_or_create(name=row["item"])
            user.gems.add(gem)

        return Response(status=status.HTTP_200_OK)


class TopSpendingCustomerView(APIView):
    def get(self, request):
        top_five_customers = User.objects.order_by("-spent_money")[
            : Limits.TOP_CUSTOMER_VALUE_LIMIT
        ]

        gems = (
            Gem.objects.filter(user__in=top_five_customers)
            .annotate(count=Count("user"))
            .filter(count__gte=Limits.MIN_GEMS_VALUE)
        )
        response_data = [
            {
                "username": customer.username,
                "spent_money": customer.spent_money,
                "gems": [
                    gem.name for gem in gems if customer in gem.user.all()
                ],
            }
            for customer in top_five_customers
        ]

        return Response({"response": response_data})
