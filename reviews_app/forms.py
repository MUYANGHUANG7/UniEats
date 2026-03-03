from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        # 用户只需要填打分和评语，其他（如时间、是谁写的）后端自动生成
        fields = ['rating', 'comment']