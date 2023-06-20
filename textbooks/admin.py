from django.contrib import admin
from .models import Textbook, Lesson, Card, ProfileCard, LastingCard, ProfileLesson

admin.site.register(Textbook)
admin.site.register(Lesson)
admin.site.register(Card)
admin.site.register(ProfileCard)
admin.site.register(LastingCard)
admin.site.register(ProfileLesson)
