from.models import Post
from.serializer import PostSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from django.shortcuts import get_list_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

# this is api decomation
# http://127.0.0.1:6589/api-documentation/


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_api(request):
    all_post= Post.objects.all()
    data=PostSerializers(all_post , many=True,context={"request":request}).data
    return Response({
                    'data':data
                    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_details_api(request,id):
    post = get_list_or_404(Post , id=id)
    data=PostSerializers(post , many=True).data
    return Response({
                    'data':data
                    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_search_api(request,query):
    posts=Post.objects.filter(
                        Q(title__icontains=query) |
                        Q(description__icontains=query))
    data=PostSerializers(posts , many=True,context={"request":request}).data
    return Response({
                    'data':data
                    })