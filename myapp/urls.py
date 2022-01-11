from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    
    # LOGIN
    path('login_guest/',views.login_guest,name='Login Guest'),
    path('login/',views.login,name='Login Page'),
    path('login_authentication/',views.login_authentication,name='Login Page'),
    path('logout/',views.logout,name='Logout Page'),

    path('profile/',views.profile,name='Profile Page'),
    path('search/',views.search,name='Search Page'),
    path('autocomplete_text/',views.autocomplete_text,name='Autocomplete Text'),
    path('results/',views.results,name='Results Page'),

    path('details/',views.details,name='Details Page'),
    path('inform_me/',views.inform_me,name='Inform Me'),

    # RECOMMENDATIONS
    path('recommendations/',views.recommendations,name='Recommendations Page'),

    # SENTIMENT ANALYSIS
    path('sentiment_analysis/',views.sentiment_analysis,name='Sentiment analysis'),
    path('validate_sentiment_analysis/',views.validate_sentiment_analysis,name='Validate Sentiment analysis'),

    # CHATBOT
    path('chatbot/',views.chatbot,name='Chatbot'),
    path('chatbot_response/',views.chatbot_response,name='Chatbot Response'),

    # BOOKBOT
    path('book_bot/',views.book_bot,name='Bookbot'),
    path('book_bot_response/',views.book_bot_response,name='Bookbot Response'),

    # ASSIGNMENT HELPER
    path('assignment_helper/',views.assignment_helper,name='Assignment Helper'),
    path('assignment_helper_response/',views.assignment_helper_response,name='Assignment Helper'),

    #IMAGE SEARCH
    path('image_search/',views.image_search,name='Image Search Page'),
    path('results_image/',views.results_image,name='Image Results Page'),

    # AVAILABILITY
    path('availability/',views.availability,name='Availability of Book'),
    path('availability_enter/',views.availability_enter,name='Availability of Book'),

    path('clicks_history/',views.clicks_history,name='Clicks History'),
]
