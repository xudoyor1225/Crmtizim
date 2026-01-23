from rest_framework import viewsets, permissions
from .serializers import UserSerializer, TransactionSerializer
from apps.users.models import User
from apps.finance.models import Transaction

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Har kim faqat o'zini yoki o'z filialini ko'rsin
        user = self.request.user
        if user.role == 'super_admin':
            return User.objects.all()
        return User.objects.filter(organization=user.organization)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Mobil ilovadan kelgan to'lovlar 'pending' bo'ladi
        serializer.save(
            created_by=self.request.user,
            organization=self.request.user.organization,
            status='pending',
            receipt_verified=False
        )
