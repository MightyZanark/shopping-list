from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request: HttpRequest) -> JsonResponse:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is deactivated."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, invalid username or password."
        }, status=401)


@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)
