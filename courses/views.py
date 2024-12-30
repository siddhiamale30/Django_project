from rest_framework import viewsets
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('instructor').prefetch_related('modules__lessons')
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        cached_courses = cache.get('courses')
        if not cached_courses:
            response = super().list(request, *args, **kwargs)
            cache.set('courses', response.data, timeout=60*15)
            return response
        return Response(cached_courses)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)