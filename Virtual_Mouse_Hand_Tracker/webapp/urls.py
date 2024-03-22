from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("mouse_action/<int:id>", views.mouse_action, name="mouse_action"),
    path("mappings/<int:id>", views.mouse_action_gesture_mapping, name="mappings"),
    path("user_mappings/", views.user_mappings, name="user_mappings"),
    path("all_actions/", views.all_actions, name="all_actions"),
    path("gestures/", views.all_gestures, name="gestures"),
    path("hand_gesture/<int:id>", views.hand_gesture, name="hand_gesture"),
    path("api/login", views.check_for_user),
    path('download/', views.DownloadZipFileView.as_view(), name='download_zip_file'),
    path('delete/<int:id>', views.delete_mapping, name="delete_mapping"),
]
