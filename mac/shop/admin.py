from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate, User, Admin, ProductReview, Url, Session, Question

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(ProductReview)
admin.site.register(Url)
admin.site.register(Session)
admin.site.register(Question)
