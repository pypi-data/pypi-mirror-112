from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Dictionary, Newsletter, RssFeed

User = get_user_model()


class NewsletterAdmin(admin.ModelAdmin):
    pass


class DictionaryAdmin(admin.ModelAdmin):
    search_fields = ("word", "pronunciation")
    list_display = ("word", "pronunciation")


class RssFeedAdmin(admin.ModelAdmin):
    list_display = ("user", "feed")
    readonly_fields = ("feed",)
    raw_id_fields = ("user",)

    def get_search_fields(self, request):
        return {"feed", f"user__{User.USERNAME_FIELD}"}


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(RssFeed, RssFeedAdmin)
