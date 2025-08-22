from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Show email, phone number, date of birth, profile photo and role in the main form
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info', 
            {
                'fields': (
                    'phone_number',
                    'date_of_birth',
                    'profile_photo',
                    'role',
                )
            }
        ),
    )

    # Include email, phone number, date of birth, profile photo and role on the create form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Additional Info',
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'phone_number',
                    'date_of_birth',
                    'profile_photo',
                    'role',
                ),
            }
        ),
    )

    # Columns to display on the user list page
    list_display = [
        'username',
        'email',
        'phone_number',
        'date_of_birth',
        'role',
        'is_staff',
    ]

    # Filters and search to quickly find users by role or contact info
    list_filter = [
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    ]

    search_fields = [
            'username',
            'email',
            'phone_number',
    ]
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
