from django.forms import ModelForm, Textarea, TextInput
from .models import Post, User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["image","text"]
        widgets = {
            'text': Textarea(attrs={
                'class' : 'textarea', 
                'placeholder' : 'Say something...', 
                "rows": 5
            }),
            "image": TextInput(attrs={
                "class":"input",
                "placeholder":"Put an image url here"
            })
        }

class SettingsAboutForm(ModelForm):
    class Meta:
        model = User
        fields = ["about"]
        widgets = {
            'about': Textarea(attrs={
                'class' : 'textarea', 
                'placeholder' : 'Say something...', 
                "rows": 5
            }),
        }