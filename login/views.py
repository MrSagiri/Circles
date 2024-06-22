# AUTHENTICATION FOR BACKENDS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseServerError, JsonResponse

# OTHER STUFF FOR FRONTEND 
from django.shortcuts import render, redirect, get_object_or_404
from .forms import newAccForm, LoginForm, CreateForm, PostsForm
from .models import Posts, newAcc
from django.contrib import messages

# ========================================================================================
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user is not None:
                    login(request, user)
                    return redirect('/login/success')  # Replace 'home' with your desired redirect URL
        form = LoginForm()
        return render(request, 'index.html', {'form': form})

def register(request):
    if request.method == "POST":
        accountform = newAccForm(request.POST, request.FILES)
        createform = CreateForm(request.POST)
        if accountform.is_valid() and createform.is_valid():
            account = accountform.save(commit=False)
            account.firstname = createform.cleaned_data.get('first_name')
            account.lastname = createform.cleaned_data.get('last_name')
            account.username = createform.cleaned_data.get('username')
            account.save()
            createform.save()
            user = authenticate(username=createform.cleaned_data.get('username'), password=createform.cleaned_data.get('password1'))
            login(request, user)
            return redirect ('/register/success')
        else:
            # Passing form errors to the template
            return render(request, 'createaccount.html', {'accountform': accountform, 'createform': createform, 'form_errors': form.errors})
        
    accountform = newAccForm()
    createform = CreateForm()
    return render(request, 'createaccount.html', {'accountform': accountform, 'createform': createform})

@login_required
def register_success(request):
    user = request.user
    if user is not None:
        user = request.user.username
        return render(request,'register_success.html', {'user': user})
    return render(request,'index.html')

@login_required
def login_success(request):
    user = request.user
    if user is not None:
        user = request.user.username
        return render(request,'Login_success.html', {'user': user})
    return render(request,'index.html')


@login_required
def like_unlike_post(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Posts, id=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            action = 'unliked'
        else:
            post.likes.add(request.user)
            action = 'liked'

        return JsonResponse({
            'action': action,
            'likes_count': post.total_likes()
        })
        
@login_required
def home(request):
    user = request.user
    username = request.user.username  # Retrieve the authenticated user
    if username is not None:
        if request.method == 'POST':
            if 'Create_Post' in request.POST:
                UserData = get_object_or_404(newAcc, username=username)
                post = PostsForm(request.POST, prefix='createPost')
                if post.is_valid():
                    if post.is_valid():
                        UserData = get_object_or_404(newAcc, username=username)
                        print(UserData.image.url)
                        post = post.save(commit=False)
                        post.author = request.user.username
                        post.image = UserData.image.url
                        post.save()
                        return(redirect('/home'))
                
        getpost = Posts.objects.all().order_by("-created")
        createPost = PostsForm(prefix='createPost')
        user = get_object_or_404(User, username=username)
        # print(post)
        if username:
            # Retrieve user profile from database
            UserData = get_object_or_404(newAcc, username=username)
            
        context = {
            'user': user,
            'post': getpost,
            'Profile': UserData,
            'createPost': createPost
        }
        
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)


@login_required
def friendreq(request):
    return render(request, 'friendreq.html')


@login_required
def profile(request, username):
    username = request.user.username  # Retrieve the authenticated user
    getpost = Posts.objects.all().order_by("-created")
    post_count = getpost.count()
    user = get_object_or_404(User, username=username)
    UserData = get_object_or_404(newAcc, username=username)
    
    for post in getpost:
        print(post)
    context = {
        'user': user,
        'post': getpost,
        'Profile': UserData,
        'post_count': post_count,
    }
    return render(request, 'profile.html', context)


def Log_out(request):
    request.session.flush()
    logout(request)
    return redirect("/logout/success")

def Logout_success(request):
    return render(request,'Logout_success.html')