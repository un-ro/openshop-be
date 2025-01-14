from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from openshop.serializers import ProductSerializer
from .models import Product

# Create your views here.
class ProductList(APIView):
    def post(selft, request):
        product = ProductSerializer(data=request.data, context={'request': request})

        if product.is_valid(raise_exception=True):
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)
    

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = ProductSerializer(note, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = ProductSerializer(note, data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)