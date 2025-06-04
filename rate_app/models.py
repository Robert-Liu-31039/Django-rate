from django.db import models


# Create your models here.
class rate_data(models.Model):
    # 物件型別要同時兩組 null=True, blank=True
    # 才可以代表 該 column 可以為 null
    date = models.DateTimeField(null=False, blank=False)

    # 在字串型別中，blank=True 代表可以為空字串
    currency = models.TextField(blank=False)

    # 在字串型別中，blank=True 代表可以為空字串
    price = models.FloatField(blank=False)

    # 時間型別中，auto_now_add=True 代表自動帶入現在的時間
    created = models.DateTimeField(auto_now_add=True)

    # __str__ 是 models.Model 內的既有函式，
    # 功能只是在 Django 的 管理後端，
    # 將 該資料庫的 資料的顯示 名稱做自定義的顯示
    def __str__(self):  # self 代表是要取同個 model 內的物件
        # id 是 table 預設一定會有的欄位
        return f"{self.date} - {self.currency} - {self.price}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "currency"], name="unique_date_currency"
            )
        ]
