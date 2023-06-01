from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from projects.models import Project, Comment
from users.models import User


class ProjectMixin:
    def make_author(
        self,
        email: str = 'username@email.com',
        username: str = 'username',
        password: str = '123456',
    ) -> User:
        '''
        Create a user with the registration parameters.
        '''

        return User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )

    def make_project(
        self,
        title: str = 'Project title',
        description: str = 'Project description',
        explanatory_text: str = 'Project explanatory',
        is_approved: bool = False,
        author_data: User = None,
    ) -> Project:
        '''
        Create a project and a user to be its author.
        '''

        if author_data is None:
            author_data = {}

        return Project.objects.create(
            title=title,
            description=description,
            explanatory_text=explanatory_text,
            is_approved=is_approved,
            author=self.make_author(**author_data)
        )


@override_settings(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
)
class TestBase(TestCase, ProjectMixin):
    def view_test_function(
        self, url: str, view: any, url_kwargs: dict = None
    ) -> None:
        '''
        Base view function test.
        '''
        resolved_view = resolve(reverse(url, kwargs=url_kwargs))

        self.assertIs(resolved_view.func, view)

    def template_test_function(
        self, url: str, template_url: str, url_kwargs: dict = None
    ) -> None:
        '''
        Base template test function.
        '''
        response = self.response_test_function(url, url_kwargs=url_kwargs)
        template = template_url

        self.assertTemplateUsed(response, template)

    def response_test_function(
        self,
        url: str,
        url_kwargs: dict = None,
        method: str = 'get',
        data: dict = None,
        follow: bool = True,
    ):
        '''
        Simplifies responses tests that use GET or POST methods.
        '''
        reversed_url = reverse(url, kwargs=url_kwargs)

        if method == 'get':
            response = self.client.get(
                reversed_url, data=data, follow=follow
            )

        elif method == 'post':
            response = self.client.post(
                reversed_url, data=data, follow=follow
            )

        return response

    def register_and_login(
        self,
        email: str = 'username@email.com',
        password: str = '123456',
    ) -> User:
        '''
        Create a user and login.
        '''
        self.make_author(
            email=email,
            password=password,
        )
        login = self.client.login(
            email=email,
            password=password,
        )

        return login


class ProjectTestBase(TestBase):
    def setUp(self, *args, **kwargs):
        self.project_form_data = {
            'title': 'Project title',
            'description': 'Project description',
            'explanatory_text': 'Project explanatory',
        }

        return super().setUp(*args, **kwargs)

    def make_project_and_login(self) -> Project:
        '''
        Create a approved project and make login with the project's author
        '''
        project = self.make_project(is_approved=True)
        self.client.login(
            email='username@email.com',
            password='123456',
        )

        return project

    def make_comment_and_login(self) -> Comment:
        '''
        Create a comment in a project and make login with the comment's author
        '''
        project = self.make_project(is_approved=True)
        self.client.login(
            email='username@email.com',
            password='123456'
        )

        return Comment.objects.create(
            project=project,
            author=project.author,
            comment='Test comment',
        )
