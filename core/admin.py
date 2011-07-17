from django.contrib import admin
from models import Post,CategoryDefault, Location,Quote,RandomLinks,ContactUs
from django.contrib.auth.models import User


class categoryDefaultAdmin(admin.ModelAdmin):
	list_display = ('name','type')
	list_filter = ('type',)

class locationDefaultAdmin(admin.ModelAdmin):
	#list_display = ('name','type')
	list_filter = ('type',)

admin.site.register(Post)
admin.site.register(CategoryDefault,categoryDefaultAdmin)
admin.site.register(Location,locationDefaultAdmin)
admin.site.register(Quote)
admin.site.register(RandomLinks)
admin.site.register(ContactUs)

