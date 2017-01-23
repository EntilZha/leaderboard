from django.conf.urls import url, include
from django.contrib import admin

from leaderboard.views import pages

urlpatterns = [
    url(r'^$', pages.index),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('leaderboard.urls'))
]
