from django.shortcuts import render, redirect
from .models import rate_data
import pandas as pd
from datetime import datetime
import json


# Create your views here.
def rate_index(request):
    currency = None
    x_data = None
    y_data = None
    currencies = (
        rate_data.objects.values_list("currency", flat=True)
        .order_by("currency")
        .distinct()
    )

    lastest_date = (
        rate_data.objects.values_list("date", flat=True).order_by("-date").first()
    )

    if request.method == "POST":
        currency = request.POST.get("currency")
        datas = rate_data.objects.filter(currency=currency)

        x_data = list(
            datetime.strftime(date[0], "%Y-%m-%d") for date in datas.values_list("date")
        )

        y_data = list(price[0] for price in datas.values_list("price"))

    result = {
        "currencies": currencies,
        "lastest_date": lastest_date,
        "currency": currency,
        "x_data": json.dumps(x_data),
        "y_data": json.dumps(y_data),
    }

    print(result)

    return render(request, "rate_app/rate_data.html", result)


def update_rate_data(request):
    api_url = "https://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates"

    try:
        # 讀取最新的雲端資料
        read_datas = pd.read_csv(api_url, encoding="utf-8-sig")

        currency_key = set()
        for key in read_datas.keys()[1:]:
            currency_key.add(key)

        insert_datas = []
        for index, data in read_datas.iterrows():
            for key in currency_key:
                # print(data["日期"], key, data[key])

                insert_datas.append(
                    rate_data(
                        date=pd.to_datetime(str(data["日期"])[:8]),
                        price=data[key],
                        currency=key,
                    )
                )

        # 寫入資料庫(忽略錯誤)
        rate_data.objects.bulk_create(insert_datas, ignore_conflicts=True)

    except Exception as ex:
        print(ex)

    return redirect("rateDataUrlName")
