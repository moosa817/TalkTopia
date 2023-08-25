from django.forms import ModelForm, CharField
from .models import Room, Message, Topic
import re
from django.core.exceptions import ValidationError


class RoomForm(ModelForm):
    topic = CharField(max_length=200)

    class Meta:
        model = Room
        fields = ['name', 'topic', 'description']

    def clean_topic(self):
        topic_name = self.cleaned_data['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        return topic


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
