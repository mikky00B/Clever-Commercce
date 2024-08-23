from django.contrib import admin
from .models import CustomUser, UserAddress


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 1  # Number of extra empty address forms to display


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name"]
    inlines = [UserAddressInline]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "country"]
