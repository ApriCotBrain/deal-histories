import pandas
from django.db.models import Count
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
        except pandas.errors.ParserError:
            return Response(
                {"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST
            )

        existing_users = {user.username: user for user in User.objects.all()}
        existing_gems = {gem.name: gem for gem in Gem.objects.all()}

        users_to_create = []
        gems_to_create = []

        for index, row in data_frame.iterrows():
            username = row["customer"]

            if username not in existing_users:
                new_user = User(username=username)
                existing_users[username] = new_user
                users_to_create.append(new_user)
            else:
                existing_users[username].spent_money += row["total"]

            item_name = row["item"]

            if item_name not in existing_gems:
                new_gem = Gem(name=item_name)
                existing_gems[item_name] = new_gem
                gems_to_create.append(new_gem)

            existing_users[username].save()
            existing_gems[item_name].user.add(existing_users[username])

        User.objects.bulk_update(
            list(existing_users.values()), ["spent_money"]
        )
        User.objects.bulk_create(users_to_create)
        Gem.objects.bulk_create(gems_to_create)

        return Response(status=status.HTTP_200_OK)


class TopSpendingCustomerView(APIView):
    def get(self, request, format=None):
        top_five_customers = User.objects.all().order_by("-spent_money")[
            : Limits.TOP_CUSTOMER_VALUE_LIMIT
        ]
        gems_list = (
            Gem.objects.filter(user__in=top_five_customers)
            .values("name")
            .annotate(count=Count("name"))
            .filter(count__gte=Limits.MIN_GEMS_VALUE)
        )
        gems_list = [gem["name"] for gem in gems_list]

        response_data = [
            {
                "username": user.username,
                "spent_money": user.spent_money,
                "gems": gems_list,
            }
            for user in top_five_customers
        ]

        return Response({"response": response_data})
