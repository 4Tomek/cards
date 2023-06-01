from django.forms import ModelForm
from .models import Textbook, Basic_card


class PackageForm(ModelForm):
    class Meta:
        model = Basic_card
        fields = ['textbook', 'question', 'answer']
