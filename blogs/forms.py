from django.forms import fields, widgets
from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ['post']

        labels = {
            'user_name': "Your Name",
            'user_email': 'Your Email',
            'comment_text': 'Your Comment'
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'enter your name'}),
            'user_email': forms.EmailInput(attrs={'placeholder':'enter your email address'}),
            'comment_text':forms.Textarea(attrs={'placeholder':'your comments'})
        }
        # error_message={
        #     'required': 'This field is required',
        # }
