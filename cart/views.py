from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .cart import Cart
from item.models import Item
from .serializer import CartSerializer


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = Cart(request)
    items = cart.get_products()
    total = cart.get_total_price()

    serializer = CartSerializer({
        'items': items,
        'total_price': total
    })

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def cart_add(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    if not product_id:
        return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Item.objects.get(id=product_id)
    except Item.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart(request)
        cart.add(product, quantity)
        return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)
    except ValueError:
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def cart_update(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id or quantity is None:
        return Response({'error': 'product_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Item.objects.get(id=product_id)
    except Item.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    cart = Cart(request)
    cart.update(product, quantity)
    return Response({'message': 'Cart updated'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def cart_delete(request):
    product_id = request.data.get('product_id')

    if not product_id:
        return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    cart = Cart(request)
    cart.delete(product_id)
    return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)
