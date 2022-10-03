from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from decouple import config # type: ignore

from .models import Post, Report, User, Like, UserFollowing

from .forms import PostForm, SettingsAboutForm



# Create your views here.

def index(request):
    form = PostForm()
    posts = Post.objects.filter(hidden=False).order_by("-date_posted").all()[:10]
    if len(posts) == 0:
        posts = None
    context = {"form": form, "posts": posts}
    return render(request, 'socialapp/index.html', context)

def posts(request):
    start_offset = int(request.GET.get("o", 0))
    if start_offset < 0:
        start_offset = 0
    end_offset = start_offset + 10
    posts = Post.objects.filter(hidden=False).order_by("-date_posted").all()[start_offset:end_offset]
    if len(posts) == 0:
        posts = None
    context = {"posts": posts}
    return render(request, 'socialapp/posts.html', context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.hidden_by = request.user
            post.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))


@login_required
def logout(request):
    django_logout(request)
    domain = config("SOCIAL_AUTH_AUTH0_DOMAIN")
    client_id = config("SOCIAL_AUTH_AUTH0_KEY")
    return_to = 'https://social.ninjamar.dev/' # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

@login_required
def delete_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            post.delete()
    return redirect("/")

@permission_required("socialapp.view_report", raise_exception=True)
def reports(request):
    start_offset = int(request.GET.get("o", 0))
    if start_offset < 0:
        start_offset = 0
    end_offset = start_offset + 10

    reports = Post.objects.annotate(times_reported=Count('reports')).filter(times_reported__gt=0).all()[start_offset:end_offset]
    if len(reports) == 0:
        reports = None
    context = {"reports": reports}
    return render(request, 'socialapp/reports.html', context)

@login_required
def report_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        report, created = Report.objects.get_or_create(reported_by=request.user, post=post)
        if created:
            report.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))

@permission_required("socialapp.change_post", raise_exception=True)
def hide_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.hidden = True
        post.date_hidden = datetime.now()
        post.hidden_by = request.user
        post.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))

@permission_required("socialapp.change_post", raise_exception=True)
def unhide_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.hidden = False
        post.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))

@permission_required("socialapp.change_user", raise_exception=True)
def ban_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        for post in user.posts.all():
            post.hidden = True
            post.hidden_by = request.user
            post.date_hidden = datetime.now()
            post.save()
        user.is_active = False
        user.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))

@permission_required("socialapp.change_user", raise_exception=True)
def unban_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        for post in user.posts.all():
            post.hidden = False
            post.save()
        user.is_active = True
        user.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))

def inactive_user(request):
    if request.user.is_active:
        return redirect(request.META.get('HTTP_REFERER',"/"))
    return render(request, "socialapp/status/inactive.html")

@login_required
def like_post(request, post_id):
    if request.method == "POST":
        new_like, created = Like.objects.get_or_create(user=request.user, post=Post.objects.get(id=post_id))
    return redirect(request.META.get('HTTP_REFERER',"/")) 

@login_required
def unlike_post(request, post_id):
    if request.method == "POST":
        like = Like.objects.get(user=request.user, post=Post.objects.get(id=post_id))
        like.delete()
    return redirect(request.META.get('HTTP_REFERER',"/")) 

def profile(request, username):
    lo_start_offset = int(request.GET.get("lo", 0))
    co_start_offset = int(request.GET.get("co", 0))
    if lo_start_offset < 0:
        lo_start_offset = 0
    if co_start_offset < 0:
        co_start_offset = 0

    lo_end_offset = lo_start_offset + 10
    co_end_offset = co_start_offset + 10

    user = User.objects.get(username=username)
    followers = [i.who_follows for i in user.followers.all()]
    following = (i.to_follow for i in user.following.all())
    
    post_likes = [i.post for i in Like.objects.filter(user=user)]
    post_likes = post_likes[lo_start_offset:lo_end_offset]
    try:
        posts = user.posts.all()[co_start_offset:co_end_offset]
    except:
        posts = None
    if len(posts) == 0:
        posts = None
    if len(post_likes) == 0:
        post_likes = None
    context = {"profile": user, "followers": followers, "following": following, "post_likes": post_likes, "posts": posts}
    return render(request, "socialapp/profile.html", context)

@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        me = request.user
        them = User.objects.get(id=user_id)
        try:
            UserFollowing.objects.create(to_follow=them, who_follows=me)
        except:
            pass
    return redirect(request.META.get('HTTP_REFERER',"/"))

@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        me = request.user
        them = User.objects.get(id=user_id)
        try:
            UserFollowing.objects.get(to_follow=them, who_follows=me).delete()
        except:
            pass
    return redirect(request.META.get('HTTP_REFERER',"/")) 

def search(request):
    user = request.GET.get("user", None)
    to_search = request.GET.get("q", None)
    start_offset = request.GET.get("o", 0)

    if user is not None:
        if to_search is not None:
            try:
                result = Post.objects.filter(user=User.objects.get(username=user), text__contains=to_search, hidden=False)
            except:
                result = []
        else:
            try:
                result = Post.objects.filter(user=User.objects.get(username=user), hidden=False)
            except:
                result = []
    else:
        if not ((user == None) and (to_search == None)):
            try:
                result = Post.objects.filter(text__contains=to_search, hidden=False)
            except:
                result = []
        else:
            result = []

    start_offset = int(request.GET.get("o", 0))
    if start_offset < 0:
        start_offset = 0
    end_offset = start_offset + 10

    result = result[start_offset:end_offset]
    if len(result) == 0:
        result = None
    context = {"results": result, "noresults": True if (len(result) == 0) else False}
    return render(request, "socialapp/search.html", context)

@login_required
def set_about(request):
    if request.method == "POST":
        form = SettingsAboutForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER',"/"))
    
@login_required
def settings(request):
    about_form = SettingsAboutForm()
    context = {"about_form": about_form}
    return render(request, 'socialapp/settings.html', context)

def about(request):
    return render(request, 'socialapp/about.html')

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
    return redirect("/logout")

@login_required
def groupchat(request, roomid):
    context = {"roomid":roomid}
    return render(request, "socialapp/groupchat.html", context=context)

@login_required
def uuchat(request, u1, u2):
    context = {"u1": u1, "u2": u2}

    if request.user not in [User.objects.get(username=u1), User.objects.get(username=u2)]:
        raise PermissionDenied("stop snooping on other people's chat")
    
    return render(request, "socialapp/uuchat.html", context=context)
@login_required
def chatindex(request):
    return render(request, "socialapp/chatindex.html")