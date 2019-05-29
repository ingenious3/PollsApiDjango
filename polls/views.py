# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse

from rest_framework import viewsets
from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

# def polls_list ( request ) :
# 	MAX_OBJECTS = 20
# 	polls = Poll.objects.all()[:MAX_OBJECTS]
# 	data = {'result': list(polls.values('question','created_by', 'pub_date'))}
# 	return JsonResponse(data)

# def polls_details ( request, pk) :
# 	poll = get_object_or_404(Poll, pk = pk)
# 	# data = {'results': {
# 	# 				'question':poll.question, 'created_by':poll.created_by, 'pub_date':poll.pub_date
# 	# 		} }
#
# 	data = {'results': { 'question': poll.question, 'pub_date': poll.pub_date } }
# 	return JsonResponse(data)

class PollViewSet(viewsets.ModelViewSet):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

	def destroy(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs['pk'])
		if not request.user == poll.created_by:
			raise PermissionError("You can not delete the poll")
		return super().destroy(request,*args, **kwargs)