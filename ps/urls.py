from django.urls import path
from . import views
from django.conf import settings

app_name = 'plant-sharing'
assert isinstance(settings.STATIC_URL, object)
urlpatterns = [
                path('', views.landing_page, name='landing_page'),
                path('home', views.plant_list_search, name='homepage'),
                path('plants/plant', views.plant_add, name='plant_add'),
                path('plants/plant/<int:plant_id>', views.plant_edit, name='plant_edit'),
                path('plants/plant/<int:plant_id>/details', views.plant_details, name='plant_details'),
                path('plants', views.plant_list, name='my_listings'),
                path('messages', views.my_messages, name='my_messages'),
                path('results', views.global_search_results, name='global_search_results'),
                path('plants/plant/delete', views.plant_delete, name='delete_plant_listing'),
                path('plants/plant/all', views.full_list, name='all_plant_listings'),
                path('plants/plant/<int:plant_id>/save', views.save_details, name='plant_data_save'),
                path('plants/<int:plant_id>/comment', views.post_comments, name='post_comment'),
                path('comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
                path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
              ]
