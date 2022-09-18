from django.db import models
from core import models as core_models

# Create your models here.


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "№ of messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "№ of participants"


class Message(core_models.TimeStampedModel):

    creator = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    message = models.TextField()
    conversation = models.ForeignKey(
        "conversations.Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.creator} says: {self.message}"
