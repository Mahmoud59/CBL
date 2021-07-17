from django.contrib import admin
from django import forms

from faculty.models import Faculty
from .models import Visit, VisitSites, Achievement, Benefician, Activity
from django.contrib.auth import get_user_model
from department.models import Department
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _

# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#admin-custom-validation
# class VisitAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['users'].queryset = self.instance.users.filter(is_staff=False,  is__null=False).all()

from functools import partial
from itertools import groupby
from operator import attrgetter

from django.forms.models import ModelChoiceIterator, ModelChoiceField


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class VisitAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password2'].queryset = Faculty.objects.filter()


class InlineBenefician(admin.StackedInline):
    model = Benefician
    extra = 0
    max_num = 3


class ExpenseForm(forms.ModelForm):
    department = GroupedModelChoiceField(
        queryset=Department.objects.filter(faculty__isnull=False).order_by('faculty'),
        choices_groupby='faculty'
    )


class VisitAdmin(admin.ModelAdmin):
    form = ExpenseForm

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_choice_field
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "users":
            kwargs["queryset"] = settings.AUTH_USER_MODEL.objects.filter(is_staff=False)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # non_model_field.short_description = _("non_model_field")

    list_display = ("id", "name", "site", "visit_course", "date")
    list_display_links = ("name",)
    list_filter = ("date", "site")
    list_editable = ("visit_course", "site")
    search_fields = ("name", "visit_course__title")
    list_per_page = 10
    raw_id_fields = ("meeting",)
    inlines = [InlineBenefician]


admin.site.register(Visit, VisitAdmin)
admin.site.register(VisitSites)
admin.site.register(Achievement)
admin.site.register(Benefician)
admin.site.register(Activity)
