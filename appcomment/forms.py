from .models import Comment, Diary
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'diary_entry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diary_entry'].widget = forms.HiddenInput()

class DiaryForm(forms.ModelForm):
    class Meta: 
        model = Diary
        fields = ['title', 'body']
    