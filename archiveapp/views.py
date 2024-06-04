from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.contrib import messages
from .models import MediaFile
from .forms import MediaFileForm, MediaFileEditForm
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required(login_url='login_user')
def home(request):
    media = MediaFile.objects.filter(file_type='video').order_by('-uploaded_at')
    print(media)  # Debugging print statement
    return render(request, 'home.html', {'media': media})

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                # Attempt to create a new user
                User.objects.create_user(username=uname, email=email, password=pass1)
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login_user')
            except IntegrityError:
                # Handle IntegrityError (e.g., duplicate entry) gracefully
                return HttpResponse("An error occurred while creating the user. Please try again.")

    return render(request, 'register.html')

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
    else:
        # Render the login form for GET requests
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('login_user')

def play_video(request, video_id):
    video = get_object_or_404(MediaFile, pk=video_id)
    
    # Find the index of the current video in the list of related videos
    related_videos = MediaFile.objects.filter(file_type='video').exclude(pk=video_id).order_by('-uploaded_at').distinct()
    
    return render(request, 'video_player.html', {'video': video, 'related_videos': related_videos})


@login_required(login_url='login_user')
def upload(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('home') 
        else:
            messages.error(request, 'Error uploading file.')
    else:
        form = MediaFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required(login_url='login_user')
def edit_media(request, media_id):
    try:
        media_item = MediaFile.objects.get(pk=media_id)
        
        if request.method == 'POST':
            form = MediaFileForm(request.POST, request.FILES, instance=media_item)
            if form.is_valid():
                form.save()
                messages.success(request, 'Media file updated successfully!')
                return redirect('home')
        else:
            form = MediaFileForm(instance=media_item)
        
        return render(request, 'edit_media.html', {'form': form, 'media_item': media_item})
    
    except ObjectDoesNotExist:
        messages.error(request, 'Media file not found.')
        return redirect('upload')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('upload')

@login_required(login_url='login')
def delete_media(request, media_id):
    try:
        media_item = MediaFile.objects.get(pk=media_id)
        media_item.delete()
        messages.success(request, 'Media file deleted successfully!')
    except MediaFile.DoesNotExist:
        messages.error(request, 'Media file not found.')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')

    return redirect('home')

@login_required(login_url='login_user')
def search_media(request):
    query = request.GET.get('q')
    
    if query:
        if len(query) < 4:
            media = MediaFile.objects.none() 
        else:
            media = MediaFile.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('-uploaded_at')
    else:
        media = MediaFile.objects.all().order_by('-uploaded_at')
    
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        html = render_to_string('media_partial.html', {'media': media})
        return HttpResponse(html)
    
    return render(request, 'search_media.html', {'media': media, 'query': query})

def search_suggestions(request):
    query = request.GET.get('term', '')
    
    if query:
        suggestions = MediaFile.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).values_list('title', flat=True)[:10]  # 10 suggestions
        
        suggestions = list(suggestions)
    else:
        suggestions = []
    
    return JsonResponse(suggestions, safe=False)

def audio(request):
    media = MediaFile.objects.filter(file_type='audio').order_by('-uploaded_at')
    print(media)
    return render(request, 'audio.html', {'media': media})

def images(request):
    media = MediaFile.objects.filter(file_type='image').order_by('-uploaded_at')
    print(media)
    return render(request, 'images.html', {'media': media})

def documents(request):
    media = MediaFile.objects.filter(file_type='document').order_by('-uploaded_at')
    print(media)  
    return render(request, 'documents.html', {'media': media})