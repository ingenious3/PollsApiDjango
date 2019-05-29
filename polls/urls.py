from django.urls import path
# from .views import polls_details, polls_list
from .apiviews import PollDetails, PollList

urlpatterns = [
	path('polls/', PollList.as_view(), name = 'polls_list'),
	path('polls/<int:pk>/', PollDetails.as_view(), name = 'polls_details'),
]
