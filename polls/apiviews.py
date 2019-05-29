from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer

class PollList(generics.ListAPIView):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

class PollDetails(generics.RetrieveDestroyAPIView):
	# queryset = get_object_or_404(Poll,pk)
	queryset = Poll.objects.all
	serializer_class = PollSerializer

class ChoiceList(generics.ListCreateAPIView):
	def get_queryset(self):
		queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
		return queryset
	serializer_class = ChoiceSerializer

	def post(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs['pk'])
		if not request.user == poll.created_by:
			raise PermissionError("You can not create choice for the poll")
		return super().post(request,*args, **kwargs)

class CreateVote(generics.CreateAPIView):
	def post(self, request, pk, choice_pk):
		voted_by = request.data.get("voted_by")
		data = {'choice': choice_pk, 'poll':pk, 'voted_by':voted_by}
		serializer = VoteSerializer(data=data)
		if serializer.is_valid():
			vote =  serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserSerializer

class LoginView(APIView):
	permission_classes = ()
	def post(self, request,):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username = username, password = password)
		if user:
			return Response({'token':user.auth_token.key})
		else:
			return Response({'error':'Wrong credentials'},status=status.HTTP_400_BAD_REQUEST)


# class PollList(APIView) :
# 	def get(self, request):
# 		polls = Poll.objects.all()[:20]
# 		data  = PollSerializer(polls,many=True).data
# 		return Response(data)
#
# class PollDetails(APIView):
# 	def get(self, request, pk):
# 		poll = get_object_or_404(Poll, pk=pk )
# 		data = PollSerializer(poll).data
# 		return Response(data)
