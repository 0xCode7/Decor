from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from item.serializers import ItemSerializer
from .models import Favorite
from item.models import Item


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    items = [fav.item for fav in favorites]
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

    if not created:
        favorite.delete()
        return Response({'message': 'Removed from favorites'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Added to favorites'}, status=status.HTTP_201_CREATED)
