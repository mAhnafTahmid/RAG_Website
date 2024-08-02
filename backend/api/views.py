from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, QASerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import QA
from .generateAnswer import setup_vectorstore_and_search
from rest_framework.exceptions import ValidationError


class QAListCreate(generics.ListCreateAPIView):
    serializer_class = QASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QA.objects.filter(user=user)

    # def perform_create(self, serializer):
    #     message = self.request.data.get("message")
    #     res = setup_vectorstore_and_search(query=message)
    #     ai = res["result"]
    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user, message=message, ai=ai)
    #     else:
    #         print(serializer.errors)

    def perform_create(self, serializer):
        message = self.request.data.get("message")

        if not message:
            raise ValidationError("Message field is required.")

        # Generate 'ai' dynamically
        res = setup_vectorstore_and_search(query=message)
        ai = res.get("result")

        if ai is None:
            raise ValidationError("AI response could not be generated.")

        # Pass 'ai' directly to serializer's save method
        serializer.save(user=self.request.user, message=message, ai=ai)


class QADelete(generics.DestroyAPIView):
    serializer_class = QASerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return QA.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()  # Checks all users in db
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allows anyone to access this class
