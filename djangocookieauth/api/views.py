from django.shortcuts import render

import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View

# @method_decorator(csrf_exempt, name='dispatch')
# class LoginView(View):
#     def post(self, request, *args, **kwargs):
#         import json
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message": "Logged in successfully"}, status=200)
#         else:
#             return JsonResponse({"error": "Invalid username or password"}, status=400)


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    if username is None or password is None:
        return JsonResponse({"detail":"Please provide username and password."})
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return JsonResponse({"detail": "Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})

def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail":"Your are not logged in."}, status=400)
    logout(request)
    return JsonResponse({"detail":"Successfully logout."})

@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated": False})
    return JsonResponse({"is_authenticated": True})

def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"username":request.user.username})
    return JsonResponse({"username": request.user.username})
    