from django import forms
from .models import Post, Category, Comment


# cats = [('coding', 'coding'), ('sports', 'sports'), ('entertainment', 'entertainment'), ('programming language', 'programming language')]


cats = Category.objects.all().values_list('name', 'name')
cat_list = list()

for item in cats:
    cat_list.append(item)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'body','header_image', 'snippet')

        widgets = {
            'title': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Enter Title'}),
            #'header_image': forms.FileInput(attrs= {'class': 'custom-file-input', 'placeholder': 'Choose Image'}),
            'author': forms.TextInput(attrs= {'class': 'form-control', 'value': '', 'id':'author_name', 'type':'hidden'}),
            #'author': forms.Select(attrs= {'class': 'form-control'}),
            'category': forms.Select(choices= cat_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs= {'class': 'form-control'}),
            'snippet': forms.TextInput(attrs= {'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'header_image', 'snippet')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }