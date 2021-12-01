from django import forms
from posts.models import Post
from django.forms import ClearableFileInput


class NewPostForm(forms.ModelForm):
    # picture = forms.ImageField(required=True)
    # content = forms.FileField(widget=forms.ClearableFileInput(
        # attrs={'multiple': True}), required=True)
    # caption = forms.CharField(widget=forms.Textarea(
    #     attrs={'class': 'input is-medium'}), required=True)
    # tags = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        # fields = ('content', 'caption', 'tags')
        fields = ('caption',)
