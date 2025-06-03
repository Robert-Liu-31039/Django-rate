from django.shortcuts import render, redirect
from .models import rate_data
import pandas as pd
from datetime import datetime


# Create your views here.
def rate_index(request):
    currencies = rate_data.objects.values_list("currency", flat=True).distinct()
    lastest_date = (
        rate_data.objects.values_list("date", flat=True).order_by("-date").first()
    )

    result = {"currencies": currencies, "lastest_date": lastest_date}

    return render(request, "rate_app/rate_data.html", result)


def update_rate_data(request):
    api_url = "https://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates"

    try:
        # 讀取最新的雲端資料
        read_datas = pd.read_csv(api_url, encoding="big5")

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

        # 寫入資料庫
        rate_data.objects.bulk_create(insert_datas)

    except Exception as ex:
        print(ex)

    return redirect("rateDataUrlName")
