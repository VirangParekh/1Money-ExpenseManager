from django.contrib import admin
from .models import Customer
from .models import Expenditure
from .models import Income
from .models import Data

# Register your models here.

admin.site.register(Customer)
admin.site.register(Expenditure)
admin.site.register(Income)
admin.site.register(Data)