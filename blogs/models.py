from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name='Post Title')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blogs/images')
    slug = models.SlugField(max_length=156,unique=True)
    excerpt = models.CharField(max_length=256)
    content = models.TextField()

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    comment_text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.Case)
    
    def __str__(self):
        return self.comment_text