from django.contrib import admin
from .models import Textbook, Lesson, Card, ProfileCard

admin.site.register(Textbook)
admin.site.register(Lesson)
admin.site.register(Card)
admin.site.register(ProfileCard)
