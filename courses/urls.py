from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]