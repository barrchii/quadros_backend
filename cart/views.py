from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Print, CartItem
from .serializers import AddToCartSerializer


def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    
    session_key = request.session.session_key
    if not session_key:
        return CartItem.objects.none()
    return CartItem.objects.filter(session_key=session_key)


def get_price(print_item, size, frame):
    is_framed = frame != 'none'
    if size == 'medium':
        return print_item.medium_framed_price if is_framed else print_item.medium_price
    return print_item.large_framed_price if is_framed else print_item.large_price


def cart_to_json(items):
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'name': item.print_item.name,
            'slug': item.print_item.slug,
            'size': item.size,
            'frame': item.frame,
            'quantity': item.quantity,
            'price': get_price(item.print_item, item.size, item.frame),
        })
    return result


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    slug = serializer.validated_data['slug']
    size = serializer.validated_data['size']
    frame = serializer.validated_data['frame']

    try:
        print_item = Print.objects.get(slug=slug)
    except Print.DoesNotExist:
        return Response({'error': 'Print not found'}, status=status.HTTP_404_NOT_FOUND)

    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            print_item=print_item,
            size=size,
            frame=frame,
            defaults={'quantity': 1}
        )
    else:
        cart_item, created = CartItem.objects.get_or_create(
            session_key=request.session.session_key,
            print_item=print_item,
            size=size,
            frame=frame,
            defaults={'quantity': 1}
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    items = get_cart_items(request)
    return Response({'cart': cart_to_json(items)}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_cart(request):
    items = get_cart_items(request)
    return Response({'cart': cart_to_json(items)}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def remove_from_cart(request, item_id):
    try:
        if request.user.is_authenticated:
            item = CartItem.objects.get(id=item_id, user=request.user)
        else:
            item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    items = get_cart_items(request)
    return Response({'cart': cart_to_json(items)}, status=status.HTTP_200_OK)