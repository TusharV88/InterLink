from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(followers=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)


    feed_list = list(chain(*feed))

    profile_images = []

    for post in feed_list:
        user_object = User.objects.get(username=post.user)
        profile = Profile.objects.get(user=user_object)
        profile_images.append(profile.profileImg)


    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'profile_images': profile_images, 'suggestions': suggestions_username_profile_list})



@login_required(login_url='signin')
def profile_page(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    total_post = len(user_posts)
    
    follower = request.user.username
    user = pk


    if FollowersCount.objects.filter(followers=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(followers=pk))
    
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'total_post': total_post,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }


    return render(request, 'profile.html', context)






@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        print('Image: ', image)
        print('Caption: ', caption)

        if image is not None:
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')



@login_required(login_url='signin')
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if post:
        post.delete()
        return redirect(f'/profile/{post.user}/')
    else:
        return redirect('/')
    



@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')


    post = Post.objects.get(id=post_id)    

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.no_of_likes += 1
        post.save()
    else:
        like_filter.delete()

        post.no_of_likes -=1 
        post.save()

    return redirect('/')





@login_required(login_url='signin')
def acc_settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileImg


        if request.FILES.get('image') != None:
            image = request.FILES.get('image')


        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileImg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        user_profile.user.first_name = first_name
        user_profile.user.last_name = last_name
        user_profile.user.save()


        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})




@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    
    
        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list, 'username': username})
        
    else:    
        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})





@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']


        if FollowersCount.objects.filter(followers=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(followers=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+ user) 
        else:
            new_follower = FollowersCount.objects.create(followers=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+ user)
    else:
        return redirect('/')



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirmpassword']

        if len(pass1) < 8:
            messages.info(
                request, 'Oops! The password you entered is too short. Please enter a password with at least 8 characters.')
            return redirect('signup')
        elif username == '' or len(username) < 5:
            messages.info(
                request, 'Oops! The username you entered is too short. Please enter a username with at least 5 characters.')
            return redirect('signup')
        elif email == '':
            messages.info(
                request, 'Please, enter an email address!!')
            return redirect('signup')



        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(
                    request, 'Sorry, the email you entered is already registered. Please choose a different email or try logging in.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Sorry, the username you entered is already taken. Please choose a different username.')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=pass1)
                user.save()

                # log in user and redirect to settings page
                user_login = auth.authenticate(
                    username=username, password=pass1)
                auth.login(request, user_login)

                # Create a new user profile
                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                user_profile.save()
                return redirect('settings')

        else:
            messages.info(
                request, 'Oops! The passwords you entered do not match. Please try again.')
            return redirect('signup')
    else:
        return render(request, 'signup.html')




def signin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        user = auth.authenticate(username=username, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(
                request, 'Oops! The username or password you entered is incorrect. Please try again.')
            return redirect('signin')

    return render(request, 'signin.html')





@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
