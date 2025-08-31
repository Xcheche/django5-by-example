from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView
from django.contrib import messages
from blog.forms import *
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
from .models import *
from django.core.mail import send_mail


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of result
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


# class PostListView(ListView):
#     model = Post
#     context_object_name = "posts"
#     # queryset = Post.published.all()    (Either this way or with get_queryset function)
#     template_name = "blog/post/list.html"
#     paginate_by = 2

#     def get_queryset(self):
#         return Post.published.all()


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
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    # === List of similar posts====
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar_posts": similar_posts,
    }
    return render(request, "blog/post/detail.html", context=context)


# Share post
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
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
            messages.success(request, "Post shared successfully!")
            return redirect(post.get_absolute_url())
    else:
        form = SharePostForm()
    context = {
        "form": form,
        "post": post,
        "sent": sent,
    }
    return render(request, "blog/post/share.html", context=context)


# Comment
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
    # Assign the post to the comment
    comment.post = post
    # Save the comment to the database
    comment.save()
    context = {"post": post, "form": form, "comment": comment}
    return render(request, "blog/post/comment.html", context=context)


# Search view
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post

def post_search(request):
    query = request.GET.get("query", "")
    results = []
    if query:
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        results = Post.published.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.1).order_by('-rank')

    return render(request, "blog/post/search.html", {"results": results, "query": query})
