from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import *
from .pricing_engine import calculate_book_price
from .serializers import get_option_serializer


# -----------------------
# Dropdown Options View
# -----------------------
class DropdownOptionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "binding_types": get_option_serializer(BindingType)(BindingType.objects.all(), many=True).data,
            "spine_types": get_option_serializer(SpineType)(SpineType.objects.all(), many=True).data,
            "exterior_colors": get_option_serializer(ExteriorColor)(ExteriorColor.objects.all(), many=True).data,
            "foil_stampings": get_option_serializer(FoilStamping)(FoilStamping.objects.all(), many=True).data,
            "screen_stampings": get_option_serializer(ScreenStamping)(ScreenStamping.objects.all(), many=True).data,
            "corner_protectors": get_option_serializer(CornerProtector)(CornerProtector.objects.all(), many=True).data,
            "interior_colors": get_option_serializer(InteriorColor)(InteriorColor.objects.all(), many=True).data,
            "paper_types": get_option_serializer(PaperType)(PaperType.objects.all(), many=True).data
        })


# -----------------------
# Pricing Calculation View
# -----------------------
class PricingCalculationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            result = calculate_book_price(request.data)
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------
# Reusable Update View
# -----------------------
def create_update_view(model_class, field_names):
    class UpdateView(APIView):
        permission_classes = [AllowAny]

        def put(self, request, pk):
            instance = get_object_or_404(model_class, pk=pk)
            for field in field_names:
                if field in request.data:
                    setattr(instance, field, request.data[field])
            instance.save()
            return Response({"message": f"{model_class.__name__} updated successfully"})
    return UpdateView

# -----------------------
# Registering Update Views
# -----------------------
BindingTypeUpdateView = create_update_view(BindingType, ["price"])
SpineTypeUpdateView = create_update_view(SpineType, ["price"])
ExteriorColorUpdateView = create_update_view(ExteriorColor, ["price"])
FoilStampingUpdateView = create_update_view(FoilStamping, ["price"])
ScreenStampingUpdateView = create_update_view(ScreenStamping, ["price"])
CornerProtectorUpdateView = create_update_view(CornerProtector, ["price"])
InteriorColorUpdateView = create_update_view(InteriorColor, ["price_per_page"])
PaperTypeUpdateView = create_update_view(PaperType, ["price_per_page"])
