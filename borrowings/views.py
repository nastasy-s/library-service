from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")
        user = self.request.user

        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        if user_id and user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response({"error": "Borrowing already returned"})

        borrowing.actual_return_date = borrowing.borrow_date
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response({"status": "Book returned successfully"})
