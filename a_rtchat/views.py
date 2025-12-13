from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .forms import ChatmessageCreateForm


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")

    # get last 30 messages in correct order
    chat_messages = chat_group.chat_messages.order_by('-created')[:30]
    chat_messages = reversed(chat_messages)   # oldest → newest

    form = ChatmessageCreateForm()

    if request.htmx and request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():                          # FIXED — added ()
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            context = {
                'message': message,
                'user': request.user
            }

            # FIXED — return a rendered partial (not redirect)
            return render(
                request,
                'a_rtchat/partials/chat_message_p.html',
                context
            )

    return render(
        request,
        'a_rtchat/chat.html',
        {'chat_messages': chat_messages, 'form': form}
    )
