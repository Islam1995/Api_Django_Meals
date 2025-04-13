from django.shortcuts import render, get_object_or_404
from .models import Product, Review
from .serializers import ProductSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .filters import ProductFilters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg, Aggregate
# Create your views here.
@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    filterset = ProductFilters(request.GET, queryset= products.order_by('id'))
    count = filterset.qs.count()
    respage = 8
    paginator = PageNumberPagination()
    paginator.page_size =respage
    queryset = paginator.paginate_queryset(filterset.qs,request)
    serializers = ProductSerializers(queryset, many=True).data
    return Response({'products':serializers, 'per page':respage,'count':count})

@api_view(['GET'])
def get_product_by_slug(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializers = ProductSerializers(product, many = False).data
    return Response({'product':serializers})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializers(data = data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user = request.user)
        res = ProductSerializers(product, many=False).data
        return Response({"product":res})
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"error":"sorry you can not update this product"}
        , status= status.HTTP_403_FORBIDDEN)
    product.name = request.data['name']
    product.slug = request.data['slug']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.Catogery = request.data['Catogery']
    product.rating = request.data['rating']
    product.stock = request.data['stock']
    product.save()
    serializer = ProductSerializers(product, many=False)
    return Response({"product":serializer.data})
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"error":"sorry you can not delete this product"}
        , status= status.HTTP_403_FORBIDDEN)
    product.delete()
    return Response({"details":"Delete is done"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    user = request.user
    data = request.data
    review = product.review.filter(user = user)
    if data['rating'] <=0 or data['rating'] > 5:
        return Response({"error":"please inter number from 0 to 5"}, status= status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating':data['rating'], 'comment': data['comment']}
        review.update(**new_review)

        rating = product.review.aggregate(avg_ratings = Avg('rating'))
        product.rating = rating['avg_ratings']
        product.save()
        return Response({'details':'product review updated'})
    else:
        Review.objects.create(
            user=user,
            product = product,
            rating = data['rating'],
            comment = data['comment']
        )
        rating = product.review.aggregate(avg_ratings = Avg('rating'))
        product.rating = rating['avg_rating']
        product.save()
        return Response({'details':'product review created'})

    
