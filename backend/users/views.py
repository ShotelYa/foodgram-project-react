from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow
from users.serializers import FollowSerializer

User = get_user_model()


class FollowApiView(APIView):
    def post(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response(
                {"error": "You can't subscribe to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(user=user, author=author):
            return Response(
                {"error": "You are already subscribed to this author"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_create = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(follow_create,
                                      context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATE)

    def delete(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        follow_delete = Follow.objects.filter(user=user, author=author)
        if follow_delete.exists():
            follow_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowListViewSet(ListAPIView):
    queryset = Follow.objects.all()
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)
