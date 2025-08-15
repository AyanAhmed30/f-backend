from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .utils import get_available_bindings
from decimal import Decimal

@api_view(['GET'])
@permission_classes([AllowAny])
def get_dropdowns(request):
    trim_sizes = TrimSizeSerializer(TrimSize.objects.all(), many=True).data
    interior_colors = InteriorColorSerializer(InteriorColor.objects.all(), many=True).data
    paper_types = PaperTypeSerializer(PaperType.objects.all(), many=True).data
    cover_finishes = CoverFinishSerializer(CoverFinish.objects.all(), many=True).data

    # Deduplicate binding types by name
    seen = set()
    unique_bindings = []
    for b in BindingType.objects.all():
        if b.name not in seen:
            seen.add(b.name)
            unique_bindings.append(b)
    binding_types = BindingTypeSerializer(unique_bindings, many=True).data

    return Response({
        'trim_sizes': trim_sizes,
        'interior_colors': interior_colors,
        'paper_types': paper_types,
        'cover_finishes': cover_finishes,
        'binding_types': binding_types
    })



# GET bindings based on trim and page count — public access
@api_view(['GET'])
@permission_classes([AllowAny])
def get_bindings_by_trim_and_page_count(request):
    try:
        trim_size_id = int(request.GET.get('trim_size_id'))
        page_count = int(request.GET.get('page_count'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid or missing parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    allowed_names = get_available_bindings(page_count)

    bindings = BindingType.objects.filter(
        trim_size_id=trim_size_id,
        min_pages__lte=page_count,
        max_pages__gte=page_count,
        name__in=allowed_names
    )

    serialized = BindingTypeSerializer(bindings, many=True)
    return Response(serialized.data)


# GET available options based on trim and page count — public access
@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_options(request):
    try:
        trim_size_id = int(request.GET.get('trim_size_id'))
        page_count = int(request.GET.get('page_count'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid or missing parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    allowed_names = get_available_bindings(page_count)

    bindings = BindingType.objects.filter(
        trim_size_id=trim_size_id,
        min_pages__lte=page_count,
        max_pages__gte=page_count,
        name__in=allowed_names
    )

    return Response({
        'bindings': BindingTypeSerializer(bindings, many=True).data,
        'interior_colors': InteriorColorSerializer(InteriorColor.objects.all(), many=True).data,
        'paper_types': PaperTypeSerializer(PaperType.objects.all(), many=True).data,
        'cover_finishes': CoverFinishSerializer(CoverFinish.objects.all(), many=True).data,
    })


# POST cost calculation — public access
@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_cost(request):
    try:
        data = request.data
        page_count = int(data['page_count'])
        quantity = int(data['quantity'])
        trim_size_id = int(data['trim_size_id'])

        binding_name = data['binding_id']
        interior_name = data['interior_color_id']
        paper_name = data['paper_type_id']
        cover_name = data['cover_finish_id']

        # Optional name mappings for flexibility
        interior_name_mapping = {
            "Standard Black and White": "Standard Black & White",
            "Premium Black and White": "Premium Black & White"
        }
        paper_name_mapping = {
            "60# Cream Uncoated": "60# Cream-Uncoated",
            "60# White Uncoated": "60# White-Uncoated",
            "80# White Coated": "80# White-Coated",
            "100# White Coated": "100# White-Coated"
        }
        cover_name_mapping = {
            "Glossy": "Gloss",
            "Matte": "Matte"
        }

        # Apply name corrections
        interior_db_name = interior_name_mapping.get(interior_name, interior_name)
        paper_db_name = paper_name_mapping.get(paper_name, paper_name)
        cover_db_name = cover_name_mapping.get(cover_name, cover_name)

        # Fetch from DB
        binding = get_object_or_404(BindingType, name=binding_name, trim_size_id=trim_size_id, min_pages__lte=page_count, max_pages__gte=page_count)
        interior = get_object_or_404(InteriorColor, name=interior_db_name)
        paper = get_object_or_404(PaperType, name=paper_db_name)
        cover = get_object_or_404(CoverFinish, name=cover_db_name)

        # Calculate cost
        per_book_cost = (
            Decimal(str(binding.price)) +
            Decimal(str(interior.price_per_page)) * page_count +
            Decimal(str(paper.price_per_page)) * page_count +
            Decimal(str(cover.price))
        )

        total_cost = per_book_cost * quantity

        return Response({
            'cost_per_book': float(per_book_cost),
            'total_cost': float(total_cost)
        })

    except (KeyError, ValueError) as e:
        return Response({'error': f'Invalid or missing data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return Response({'error': 'Internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# UPDATE: Interior Color
@api_view(['PUT'])
def update_interior_color(request, pk):
    color = get_object_or_404(InteriorColor, pk=pk)
    price = request.data.get('price_per_page')
    if price is not None:
        color.price_per_page = price
        color.save()
        return Response({'status': 'updated'})
    return Response({'error': 'Invalid input'}, status=400)


# UPDATE: Paper Type
@api_view(['PUT'])
def update_paper_type(request, pk):
    paper = get_object_or_404(PaperType, pk=pk)
    price = request.data.get('price_per_page')
    if price is not None:
        paper.price_per_page = price
        paper.save()
        return Response({'status': 'updated'})
    return Response({'error': 'Invalid input'}, status=400)


# UPDATE: Cover Finish
@api_view(['PUT'])
def update_cover_finish(request, pk):
    cover = get_object_or_404(CoverFinish, pk=pk)
    price = request.data.get('price')
    if price is not None:
        cover.price = price
        cover.save()
        return Response({'status': 'updated'})
    return Response({'error': 'Invalid input'}, status=400)


# ✅ UPDATE: Binding Type
@api_view(['PUT'])
def update_binding_type(request, pk):
    binding = get_object_or_404(BindingType, pk=pk)
    price = request.data.get('price')
    if price is not None:
        binding.price = price
        binding.save()
        return Response({'status': 'updated'})
    return Response({'error': 'Invalid input'}, status=400)
