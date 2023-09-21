from django.contrib import admin
from .models import LettersArchiveModel, RecipientModel, SenderModel, RecipientNameModel


# Register your models here.
@admin.register(LettersArchiveModel)
class LettersArchiveAdmin(admin. ModelAdmin):
    prepopulated_fields = {'slug': ('track_number', )}


class RecipientNameInline(admin.TabularInline):
    model = RecipientNameModel
    # form = SubscriberNameForm


class LettersArchiveInline(admin.TabularInline):
    model = LettersArchiveModel


@admin.register(RecipientModel)
class RecipientAdmin(admin.ModelAdmin):
    # list_display = ['build_and_flat', 'build_letter', 'street']
    search_fields = ['build', 'build_letter', 'flat', 'street']
    list_per_page = 15
    inlines = [
        RecipientNameInline,
        LettersArchiveInline
    ]


admin.site.register(SenderModel)

