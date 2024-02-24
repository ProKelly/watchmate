from django.shortcuts import get_object_or_404
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.exceptions  import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all() 
    throttle_classes  = [ReviewCreateThrottle]
    # or 
    # def get_queryset(self):
    #     return Review.objects.all()
    def perform_create(self, serializer): #default method we are overriding
        pk = self.kwargs.get('pk')
        watchlist = get_object_or_404(WatchList, pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You can't review movie twice, insttead edit your previous review")
        
        if watchlist.avg_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist = watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    
    def get_queryset(self):#this is a default method we are overriding
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def update(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # def list(self, request):
    #     queryset = StreamPlatform.objects.all()
    #     serializer = StreamPlatformSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     queryset = StreamPlatform.objects.all()
    #     watchlist = get_object_or_404(queryset, pk=pk)
    #     serializer = StreamPlatformSerializer(watchlist)
    #     return Response(serializer.data)
    # def update(self, request, pk=None):
    #     queryset = StreamPlatform.objects.all()
    #     watchlist = get_object_or_404(queryset, pk=pk)
    #     serializer = StreamPlatformSerializer(watchlist, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)


class StreamPlatformsAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(platform, many=False,)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListAV(APIView):

    permission_classes = [AdminOrReadOnly]
    # permission_classes = [AdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):

    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = WatchListSerializer(movie, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    






# @api_view(['GET', 'POST'])
# def platforms(request):

#     if request.method == 'GET':
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def platform_details(request, pk):

#     if request.method == 'GET':
#         platform = get_object_or_404(StreamPlatform, pk=pk)
#         serializer = StreamPlatformSerializer(platform, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         platform = get_object_or_404(StreamPlatform, pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             raise Response(status=status.HTTP_404_NOT_FOUND)
        
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])#api_view(['GET'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         movie = get_object_or_404(Movie, pk=pk) #Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
