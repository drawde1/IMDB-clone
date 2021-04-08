from django.contrib import admin
from IMDB_user.models import MyCustomUser
# Register your models here.
from django.contrib.auth.admin import UserAdmin


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = MyCustomUser

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': [
                    'displayname',
                    'watch_list',
                    'favorites_list'
                ]
            }
        )
    )


admin.site.register(MyCustomUser, CustomUserAdmin)
