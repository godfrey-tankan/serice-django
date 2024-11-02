from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import Http404
from .content_processor import custom_context
from django.db.models import Q
from a_users.models import Profile
import json

# Create your views here.
@login_required
def chat_view(request,chatroom_name='public-chat'):
    request_user_roles = get_object_or_404(Profile, user=request.user).user_type.split(',')[0]
            
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:20]
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group 
            message.author = request.user
            message.save()
            context = {'message':message, 'user':request.user}
            return render(request, 'a_rtchat/partials/chat_message_p.html',context)
    try:
        request_user_profile = Profile.objects.get(user=request.user)
        request_user_roles = request_user_profile.user_type.split(',')
        q_objects = [Q(user_type__icontains=user_type.strip()) for user_type in request_user_roles]
        combined_q = q_objects[0]
        for q in q_objects[1:]:
            combined_q |= q
        all_users = Profile.objects.filter(combined_q).exclude(user=request.user)
    except:
        all_users = None
    context = {'chat_messages':chat_messages, 'form':form, 'chatroom_name':chatroom_name, 'other_user':other_user, 'all_users':all_users}
    return render(request, 'a_rtchat/chat.html', context)



def get_object_or_create_chatroom(request, user_name):
    if request.user.username == user_name:
        return redirect('profiles')
    other_user = get_object_or_404(User, username=user_name)
    chatroom = ChatGroup.objects.filter(
        is_private=True,
        members=request.user
    ).filter(
        members=other_user
    ).first()
    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)

    return redirect('chatroom', chatroom_name=chatroom.group_name)
