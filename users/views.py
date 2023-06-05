from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse

from .forms import LoginForm, RegisterForm, UpdateForm
from .tokens import account_activation_token
from projects.models import Project
from .models import User


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:  # noqa
        user = None

    if user is not None and account_activation_token.check_token(
        user, token
    ):
        user.is_active = True
        user.save()

        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('users:login')

    else:
        messages.error(request, 'Não foi possível ativar sua conta!')

    return redirect('projects:home')


def activate_email(request, user, to_email):
    mail_subject = 'Ative sua conta de usuário.'
    message = render_to_string(
        'auth/pages/activate-account.html',
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(
            request, f'Um email de confirmação foi enviado para {to_email}'
        )
    else:
        messages.error(
            request,
            f'O email de verificação não pode ser enviado para {to_email}!'
        )


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('projects:home')
        else:
            form.add_error(field=None, error='Email ou senha inválidos')
    return render(
        request,
        'auth/pages/login.html',
        context={
            'form': form
        }
    )


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        form.cleaned_data.get('confirmed_password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
        )
        activate_email(request, user, email)

        return redirect('users:login')

    return render(
        request,
        'auth/pages/register.html',
        context={
            'form': form
        }
    )


def logout_view(request):
    logout(request)
    return redirect('projects:home')


def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    user_projects = Project.objects.filter(author=user, is_approved=True)
    owner = False
    if request.user.is_authenticated and request.user.id == id:
        owner = True
    return render(
        request,
        'users/pages/user_detail.html',
        context={
            'user': user,
            'projects': user_projects,
            'owner': owner
        }
    )


def user_update(request, id):
    if request.user.is_authenticated and request.user.id == id:
        user = get_object_or_404(User, id=id)
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                new_password = form.cleaned_data.get('new_password')
                linkedin = form.cleaned_data.get('linkedin')
                github = form.cleaned_data.get('github')

                check = check_password(password, user.password)
                if not check:
                    form.add_error(
                        field='password', error='Senha atual incorreta'
                    )
                exists = User.objects.filter(email=email).exists()
                email_error = False
                if exists and email != user.email:
                    form.add_error(
                        field='email',
                        error='Este email já está em uso'
                    )
                    email_error = True

                if check and not email_error:
                    update_fields = []
                    if username != user.username:
                        user.username = username
                        update_fields.append('username')
                    if email != user.email:
                        user.email = email
                        update_fields.append('email')
                    if linkedin:
                        user.linkedin = linkedin
                        update_fields.append('linkedin')
                    if github:
                        user.github = github
                        update_fields.append('github')
                    if new_password:
                        user.password = make_password(new_password)
                        update_fields.append('password')
                        user.save(update_fields=update_fields)
                        return redirect('users:login')
                    user.save(update_fields=update_fields)
                    return redirect(
                        reverse('users:user_detail', kwargs={'id': user.id})
                    )
        else:
            data = {
                'username': user.username,
                'email': user.email,
            }
            form = UpdateForm(initial=data)
        return render(
            request,
            'users/pages/user_update.html',
            context={
                'form': form,
                'id': user.id
            }
        )
    return redirect('projects:home')
