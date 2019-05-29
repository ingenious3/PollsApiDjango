from django.urls import path
# from .views import polls_details, polls_list
from .apiviews import PollDetails, PollList, ChoiceList, CreateVote
from rest_framework.routers import DefaultRouter
from .views import PollViewSet

router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')

urlpatterns = [
	path('polls/', PollList.as_view(), name = 'polls_list'),
	path('polls/<int:pk>/', PollDetails.as_view(), name = 'polls_details'),
	path('polls/<int:pk>/choices/', ChoiceList.as_view(), name = 'choice_list'),
	path('polls/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name = 'create_vote'),
]

urlpatterns += router.urls
