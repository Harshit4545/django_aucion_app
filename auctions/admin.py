from django.contrib import admin
from .models import Comment, listing,User,Bid, watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(watchlist)

