from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

from decimal import Decimal

@api_view(['GET'])
def get_dropdowns(request):
    return Response({
        "trim_sizes": TrimSizeSerializer(TrimSize.objects.all(), many=True).data,
        "interior_colors": InteriorColorSerializer(InteriorColor.objects.all(), many=True).data,
        "paper_types": PaperTypeSerializer(PaperType.objects.all(), many=True).data,
        "cover_finishes": CornerProtectorSerializer(CornerProtector.objects.all(), many=True).data,
        "spines": SpineSerializer(Spine.objects.all(), many=True).data,
        "exterior_colors": ExteriorColorSerializer(ExteriorColor.objects.all(), many=True).data,
        "foil_stampings": FoilStampingSerializer(FoilStamping.objects.all(), many=True).data,
        "screen_stampings": ScreenStampingSerializer(ScreenStamping.objects.all(), many=True).data,
        "bindings": BindingTypeSerializer(BindingType.objects.all(), many=True).data,
    })

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    try:
        pages = int(data['page_count'])
        qty = int(data['quantity'])

        binding = BindingType.objects.get(id=data['binding_id'])
        interior = InteriorColor.objects.get(id=data['interior_color_id'])
        paper = PaperType.objects.get(id=data['paper_type_id'])
        corner = CornerProtector.objects.get(id=data['cover_finish_id'])

        base_price = binding.price
        spine_price = Decimal(5)
        color_price = Decimal(0)
        paper_price = Decimal(0)

        if data.get('spine_id'):
            spine = Spine.objects.get(id=data['spine_id'])
            spine_price = spine.price

        if data.get('exterior_color_id'):
            ext = ExteriorColor.objects.get(id=data['exterior_color_id'])
            color_price = ext.price

        if data.get('foil_stamping_id'):
            foil = FoilStamping.objects.get(id=data['foil_stamping_id'])
            foil_price = foil.price
        else:
            foil_price = Decimal(0)

        if data.get('screen_stamping_id'):
            screen = ScreenStamping.objects.get(id=data['screen_stamping_id'])
            screen_price = screen.price
        else:
            screen_price = Decimal(0)

        interior_price = interior.price_per_page * pages
        paper_price = paper.price_per_page * pages
        cover_price = corner.price

        book_price = base_price + spine_price + color_price + foil_price + screen_price + interior_price + paper_price + cover_price
        total_cost = book_price * qty

        if qty > 100:
            discount = Decimal(0.05) * total_cost
            discounted = total_cost - discount
        else:
            discounted = total_cost

        return Response({
            "cost_per_book": round(book_price, 2),
            "total_cost": round(discounted, 2)
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)
@api_view(['GET'])
def get_bindings(request):
    trim_size_id = request.GET.get('trim_size_id')
    page_count = request.GET.get('page_count')

    if not trim_size_id or not page_count:
        return Response({"error": "Missing parameters"}, status=400)

    try:
        # You can customize this logic as needed
        bindings = BindingType.objects.all()

        serializer = BindingTypeSerializer(bindings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
@api_view(['PUT'])
def update_binding(request, pk):
    binding = get_object_or_404(BindingType, pk=pk)
    binding.price = request.data.get('price', binding.price)
    binding.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_interior_color(request, pk):
    color = get_object_or_404(InteriorColor, pk=pk)
    color.price_per_page = request.data.get('price_per_page', color.price_per_page)
    color.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_paper_type(request, pk):
    paper = get_object_or_404(PaperType, pk=pk)
    paper.price_per_page = request.data.get('price_per_page', paper.price_per_page)
    paper.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_cover_finish(request, pk):
    cover = get_object_or_404(CornerProtector, pk=pk)
    cover.price = request.data.get('price', cover.price)
    cover.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_spine(request, pk):
    spine = get_object_or_404(Spine, pk=pk)
    spine.price = request.data.get('price', spine.price)
    spine.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_exterior_color(request, pk):
    ext = get_object_or_404(ExteriorColor, pk=pk)
    ext.price = request.data.get('price', ext.price)
    ext.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_foil_stamping(request, pk):
    foil = get_object_or_404(FoilStamping, pk=pk)
    foil.price = request.data.get('price', foil.price)
    foil.save()
    return Response({"success": True})


@api_view(['PUT'])
def update_screen_stamping(request, pk):
    screen = get_object_or_404(ScreenStamping, pk=pk)
    screen.price = request.data.get('price', screen.price)
    screen.save()
    return Response({"success": True})