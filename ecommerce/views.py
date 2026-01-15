from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer, CategorySerializer, CartSerializer,
    CartItemSerializer, OrderSerializer
)
import uuid


def api_root(request):
    """Welcome endpoint for the API"""
    return JsonResponse({
        'message': 'E-Commerce API Backend',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products/',
            'categories': '/api/categories/',
            'cart': '/api/carts/',
            'orders': '/api/orders/',
            'admin': '/admin/',
        },
        'frontend': 'Run your frontend on a separate port (e.g., 3000)',
    })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = []


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = []

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        return queryset


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = []

    def get_queryset(self):
        return Cart.objects.all()

    def get_cart(self, request):
        session_id = request.data.get('session_id') or request.query_params.get('session_id')
        if not session_id:
            session_id = request.session.get('cart_session_id') or str(uuid.uuid4())
            request.session['cart_session_id'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)
        return cart

    @action(detail=False, methods=['get'], url_path='my-cart')
    def my_cart(self, request):
        cart = self.get_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='update-item')
    def update_item(self, request):
        cart = self.get_cart(request)
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')

        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='remove-item')
    def remove_item(self, request):
        cart = self.get_cart(request)
        cart_item_id = request.data.get('cart_item_id')

        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        cart_item.delete()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_cart(self, request):
        cart = self.get_cart(request)
        cart.items.all().delete()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = []

    def get_queryset(self):
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return Order.objects.filter(session_id=session_id)
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        cart_session_id = request.data.get('session_id')
        cart = get_object_or_404(Cart, session_id=cart_session_id)

        order_data = {
            'order_id': str(uuid.uuid4())[:8].upper(),
            'session_id': cart_session_id,
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'country': request.data.get('country'),
            'zip_code': request.data.get('zip_code'),
            'total_amount': cart.total_price,
            'payment_method': request.data.get('payment_method', 'card'),
            'notes': request.data.get('notes', ''),
        }

        order = Order.objects.create(**order_data)

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.discount_price,
                subtotal=cart_item.subtotal,
            )

        cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
