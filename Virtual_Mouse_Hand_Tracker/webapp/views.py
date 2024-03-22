from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import category_MouseAction_Mapping, mouseAction, category
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.views import View
from django.utils.encoding import smart_str
from django.http import HttpResponse

import os

# Create your views here.

def home(request) :
    mouse_actions = mouseAction.objects.all
    gestures = category.objects.all
    return render(request, "webapp/home.html", {
        "mouse_actions": mouse_actions,
        "gestures": gestures
    })

def register_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]

            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "webapp/register.html", {
                    "error_message": "The user name already exists."
                })

            login(request, user)
            return HttpResponseRedirect(reverse(home))
        else:
            return render(request, "webapp/register.html")
    else:
        return HttpResponseRedirect(reverse(home))

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse(home))
            else:
                return render(request, "webapp/login.html", {
                    "error_message": "Invalid username or password"
                })
        else:
            return render(request, "webapp/login.html")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse(home))

def mouse_action(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(home))
    else:
        mouse_action = mouseAction.objects.get(id=id)
        return render(request, "webapp/mouse_action.html", {
            "mouse_action": mouse_action
        })

def hand_gesture(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(home))
    else:
        gesture = category.objects.get(id=id)
        mapping = category_MouseAction_Mapping.get_mapping_using_gesture(gesture, request.user)
        user_selected_actions = []
        user_selected_actions = category_MouseAction_Mapping.get_all_actions(request.user)
        if mapping and user_selected_actions:
            user_selected_actions.remove(mapping.mouse_action.id)
        return render(request, "webapp/hand_gesture.html", {
            "gesture" : gesture,
            "mapping" : mapping,
            "user_selected_actions" : user_selected_actions
        })

def mouse_action_gesture_mapping(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(home))
    else:
        mouse_action = mouseAction.objects.get(id=id)
        mapping = category_MouseAction_Mapping.get_mapping(mouse_action, request.user)
        user_selected_gestures = []
        user_selected_gestures = category_MouseAction_Mapping.get_all_gestures(request.user)
        if mapping and user_selected_gestures:
            user_selected_gestures.remove(mapping.category.id)
        if request.method == "GET":
            return render(request, "webapp/mouse_action_gesture_mapping.html", {
                "mouse_action": mouse_action,
                "mapping": mapping,
                "user_selected_gestures": user_selected_gestures
            })

        if request.method == "POST":
            get_gesture_id = request.POST["gesture"]
            gesture = category.objects.get(id=get_gesture_id)
            category_MouseAction_Mapping.create_update_mapping(gesture, mouse_action, request.user)
            return HttpResponseRedirect(reverse(home))

def user_mappings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(home))
    else:
        mappings = category_MouseAction_Mapping.objects.filter(user=request.user)
        return render(request, "webapp/user_mappings.html", {
            "mappings": mappings
    })

def all_actions(request):
    if request.user.is_authenticated:
        actions = mouseAction.objects.all
        actions_mapped = category_MouseAction_Mapping.get_all_actions(request.user)
        return render(request, "webapp/all_actions.html", {
            "actions": actions,
            "actions_mapped": actions_mapped
        })
    else:
        return HttpResponseRedirect(reverse(login_user))

def all_gestures(request):
    if request.user.is_authenticated:
        gestures = category.objects.all
        gestures_mapped = category_MouseAction_Mapping.get_all_gestures(request.user)
        return render(request, "webapp/all_gestures.html", {
            "gestures" : gestures,
            "gestures_mapped" : gestures_mapped
        })
    else:
        return HttpResponseRedirect(reverse(login_user))

def delete_mapping(request, id):
    if request.user.is_authenticated:
        try:
            mapping = category_MouseAction_Mapping.objects.get(id=id)
            if mapping.user == request.user:
                mapping.delete()  # Correct method to delete an object

                # Redirect to user_mappings view after successful deletion
                return HttpResponseRedirect(reverse('user_mappings'))
            else:
                # Redirect to home if the mapping does not belong to the authenticated user
                return HttpResponseRedirect(reverse('home'))
        except category_MouseAction_Mapping.DoesNotExist:
            # Handle the case where the mapping with the given ID does not exist
            return HttpResponseRedirect(reverse('user_mappings'))
    else:
        # Redirect to home if the user is not authenticated
        return HttpResponseRedirect(reverse('home'))

def user_guide(request):
    return render(request, "webapp/guide.html")

# Django view code
@csrf_exempt
def check_for_user(request):
    if request.method == "GET":
        try:
            username = request.GET.get('username')
            password = request.GET.get('password')

            user = authenticate(username=username, password=password)
            res = {}
            if user is not None:
                mappings = category_MouseAction_Mapping.objects.filter(user=user.id)
                for mapping in mappings:
                    res[mapping.mouse_action.category_id] = mapping.category.category_id
                user_details = res
                return JsonResponse(user_details)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            print("Error: ", e)
            return JsonResponse({'error': str(e)}, status=500)


class DownloadZipFileView(View):
    def get(self, request):
        # Path to your pre-existing zip file
        zip_file_path = "/home/sanjeev/Desktop/mouse_action.zip"

        # Open the file in binary mode
        with open(zip_file_path, 'rb') as zip_file:
            # Create a response with the zip file
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(zip_file_path))
            return response

########################################################################################



