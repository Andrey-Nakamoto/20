import datetime
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import *


def subscribers_send_mails(pk, headline, subscribers_emails):
    html_context = render_to_string(
        'mail/post_add_email.html',
        {
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject= titles,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


def post_comment_send_mail(pk, email):
    html_context = render_to_string(
        'mail/coment_add_email.html',
        {
            'link': f'{settings.SITE_URL}/ads/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новый отклик',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


def comment_author_send_mail(pk, email):
    html_context = render_to_string(
        'mail/comment_author_email.html',
        {
            'link': f'{settings.SITE_URL}/ads/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Отклик принят',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


@shared_task
def posts_add_notification(pk):
    post = Post.objects.get(id=pk)
    category = post.category
    subscribers = []
    subscribers_emails = []
    subscribers += category.subscribers.all()

    for s in subscribers:
        subscribers_emails.append(s.email)

    subscribers_send_mails(post.pk, post.titles, subscribers_emails)


@shared_task
def post_comment_notification(pk):
    comment = Post.objects.get(id=pk)
    post = comment.post
    post_author_email = [post.author.email]
    post_comment_send_mail(post.pk, post_author_email)


@shared_task
def comment_approve_notification(pk):
    comment = Comment.objects.get(id=pk)
    post = comment.post
    comment_author_email = [comment.author.email]
    comment_author_send_mail(post.pk, comment_author_email)



@shared_task
def my_job():
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    ads = Post.objects.filter(created_at__gte=week_ago)
    categories = set(ads.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'mail/Weekly_announcement.html',
        {
            'link': settings.SITE_URL,
            'ads': ads
        }
    )
    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)