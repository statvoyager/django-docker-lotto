import random

from django.shortcuts import render
from .models import LottoDraw, LotteryTicket


def index(request):
    return render(request, "lotto/index.html")


def buy_manual(request):
    error_message = None
    ticket = None

    if request.method == "POST":
        buyer_name = request.POST.get("buyer_name", "").strip()
        round_number = request.POST.get("round_number", "1").strip()
        selected_numbers = request.POST.getlist("numbers")

        if not buyer_name:
            error_message = "구매자 이름을 입력해야 합니다."
        elif not round_number.isdigit():
            error_message = "회차는 숫자로 입력해야 합니다."
        elif len(selected_numbers) != 6:
            error_message = "번호는 반드시 6개를 선택해야 합니다."
        else:
            numbers = sorted([int(number) for number in selected_numbers])

            if min(numbers) < 1 or max(numbers) > 45:
                error_message = "번호는 1부터 45 사이여야 합니다."
            elif len(set(numbers)) != 6:
                error_message = "중복된 번호는 선택할 수 없습니다."
            else:
                ticket = LotteryTicket.objects.create(
                    buyer_name=buyer_name,
                    round_number=int(round_number),
                    purchase_type="manual",
                    number1=numbers[0],
                    number2=numbers[1],
                    number3=numbers[2],
                    number4=numbers[3],
                    number5=numbers[4],
                    number6=numbers[5],
                )

    context = {
        "number_range": range(1, 46),
        "error_message": error_message,
        "ticket": ticket,
    }
    return render(request, "lotto/buy_manual.html", context)

def buy_auto(request):
    error_message = None
    ticket = None

    if request.method == "POST":
        buyer_name = request.POST.get("buyer_name", "").strip()
        round_number = request.POST.get("round_number", "1").strip()

        if not buyer_name:
            error_message = "구매자 이름을 입력해야 합니다."
        elif not round_number.isdigit():
            error_message = "회차는 숫자로 입력해야 합니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))

            ticket = LotteryTicket.objects.create(
                buyer_name=buyer_name,
                round_number=int(round_number),
                purchase_type="auto",
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
            )

    context = {
        "error_message": error_message,
        "ticket": ticket,
    }
    return render(request, "lotto/buy_auto.html", context)

def draw_lotto(request):
    error_message = None
    draw = None

    if request.method == "POST":
        round_number = request.POST.get("round_number", "1").strip()

        if not round_number.isdigit():
            error_message = "회차는 숫자로 입력해야 합니다."
        elif LottoDraw.objects.filter(round_number=int(round_number)).exists():
            error_message = f"{round_number}회차 당첨 번호는 이미 추첨되었습니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))

            draw = LottoDraw.objects.create(
                round_number=int(round_number),
                winning_number1=numbers[0],
                winning_number2=numbers[1],
                winning_number3=numbers[2],
                winning_number4=numbers[3],
                winning_number5=numbers[4],
                winning_number6=numbers[5],
            )

    context = {
        "error_message": error_message,
        "draw": draw,
        "draws": LottoDraw.objects.order_by("-round_number"),
    }
    return render(request, "lotto/draw.html", context)

def check_result(request):
    error_message = None
    draw = None
    results = []

    if request.method == "POST":
        buyer_name = request.POST.get("buyer_name", "").strip()
        round_number = request.POST.get("round_number", "1").strip()

        if not buyer_name:
            error_message = "구매자 이름을 입력해야 합니다."
        elif not round_number.isdigit():
            error_message = "회차는 숫자로 입력해야 합니다."
        else:
            round_number = int(round_number)

            try:
                draw = LottoDraw.objects.get(round_number=round_number)
            except LottoDraw.DoesNotExist:
                error_message = f"{round_number}회차 당첨 번호가 아직 추첨되지 않았습니다."
            else:
                tickets = LotteryTicket.objects.filter(
                    buyer_name=buyer_name,
                    round_number=round_number,
                ).order_by("created_at")

                if not tickets.exists():
                    error_message = f"{buyer_name}님의 {round_number}회차 구매 내역이 없습니다."
                else:
                    for ticket in tickets:
                        match_count = ticket.match_count(draw)

                        if match_count == 6:
                            rank = "1등"
                        elif match_count == 5:
                            rank = "2등"
                        elif match_count == 4:
                            rank = "3등"
                        elif match_count == 3:
                            rank = "4등"
                        else:
                            rank = "낙첨"

                        results.append({
                            "ticket": ticket,
                            "match_count": match_count,
                            "rank": rank,
                        })

    context = {
        "error_message": error_message,
        "draw": draw,
        "results": results,
    }
    return render(request, "lotto/check.html", context)