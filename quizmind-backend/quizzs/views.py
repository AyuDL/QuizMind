from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Quiz
from .serializers import QuizCreateSerializer
from apps.core.permissions import IsOwnerOrReadOnly
from django.db.models import Q      #Q is for set "OR" as "|" can do

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "user__username", "category__content", "difficulty"]
    ordering_fields = ["user", "difficulty", "category", "created_at"]
    ordering = ["-created_at"]

    def performe_create(self, serializer):      #Function to set the user when we create the quiz
        serializer.save(user=self.request.user)

    def get_queryset(self):                #To set all quiz which the user can see
        user = self.request.user            #Look for user
        return Quiz.objects.filter(Q(is_public=True) | Q(user=user))    #Filter quiz when is public or created by the user

    @action(detail=False, methods=['get'])
    def mine(self, request):                #To get all own user quizzes, private or public.
        quizzes = Quiz.objects.filter(user=request.user)

        total = quizzes.count()
        public = quizzes.filter(is_public=True).count()
        private = total - public

        serializer = self.get_serializer(quizzes, many=True)
        return Response({
            "count": {"total": total, "public": public, "private": private},
            "results": serializer.data,
        })