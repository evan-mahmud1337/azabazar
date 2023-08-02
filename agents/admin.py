from django.contrib import admin
from .models import Agent, Order, Wallet
from import_export.admin import ExportActionMixin
@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('product','status','total')
    search_fields = ('status','product')
    readonly_fields=()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Agent)
admin.site.register(Wallet)
