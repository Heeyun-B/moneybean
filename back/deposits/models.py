from django.db import models


# Create your models here.
class DepositProducts(models.Model):
    """정기예금 상품 기본 정보"""

    fin_prdt_cd = models.CharField(max_length=100, primary_key=True)  # 금융상품 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=200)  # 금융상품명
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    join_deny = models.IntegerField(
        choices=[(1, "제한없음"), (2, "서민전용"), (3, "일부제한")], default=1
    )  # 가입제한
    join_member = models.TextField(blank=True, null=True)  # 가입대상
    join_way = models.CharField(max_length=100, blank=True, null=True)  # 가입방법
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대조건
    mtrt_int = models.TextField(blank=True, null=True)  # 만기 후 이자율
    max_limit = models.BigIntegerField(
        blank=True, null=True
    )  # 최고한도 (금액이 클 수 있음)
    dcls_month = models.CharField(max_length=6)  # 공시 제출월 (YYYYMM)
    dcls_strt_day = models.CharField(max_length=8, blank=True, null=True)  # 공시 시작일
    dcls_end_day = models.CharField(max_length=8, blank=True, null=True)  # 공시 종료일
    fin_co_subm_day = models.CharField(
        max_length=12, blank=True, null=True
    )  # 금융회사 제출일

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"


class DepositOptions(models.Model):
    """정기예금 상품 옵션 정보"""

    product = models.ForeignKey(
        DepositProducts,
        on_delete=models.CASCADE,
        related_name="options",
        to_field="fin_prdt_cd",
    )  # 상품 외래키
    intr_rate_type = models.CharField(
        max_length=10
    )  # 저축 금리 유형 (S: 단리, M: 복리)
    intr_rate_type_nm = models.CharField(max_length=50)  # 저축 금리 유형명
    save_trm = models.IntegerField()  # 저축 기간 (개월)
    intr_rate = models.FloatField(default=-1)  # 저축 금리
    intr_rate2 = models.FloatField(default=-1)  # 최고 우대금리

    class Meta:
        # 같은 상품의 같은 금리 유형, 같은 기간은 중복 저장 방지
        unique_together = ("product", "intr_rate_type", "save_trm")

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"
