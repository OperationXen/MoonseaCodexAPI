from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

CustomUser = get_user_model()


# this doesn't work and I don't hate myself enough to work out why
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'discord_id',)
        

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'discord_id', 'email', 'is_staff', 'is_active', 'email_verified',)
    list_filter = ('username', 'discord_id', 'email', 'is_staff', 'is_active', 'email_verified',)

    fieldsets = (
        ('User Details', {'fields': ('username', 'email', 'discord_id', 'password', 'email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        ('User Details', {
            'classes': ('wide',),
            'fields': ('email', 'discord_id', 'password1', 'password2', 'email_verified',)}
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )

    search_fields = ('username', 'email', 'discord_id',)
    ordering = ('username', 'email',)
