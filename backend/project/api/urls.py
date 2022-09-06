from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', views.TagViewSet, basename='tags')
router_v1.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('api/', include(router_v1.urls)),
    path('api/', include('users.urls')),
    path('api/recipes/<int:id>/favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('api/ingredients/', views.IngredientListView.as_view(), name='ingredients'),
    path('api/ingredients/<int:id>/', views.IngredientDetailView.as_view(), name='ingredients_detail'),
]
