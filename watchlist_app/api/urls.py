from django.urls import path , include
# from watchlist_app.api import views
from watchlist_app.api import views
from rest_framework.routers import DefaultRouter

app_name = 'watchlist_app'
router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # path("streamplatforms/", views.platforms, name="streamplatforms"),
    # path("streamplatforms/<str:pk>/", views.platform_details, name="streamplatform-details"),
    # path('list/',views.movie_list, name='movie-list'),
    # path('list/<str:pk>/',views.movie_detail, name='movie-detail'),

    path("list/",views.WatchListAV.as_view(), name='movie-list'),
    path('list/<str:pk>/', views.WatchDetailAV.as_view(), name='movie-detail'),

    path('', include(router.urls)),

    path('<str:pk>/reviews-create/', views.ReviewCreate.as_view(), name="reviews-create"),
    path('<str:pk>/reviews/', views.ReviewList.as_view(), name="reviews"),
    path('reviews/<str:pk>/', views.ReviewDetail.as_view(), name="review-detail"),

]
