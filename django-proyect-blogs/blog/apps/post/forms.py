from django import forms
from apps.post.models import Post, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'allowed_comments')

class NewPostForm(PostForm):
    image = forms.ImageField(required=False)
    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data['image']
        if commit:
            post.save()
            if image:
                PostImage.objects.create(post=post, image=image)
        return post

class UpdatePostForm(PostForm):
    pass