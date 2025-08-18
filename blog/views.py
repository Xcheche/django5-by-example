from django.shortcuts import render, get_object_or_404,redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView
from django.contrib import messages
from blog.forms import SharePostForm

# Create your views here.
from .models import Post
from django.core.mail import send_mail

# Post list
# def post_list(request):
#     posts = Post.published.all()
#     # Pagination with 3 posts per page


#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     context = {
#         'posts': posts,
#         'page': page_number,
#     }
#     return render(request, "blog/post/list.html",context=context)
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    # queryset = Post.published.all()    (Either this way or with get_queryset function)
    template_name = "blog/post/list.html"
    paginate_by = 2

    def get_queryset(self):
        return Post.published.all()


# Detail view
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})

#Share post
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = SharePostForm(request.POST)
        if form.is_valid():
            # Process the form data
            cd = form.cleaned_data
            # Get absolute or canonical URL of the post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # Send the email
            # Note: Ensure you have configured your email settings in settings.py
            subject = (
                f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            messages.success(request, "Post shared successfully!")
            return redirect("blog:post_detail", post.id) 
    else:
        form = SharePostForm()
    context = {
        "form": form,
        "post": post,
        "sent": sent,
    }
    return render(request, "blog/post/share.html", context=context)
