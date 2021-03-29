from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm, AddCategoryForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


class HomeView(ListView):
    model = Post
    template_name = 'blog_post/home.html'
    ordering = ['-date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog_post/post_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked

        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_post/add_post.html'
    # fields = '__all__' #Commented because form class added.


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog_post/update_post.html'
    # fields = ['title', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog_post/delete_post.html'
    success_url = reverse_lazy('Home')


class AddCategoryView(CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'blog_post/category.html'
    # fields = '__all__'


def category_list_view(request):
    category_menu_list = Category.objects.all()
    total_post = dict()
    for i in category_menu_list:
        cat_post = Post.objects.filter(category=i.name)
        total_post[i.id] = cat_post.count()
    return render(request, 'blog_post/category_list.html',
                  {'category_menu_list': category_menu_list, 'total_post': total_post})


def category_view(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    total_post = category_posts.count()
    return render(request, 'blog_post/categories.html', {'cats': cats.title().replace('-', ' '),
                                                         'category_posts': category_posts, 'total_post': total_post})


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog_post/add_comment.html'
    # fields = '__all__'
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


def search_result(request):
    if request.method == "POST":
        searched_post = request.POST['searched']
        posts = Post.objects.filter(title__icontains=searched_post)
        return render(request, 'blog_post/search_result.html', {'searched_post': searched_post, 'posts': posts})
