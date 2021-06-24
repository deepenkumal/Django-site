from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post, Comment
from django.views.generic import DetailView, ListView, CreateView
from django.views import View
from .forms import CommentForm
from django.urls import reverse
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = "blogs/index.html"
    context_object_name = 'posts'
    ordering = ["-updated_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


def index(request):
    latest_posts = Post.objects.all().order_by('-updated_date')[:3]
    return render(request, "blogs/index.html", {'posts': latest_posts})


def posts(request):
    posts = Post.objects.all().order_by('-updated_date')
    return render(request, 'blogs/all-posts.html', {'posts': posts})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blogs/post_detail.html"
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['post'] = self.object
#         # context['post_tag'] = context['post'].tag.all()
#         context['post_tag'] = self.object.tag.all()
#         context['comments'] = self.object.comment_set.all().order_by("-id")
#         context['form'] = CommentForm
#         return context

class PostDetailView(View):
    def is_store_post(self, request, post_id):
        stored_posts=request.session.get('stored_posts')
        if post_id in stored_posts:
            is_save_later = False
        else:
            is_save_later =True
        return is_save_later

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        new_comment = Comment(post= post)
        form = CommentForm(request.POST, instance=new_comment)
        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', args=[slug]))
        return render(request,"blogs/post_detail.html",{
            'post': post,
            'form': CommentForm(),
            'post_tag': post.tag.all(),
        })


    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        form = CommentForm()
        post_tag = post.tag.all()
        comments = post.comment_set.all()
        return render(request,"blogs/post_detail.html",{
            'post': post,
            'form': form,
            'post_tag': post_tag,
            'comments': comments,
            'save_later': self.is_store_post(request, post.id),
        })


def tag_page(request, tag):
    print('This is tag')
    try:
        posts = Post.objects.filter(tag__caption__icontains=tag)
    except:
        raise Http404()
    return render(request, 'blogs/tag_page.html', {
        'posts': posts, 'tag': tag,
    })


class ReadLaterViews(View):
        def get(self, request):
            stored_posts = request.session.get('stored_posts')
            context ={}
            if stored_posts is None or len(stored_posts)==0:
                context['stored_posts']=[]
                context['has_post']=False
            else:
                posts = Post.objects.filter(id__in=stored_posts)
                context['stored_posts']=posts
                context['has_post']=True
            return render(request,'blogs/read_later.html',context)

        def post(self, request):
            stored_posts = request.session.get('stored_posts')

            if stored_posts is None:
                stored_posts = []
            post_id = int(request.POST.get('post_id'))
            if post_id not in stored_posts:
                stored_posts.append(post_id)
            else:
                stored_posts.remove(post_id)
            request.session['stored_posts']=stored_posts
            return redirect('index')
