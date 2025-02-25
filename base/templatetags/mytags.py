from django import template
from ..models import Room, Topic, Message, UserProfile
from django.db.models import Count
from django.contrib.auth.models import User


register = template.Library()


@register.simple_tag
def get_info():
    topics = Topic.objects.all()
    top_topics = Topic.objects.annotate(room_count=Count("room")).order_by(
        "-room_count"
    )[:7]
    top_topics_name = [topic.name for topic in top_topics]

    room_messages = Message.objects.filter().order_by("-updated")[:10]

    room_count = Room.objects.all().count()

    return {
        "topics": topics,
        "top_topics": top_topics,
        "top_topics_name": top_topics_name,
        "room_messages": room_messages,
        "room_count": room_count,
    }


@register.simple_tag
def pfp_info(username):
    try:
        username = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(username=username)
        return user_profile
    except:
        return {
            "pfp": {
                "url": "https://dvbewjfodfte3.cloudfront.net/static/base/img/guest.webp"
            }
        }


def pfp_url(username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(username=user)
        return user_profile.pfp.url
    except:
        return "https://dvbewjfodfte3.cloudfront.net/static/base/img/guest.webp"
