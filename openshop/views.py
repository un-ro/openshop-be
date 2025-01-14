from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from openshop.serializers import ProductSerializer
from .models import Product

# Create your views here.
class ProductList(APIView):
    def post(self, request):
        product = ProductSerializer(data=request.data, context={'request': request})

        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = Product.objects.all()

        # Filter from soft delete challenge
        products = products.filter(is_delete=False)
        
        # Search by name
        query = request.query_params.get('name', None)
        if query is not None:
            products = products.filter(name__icontains=query)
        
        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)
    

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404({
                'detail': 'Not found.',
                'message': f'Product with id {pk} not found'
            })
        
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Error updating product',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)

        # Soft delete
        try:
            product.is_delete = True
            product.save()
        except:
            return Response({
                'message': 'Error deleting product'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)