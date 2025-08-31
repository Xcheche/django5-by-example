from email.mime import text
from django import template
from ..models import Post
import markdown
from django.utils.safestring import mark_safe

register = template.Library()


# Total posts
@register.simple_tag
def total_posts():
    return Post.published.count()


# Latest post
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# Total comments
from django.db.models import Count


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


# ===Template filters===


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
