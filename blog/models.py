from django.db import models

from django.conf import settings
from django.urls import reverse
from common.models import BaseModel
from taggit.managers import TaggableManager


# Custom manager to filter published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Model for blog posts
# Inherits from BaseModel which has created_at and updated_at fields
# The Post model represents a blog post with fields for title, slug, author, body,
class Post(BaseModel):
    tags = TaggableManager()  # for taggit
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField()

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    # Metadata for the post
    class Meta:
        ordering = ["-publish"]
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    # Get absolute url using args positional arguments or kwargs keyword arguments could be used
    # Canonical URL for the post
    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={
                "post": self.slug,
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
            },
        )


# Comment Feature
class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    # Already inherited from BaseModel
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            # Helps to speed up queries that filter by created date in the database very important for any database model
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
