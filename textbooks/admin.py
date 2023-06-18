from django.contrib import admin
from .models import Textbook, Lesson, Card, ProfileCard, LastingCard

admin.site.register(Textbook)
admin.site.register(Lesson)
admin.site.register(Card)
admin.site.register(ProfileCard)
admin.site.register(LastingCard)
