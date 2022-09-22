from django.db.models import Q  # COMPLEX QUERIES
from django.shortcuts import render, redirect, reverse
from django.http import Http404
from users import models as users_models
from django.views.generic import View
from users import mixins as user_mixins
from conversations import models as conversations_models
from . import forms

# Create your views here.


def GoConversationView(request, host_pk, guest_pk):
    user_one = users_models.User.objects.get_or_none(pk=host_pk)
    user_two = users_models.User.objects.get_or_none(pk=guest_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = conversations_models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except conversations_models.Conversation.DoesNotExist:
            conversation = conversations_models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
            conversation.save()
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(user_mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        conversation = conversations_models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddMessageForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        conversation = conversations_models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        message = self.request.POST.get("message")
        if message is not None:
            conversations_models.Message.objects.create(
                message=message,
                creator=self.request.user,
                conversation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))