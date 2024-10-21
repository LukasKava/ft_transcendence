from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register('players', views.PlayerViewSet)

#players_router = routers.NestedDefaultRouter(
#    router, 'players', lookup='player')
#players_router.register('match', views.StatsViewSet, basename='player-match')


urlpatterns = router.urls
