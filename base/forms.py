from django.forms import ModelForm, CharField
from .models import Room, Message, Topic
import re
from django.core.exceptions import ValidationError


def validate_name(value):
    if not re.match(r'^[A-Za-z0-9_\.]+$', value):
        raise ValidationError(
            'Name can only contain normal characters and _, .')


class RoomForm(ModelForm):
    topic = CharField(max_length=200)

    class Meta:
        model = Room
        fields = ['name', 'topic', 'description']

    def clean_topic(self):
        topic_name = self.cleaned_data['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        return topic

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_name(name)
        return name


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('body',)

