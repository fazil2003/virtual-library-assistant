from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('login/',views.login,name='home'),
    path('login_authentication/',views.login_authentication,name='home'),

    path('add_book/',views.add_book,name='home'),
    path('update_book/',views.update_book,name='home'),
    path('delete_book/',views.delete_book,name='home'),

    path('add_book_data/',views.add_book,name='home'),
    path('update_book_data/',views.update_book,name='home'),
    path('delete_book_data/',views.delete_book,name='home'),

    path('showimage_plot/',views.showimage_plot,name='Show Plot'),
    path('showimage_bar/',views.showimage_bar,name='Show Bar'),
    path('showimage_pie/',views.showimage_pie,name='Show Pie'),
    path('showimage_scatter/',views.showimage_scatter,name='Show Scatter'),


    path('showimage_plot_impressions/',views.showimage_plot_impressions,name='Show Plot Impressions'),
    path('showimage_bar_impressions/',views.showimage_bar_impressions,name='Show Bar Impressions'),
    path('showimage_pie_impressions/',views.showimage_pie_impressions,name='Show Pie Impressions'),
    path('showimage_scatter_impressions/',views.showimage_scatter_impressions,name='Show Scatter Impressions'),


    path('showimage_plot_clicks/',views.showimage_plot_clicks,name='Show Plot Clicks'),
    path('showimage_bar_clicks/',views.showimage_bar_clicks,name='Show Bar Clicks'),
    path('showimage_pie_clicks/',views.showimage_pie_clicks,name='Show Pie Clicks'),
    path('showimage_scatter_clicks/',views.showimage_scatter_clicks,name='Show Scatter Clicks'),
]
