from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from .models import Post
from .form import SignUpForm, SignInForm, FeedBackForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from taggit.models import Tag


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'myblog/home.html', context={
            'page_obj': page_obj,
        })


class PostViewDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:3]
        return render(request, 'myblog/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': "Написать мне",
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # send_mail(f'От {name} на тему {subject}', message, from_email, ['komel97@yandex.ru'])
                # отправка писем не работает, т.к. проект в локальной сети
                # поэтому сделана просто переадресация на страницу с успешной отправкой письма
                return render(request, 'myblog/success.html', context={
                    'title': "Сообщение отправлено",
                    'name': name,
                    'from_email': from_email,
                    'subject': subject,
                    'message': message,
                })
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('Success')

        return render(request, 'myblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success.html', context={
            'title': "Спасибо :3",
        })


class SearchResultView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""

        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )

        paginator = Paginator(results, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'myblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count,
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag,slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()

        return render(request, 'myblog/tag.html', context={
            'title': f'#ТЭГ {tag}',
            'posts': posts,
            'common_tags': common_tags,
        })