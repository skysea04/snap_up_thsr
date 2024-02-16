import traceback
import uuid

from basis.logger import log
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import path
from user.models import InviteCode

# Register your models here.
from .models import InviteCode, User


class ListAdminMixin:
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class InviteCodeAdmin(ListAdminMixin, admin.ModelAdmin):
    change_list_template = 'admin/invitecode_change_list.html'

    def get_urls(self):
        urls = [
            path('create_invite_code/', self.create_invite_code),
        ]
        return urls + super().get_urls()

    def create_invite_code(self, request):
        code = uuid.uuid4().hex[:8]
        while InviteCode.is_exist(code):
            code = uuid.uuid4().hex[:8]

        try:
            InviteCode.create(code)

        except Exception as e:
            log.error('Error: %s', e)
            log.error(traceback.format_exc())

        return redirect('..')


admin.site.register(InviteCode, InviteCodeAdmin)


class UserAdminMixin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.related_model == User and not request.user.is_superuser:
            kwargs['queryset'] = User.objects.filter(email=request.user.email)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user

        super().save_model(request, obj, form, change)


class CustomUserAdmin(UserAdmin):
    # Update the list of fields to display in the admin interface.
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)

    _default_field_set = (
        None, {'fields': ('email', 'password')}
    )
    _permissions_field_set = (
        'Permissions',
        {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
    )
    _personal_info_field_set = (
        'Personal info',
        {'fields': ('personal_id', 'phone', 'use_tgo_account')}
    )

    fieldsets = (
        _default_field_set, _permissions_field_set, _personal_info_field_set,
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'invite_code', 'personal_id', 'phone', 'use_tgo_account')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return self.fieldsets

        return (self._default_field_set, self._personal_info_field_set)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(email=request.user.email)


admin.site.register(User, CustomUserAdmin)
