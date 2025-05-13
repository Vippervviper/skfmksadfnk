from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from .models import Quiz, Category, Question, Progress, CSVUpload
from mcq.models import MCQQuestion, Answer
from quiz.models import Sitting


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Убираем возможность удаления и ссылку «Удалить?»
    def has_delete_permission(self, request, obj=None):
        return False


class CSVUploadsAdmin(admin.ModelAdmin):
    model = CSVUpload
    list_display = ('title',)

# …далее остальные ваши регистрации…


class AnswerInline(admin.TabularInline):
    model = Answer
    can_delete = False


class QuizAdminForm(forms.ModelForm):
    """
    from http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """
    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('title', 'category',)
    list_filter  = ('category',)
    search_fields = ('description', 'category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)


@admin.register(MCQQuestion)
class MCQuestionAdmin(admin.ModelAdmin):
    list_display      = ('content', 'category',)
    list_filter       = ('category',)
    fields            = ('content', 'category',
                         'figure', 'quiz', 'explanation', 'answer_order')
    search_fields     = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    inlines           = [AnswerInline]


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
        create a user section
    """
    search_fields = ('user', 'score',)


@admin.register(Sitting)
class SittingAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'complete', 'score_display')

    def score_display(self, obj):
        return obj.get_percent_correct
    score_display.short_description = _('Результат (%)')

