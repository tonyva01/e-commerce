from .models import Order
from django.forms import ModelForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"