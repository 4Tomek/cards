from django.db import models
import uuid
from users.models import Profile


class Textbook(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'name']]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Card(models.Model):
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['textbook', 'question', 'answer']]

    def __str__(self):
        return self.question


class ProfileCard(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, null=True, blank=True)
    mastered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['profile', 'card']]

    def __str__(self):
        return str(self.card.question)


class LastingCard(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    correct_in_row = models.IntegerField(default=0)
    wrong_in_row_0 = models.IntegerField(default=0)
    wrong_in_row_1 = models.IntegerField(default=0)
    wrong_in_row_2 = models.IntegerField(default=0)
    wrong_ever_counter = models.IntegerField(default=0)
    scheduled = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['profile', 'card']]

    def __str__(self):
        return str(self.card.question)
