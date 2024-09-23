from django.shortcuts import redirect, render
from .forms import (
    SignupForm,
    LoginForm,
    MessageForm,
    ChangeEmailForm,
    ChangeUsernameForm,
    ChangeProfileImageForm,
    CustomPasswordChangeForm
)
from django.contrib.auth import login, logout,update_session_auth_hash
from .models import CustomUser
from .models import Message
from django.db.models import Q 
from operator import itemgetter

from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from django.contrib import messages



#戻るボタンできないかな
from urllib import parse
from django import template
from django.shortcuts import resolve_url


register = template.Library()

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ログイン維持
            # messages.success(request, 'パスワードが変更されました。')
            changed_type="パスワードが変更されました。"
            params={
                "changed_type":changed_type
            }
            return render(request, 'myapp/changed.html',params)
            # return redirect('/change_password')  
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'myapp/change_password.html', {'form': form})

@login_required
def change_image(request):
    if request.method == 'POST':
        form = ChangeProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.image = form.cleaned_data['image']
            user.save()
            # messages.success(request, 'アイコン画像が変更されました。')
            changed_type="アイコン画像が変更されました。"
            params={
                "changed_type":changed_type
            }
            return render(request, 'myapp/changed.html',params)
            # return redirect('/change_image')  
    else:
        form = ChangeProfileImageForm()

    return render(request, 'myapp/change_image.html', {'form': form})

@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()
            # messages.success(request, 'メールアドレスが変更されました。')
            changed_type="メールアドレスが変更されました。"
            params={
                "changed_type":changed_type
            }
            return render(request, 'myapp/changed.html',params)
            # return redirect('/change_email') 
    else:
        form = ChangeEmailForm()

    return render(request, 'myapp/change_email.html', {'form': form})


@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            request.user.username = new_username
            request.user.save()
            # messages.success(request, 'ユーザー名が変更されました。')
            changed_type="ユーザー名が変更されました。"
            params={
                "changed_type":changed_type
            }
            return render(request, 'myapp/changed.html',params)
            # return redirect('/change_username')  
    else:
        form = ChangeUsernameForm()

    return render(request, 'change_username.html', {'form': form})

def changed(request,params):
    return render(request, 'change_username.html', params)



@register.simple_tag
def get_return_link(request):
    friends_page = resolve_url('myapp:friends')  # 最新の日記一覧
    referer = request.environ.get('HTTP_REFERER')  # これが、前ページのURL

    # URL直接入力やお気に入りアクセスのときはリファラがないので、トップぺージに戻す
    if referer:

        # リファラがある場合、前回ページが自分のサイト内であれば、そこに戻す。
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer

    return friends_page
# ここまで戻るボタンチャレンジ

# class Logout(LogoutView):
#     # template_name = 'index.html'
#     print("logout")

def logout_view(request):
    logout(request)
    messages="ログアウトしました"
    param={
        "messages":messages
    }

    return render(request, 'myapp/index.html',param)

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    # form= SignupForm()
    # return render(request, "myapp/signup.html", {'form':form})
    if request.method == 'POST':
        print(1)
        print(request.POST)

        form = SignupForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # print(2)
            form.save()
            return render(request, 'myapp/index.html')

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'myapp/signup.html', param)






def login_view(request):
    if request.method == 'POST':
        form =LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect('/friends')
                # return render(request, 'myapp/friends.html')
                
    else:
        form = LoginForm()
    param = {
        'form': form,
    }
    
    return render(request, "myapp/login.html",param)

def friends(request):
    # print(1)
    users=CustomUser.objects.all()
    
    # print(users)
    # for user in users:
        # print(2)
        # print(user.username)
    login_user=request.user
    friends=CustomUser.objects.exclude(id=login_user.id)

    # messages=Message.objects.filter(sender=CustomUser.objects.get(id=userlist_id),recipient=request.user)
    message_list=[]
    no_message=[]
    got_message=[]
    for friend in friends:
        latest_message=Message.objects.filter(
            Q(
                sender=request.user,
                recipient=friend
            )|
            Q(
                sender=friend,
                recipient=request.user
            )
        ).order_by("created_at").last()
        if latest_message:
            got_message.append([friend, latest_message.content, latest_message.created_at])
        else:
            no_message.append([friend, None, None])

        #friends画面が時間順になるように
    got_message= sorted(got_message, key=itemgetter(2), reverse=True)
    message_list.extend(got_message)
    message_list.extend(no_message)
    
    params={
        "message_list":message_list       
    }

    return render(request, "myapp/friends.html",params)


    

def talk_room(request, userlist_id):
    # print(userlist_id)#int型


    users=CustomUser.objects.all()
    login_username=request.user
    userlist=[]
    for item in users:
        if not str(login_username)==item.username:
            userlist.append(item)
    


    if request.method == 'POST':
        
        print(request.POST)
        print(1)

        form = MessageForm(request.POST)
        message = form.save(commit=False)
        message.sender = request.user
        message.recipient =  CustomUser.objects.get(id=userlist_id)
        # print(3)
        message.save()

        

        
    
            

    else:
        form = MessageForm()

    messages=Message.objects.filter(
        Q(
            sender=request.user,
            recipient=CustomUser.objects.get(id=userlist_id)
        )|
        Q(
            sender=CustomUser.objects.get(id=userlist_id),recipient=request.user
        )
    ).order_by("created_at")
    # print(request.user)
    # print(CustomUser.objects.get(id=userlist_id))
    # print(messages)
    # print(users)
    # print(userlist_id)
    # print(Message.objects.get(sender=request.user))
    talking_username=CustomUser.objects.get(id=userlist_id)
    

    

    params={
        "data":users,
        "login_username":login_username,
        "userlist":userlist,
        "userlist_id":userlist_id,
        'form': form,
        'messages':messages,
        "talking_username":talking_username
        
        


    }
    

    # return render(request, 'myapp/signup.html', param)

    return render(request, "myapp/talk_room.html",params)

def setting(request):
    return render(request, "myapp/setting.html")
