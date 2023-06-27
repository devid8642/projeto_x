from django import forms

from .models import Project, Comment
from users.models import ProjectsDate, ProjectIdea
from utils.forms_utils import add_attr


class ProjectForm(forms.ModelForm):
    is_inspired = forms.ModelChoiceField(queryset=None, required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = self.fields['title']
        subtitle = self.fields['subtitle']
        explanatory = self.fields['explanatory_text']
        link = self.fields['link']
        date = ProjectsDate.get_solo()

        if self.instance:
            self.fields['is_inspired'].queryset = ProjectIdea.objects.filter(
                start_date__range=[date.start_date, date.end_date]
            ).order_by('-id')

        add_attr(title, 'placeholder', 'Título do seu projeto')
        add_attr(subtitle, 'placeholder', 'Breve descrição')
        add_attr(
            explanatory, 'placeholder', 'Explique e demonstre seu projeto aqui'
        )
        add_attr(link, 'placeholder', 'Link para o seu projeto/repositório')

    class Meta:
        model = Project

        fields = (
            'title', 'subtitle', 'link', 'explanatory_text', 'is_inspired'
        )


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['comment'], 'placeholder', 'Deixe seu comentário')

    class Meta:
        model = Comment

        fields = ('comment',)
