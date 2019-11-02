from django.contrib import admin

# Register your models here.
from .models import Teams,Players,Games,Fielder_results,Pitcher_results

admin.site.register(Teams)
admin.site.register(Players)
admin.site.register(Games)
admin.site.register(Fielder_results)
admin.site.register(Pitcher_results)