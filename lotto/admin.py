from django.contrib import admin
from .models import LottoDraw, LotteryTicket


@admin.register(LotteryTicket)
class LotteryTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer_name",
        "round_number",
        "purchase_type",
        "get_numbers",
        "created_at",
    )
    list_filter = ("round_number", "purchase_type", "created_at")
    search_fields = ("buyer_name",)

    def get_numbers(self, obj):
        return obj.numbers()

    get_numbers.short_description = "구매 번호"


@admin.register(LottoDraw)
class LottoDrawAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "round_number",
        "get_winning_numbers",
        "created_at",
    )
    list_filter = ("round_number", "created_at")

    def get_winning_numbers(self, obj):
        return obj.numbers()

    get_winning_numbers.short_description = "당첨 번호"