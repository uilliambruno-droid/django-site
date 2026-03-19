from django.contrib import admin

from mysite.polls.models import Choice, Question


# Register your models here.
@admin.QuestionAdmin(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.ChoiceAdmin(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass
