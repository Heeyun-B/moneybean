from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
            model = Post
            exclude = ('user',) # foreign key 빼고 

class CommentForm(forms.ModelForm):
    class Meta:
            model = Comment
            exclude = ('post', 'user',) # foreign key 빼고 