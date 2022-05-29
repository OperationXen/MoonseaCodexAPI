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
    list_display = ('username', 'discord_id', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'discord_id', 'email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'discord_id', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email', 'discord_id',)
    ordering = ('username', 'email',)
