from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
import datetime
from django.utils import timezone  # Import this for timezone utilities

@login_required
def chat_room(request, username):
    search_query = request.GET.get('search', '')
    users = User.objects.exclude(id=request.user.id)
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=username)) |
        (Q(receiver=request.user) & Q(sender__username=username))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))

    chats = chats.order_by('timestamp')
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
    # user_last_messages.sort(
    #     key=lambda x: timezone.make_aware(x['last_message'].timestamp) if x['last_message'] else timezone.make_aware(datetime.datetime.min),
    #     reverse=True
    # )


# Inside your view function, before saving a message
#     message = Message(sender=request.user, receiver=receiver_user, content=message_content)
#     message.timestamp = timezone.now()  # Manually set the timestamp, though it should auto-fill if you use auto_now_add
#     message.save()


    return render(request, 'chat.html', {
        'username': username,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
