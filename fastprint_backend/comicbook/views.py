from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .utils import get_allowed_binding_names
from decimal import Decimal



@api_view(['GET'])
@permission_classes([AllowAny])
def get_comic_dropdowns(request):
    return Response({
        'trim_sizes': ComicTrimSizeSerializer(ComicTrimSize.objects.all(), many=True).data,
        'interior_colors': ComicInteriorColorSerializer(ComicInteriorColor.objects.all(), many=True).data,
        'paper_types': ComicPaperTypeSerializer(ComicPaperType.objects.all(), many=True).data,
        'cover_finishes': ComicCoverFinishSerializer(ComicCoverFinish.objects.all(), many=True).data,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comic_bindings(request):
    try:
        trim_size_id = int(request.GET.get('trim_size_id'))
        page_count = int(request.GET.get('page_count'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)

    allowed = get_allowed_binding_names(page_count)
    bindings = ComicBindingType.objects.filter(trim_size_id=trim_size_id, name__in=allowed, min_pages__lte=page_count)
    if bindings.exists():
        bindings = bindings if not bindings[0].max_pages else bindings.filter(max_pages__gte=page_count)

    return Response(ComicBindingTypeSerializer(bindings, many=True).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_comic_cost(request):
    try:
        data = request.data
        page_count = int(data['page_count'])
        quantity = int(data['quantity'])

        binding = ComicBindingType.objects.get(id=data['binding_id'])
        interior = ComicInteriorColor.objects.get(id=data['interior_color_id'])
        paper = ComicPaperType.objects.get(id=data['paper_type_id'])
        cover = ComicCoverFinish.objects.get(id=data['cover_finish_id'])

        unit_price = (Decimal(binding.price)
                      + Decimal(interior.price_per_page) * page_count
                      + Decimal(paper.price_per_page) * page_count
                      + Decimal(cover.price))

        total_price = unit_price * quantity

        discount = Decimal('0.00')
        if quantity > 100:
            discount = total_price * Decimal('0.10')  # example 10% discount

        return Response({
            'cost_per_book': round(unit_price, 2),
            'total_cost': round(total_price, 2),
            'discount': round(discount, 2),
            'final_price': round(total_price - discount, 2)
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def update_comic_binding_type(request, pk):
    try:
        obj = ComicBindingType.objects.get(pk=pk)
    except ComicBindingType.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    
    serializer = ComicBindingTypeSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_comic_interior_color(request, pk):
    try:
        obj = ComicInteriorColor.objects.get(pk=pk)
    except ComicInteriorColor.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    serializer = ComicInteriorColorSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_comic_paper_type(request, pk):
    try:
        obj = ComicPaperType.objects.get(pk=pk)
    except ComicPaperType.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    serializer = ComicPaperTypeSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_comic_cover_finish(request, pk):
    try:
        obj = ComicCoverFinish.objects.get(pk=pk)
    except ComicCoverFinish.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    serializer = ComicCoverFinishSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_comic_bindings(request):
    bindings = ComicBindingType.objects.all()
    return Response(ComicBindingTypeSerializer(bindings, many=True).data)

