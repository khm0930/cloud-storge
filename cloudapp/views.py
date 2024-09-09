

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document, Folder
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import HttpResponse ,FileResponse
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.kakao.provider import KakaoProvider
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from .forms import DocumentForm, FolderForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os



def home(request):
    return render(request, 'cloudapp/home.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return redirect(f'/cloudapp/login/?email={email}')
        else:
            return redirect(f'/cloudapp/signup/details/?email={email}')
    return render(request, 'cloudapp/signup.html')

def signup_details(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        # 사용자 생성 로직 추가
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Authentication failed. Please try again.')
            return redirect('signup')

    return render(request, 'cloudapp/signup_details.html', {'email': email})


def login_view(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'cloudapp/login_details.html', {'email': email})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('file_list')
    else:
        form = DocumentForm()
    return render(request, 'cloudapp/upload_file.html', {'form': form})

@login_required
def upload_folder(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            # 폴더 경로를 추출
            folder_path = os.path.dirname(file.name)
            parent_folder = None

            if folder_path:
                # 경로를 '/'로 분리하여 각 폴더를 생성
                folders = folder_path.split('/')
                for folder_name in folders:
                    folder, created = Folder.objects.get_or_create(name=folder_name, parent=parent_folder, user=request.user)
                    parent_folder = folder

            # 파일 저장
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Document 객체 저장
            document = Document(upload=file, user=request.user, folder=parent_folder)
            document.save()

        return redirect('file_list')

    form = DocumentForm()
    return render(request, 'cloudapp/upload_folder.html', {'form': form})

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            parent_folder_id = request.POST.get('parent_folder_id')
            if parent_folder_id:
                folder.parent_folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)
            folder.save()
            return redirect('file_list')
    else:
        form = FolderForm()
    return render(request, 'cloudapp/create_folder.html', {'form': form})

# @login_required
# def file_list(request):
#     documents = Document.objects.filter(folder__isnull=True, user=request.user)
#     folders = Folder.objects.filter(parent_folder__isnull=True, user=request.user)
#     return render(request, 'cloudapp/file_list.html', {'documents': documents, 'folders': folders})

# @login_required
# def folder_view(request, folder_id):
#     folder = get_object_or_404(Folder, id=folder_id, user=request.user)
#     documents = Document.objects.filter(folder=folder, user=request.user)
#     sub_folders = Folder.objects.filter(parent_folder=folder, user=request.user)
#     return render(request, 'cloudapp/file_list.html', {'documents': documents, 'folders': sub_folders, 'current_folder': folder})

@login_required
def file_list(request):
    current_folder = None
    if 'folder_id' in request.GET:
        current_folder = get_object_or_404(Folder, id=request.GET['folder_id'], user=request.user)

    folders = Folder.objects.filter(parent_folder=current_folder, user=request.user)
    documents = Document.objects.filter(folder=current_folder, user=request.user)

    return render(request, 'cloudapp/file_list.html', {
        'folders': folders,
        'documents': documents,
        'current_folder': current_folder,
    })

@login_required
def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = Folder.objects.filter(parent_folder=folder, user=request.user)
    documents = Document.objects.filter(folder=folder, user=request.user)
    return render(request, 'cloudapp/file_list.html', {
        'folders': subfolders,
        'documents': documents,
        'current_folder': folder
    })


@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == 'POST':
        folder.delete()
        return redirect('file_list')
    return render(request, 'cloudapp/delete_confirm.html', {'folder': folder})

@login_required
def move_document_to_folder(request, document_id):
    if request.method == 'POST':
        document = get_object_or_404(Document, id=document_id, user=request.user)
        folder_id = request.POST.get('folder')
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, user=request.user)
            document.folder = folder
            document.save()
        return redirect('file_list')

@csrf_exempt
@login_required
def move_document_to_folder_api(request, document_id, folder_id):
    try:
        document = get_object_or_404(Document, id=document_id, user=request.user)
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        document.folder = folder
        document.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def download_file(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    response = FileResponse(document.upload, as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{document.upload.name}"'
    return response

@login_required
def delete_file(request, id):
    document = get_object_or_404(Document, id=id, user=request.user)
    if request.method == 'POST':
        document.delete()
        return redirect('file_list')
    return render(request, 'cloudapp/delete_confirm.html', {'document': document})

def logout_view(request):
    logout(request)
    return redirect('home')