from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Warehouse, ShippingRequest
from .serializers import ShippingInputSerializer, ShippingRequestSerializer, WarehouseSerializer
import requests
from rest_framework.generics import ListAPIView



class ShippingRateAPIView(APIView):
    """
    POST:
    Accepts user destination address.
    Uses stored warehouse origin to call Easyship API.
    Returns shipping rate and tax info for DHL and FedEx only.
    Saves the request and response for audit.
    """

    EASYSHIP_API_URL = "https://public-api.easyship.com/2024-09/rates"
    EASYSHIP_API_KEY = "sand_y34Y0SNhj5SyU/LcDE57P3XOc9pZOp0JWb0DrsEk1SQ="  # Replace with secure key later

    # Only allow these courier services
    ALLOWED_COURIERS = ["DHL", "FEDEX"]

    # State tax rates for economic nexus calculations
    STATE_TAX_RATES = {
        "TX": 0.0825,  # Texas Sales Tax
        "CA": 0.0725,  # California (example)
        "NY": 0.04,    # New York (example)
        "FL": 0.06,    # Florida (example)
        # Add more states as needed
    }

    def has_economic_nexus(self, state):
        """
        Check if the business has economic nexus in the given state.
        This would typically query your sales database for the state.
        Returns True if over $100,000 in sales OR 200+ transactions in that state.
        """
        # TODO: Implement actual database query for sales data
        # For now, returning False - update this with your actual logic
        
        # Example implementation (replace with actual database query):
        # from django.db.models import Sum, Count
        # from .models import Order  # Your order model
        # 
        # sales_data = Order.objects.filter(
        #     shipping_state=state,
        #     created_at__year=timezone.now().year
        # ).aggregate(
        #     total_revenue=Sum('total_amount'),
        #     transaction_count=Count('id')
        # )
        # 
        # total_revenue = sales_data['total_revenue'] or 0
        # transaction_count = sales_data['transaction_count'] or 0
        # 
        # return total_revenue >= 100000 or transaction_count >= 200
        
        return False  # Update this with your actual implementation

    def calculate_tax_rate(self, country, state, account_type="individual", has_resale_cert=False):
        """
        Comprehensive Tax Logic for Individual and Enterprise Accounts:
        
        Individual Account:
        - If shipping to Texas (US), apply 8.25%
        - If shipping to other US states or internationally, no tax
        
        Enterprise Account:
        - If shipping to Texas: 
          - With valid resale cert: 0% tax
          - Without resale cert: 8.25% tax
        - If shipping to other US states:
          - With economic nexus + no resale cert: apply that state's tax rate
          - With economic nexus + resale cert: 0% tax
          - No economic nexus: 0% tax
        - International shipping: 0% tax
        """
        
        # International shipping - no tax
        if country.upper() != "US":
            return 0.0, "International shipping - no tax"
        
        state = state.upper()
        
        # Individual Account Logic
        if account_type.lower() == "individual":
            if state == "TX":
                return self.STATE_TAX_RATES["TX"], "Texas individual sales tax"
            else:
                return 0.0, "Individual account - no tax for out-of-state shipping"
        
        # Enterprise Account Logic
        elif account_type.lower() == "enterprise":
            if state == "TX":
                if has_resale_cert:
                    return 0.0, "Texas enterprise with resale certificate - no tax"
                else:
                    return self.STATE_TAX_RATES["TX"], "Texas enterprise without resale certificate"
            else:
                # Other US states
                if self.has_economic_nexus(state):
                    if has_resale_cert:
                        return 0.0, f"Economic nexus in {state} with resale certificate - no tax"
                    else:
                        state_rate = self.STATE_TAX_RATES.get(state, 0.0)
                        return state_rate, f"Economic nexus in {state} - applying state tax"
                else:
                    return 0.0, f"No economic nexus in {state} - no tax"
        
        # Default fallback
        return 0.0, "No tax applicable"

    def filter_allowed_couriers(self, rates):
        """
        Filter rates to only include DHL and FedEx services.
        """
        filtered_rates = []
        
        for rate in rates:
            courier_service = rate.get("courier_service", {})
            courier_name = courier_service.get("name", "").upper()
            
            # Check if courier name contains DHL or FEDEX
            if any(allowed_courier in courier_name for allowed_courier in self.ALLOWED_COURIERS):
                filtered_rates.append(rate)
        
        return filtered_rates

    def post(self, request):
        input_serializer = ShippingInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user_data = input_serializer.validated_data

        warehouse = Warehouse.objects.first()
        if not warehouse:
            return Response({"error": "Warehouse origin is not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get account type and resale certificate info from request
        # These should be included in your ShippingInputSerializer
        account_type = user_data.get("account_type", "individual")  # Default to individual
        has_resale_cert = user_data.get("has_resale_cert", False)   # Default to False

        # Build Full Easyship payload combining warehouse + user destination
        payload = {
            "origin_address": {
                "country_alpha2": warehouse.country_alpha2,
                "state": warehouse.state,
                "city": warehouse.city,
                "postal_code": warehouse.postal_code
            },
            "destination_address": {
                "country_alpha2": user_data["country"],
                "state": user_data["state"],
                "city": user_data["city"],
                "postal_code": user_data["postal_code"]
            },
            "incoterms": "DDU",
            "insurance": {"is_insured": False},
            "courier_settings": {
                "show_courier_logo_url": False,
                "apply_shipping_rules": True
            },
            "shipping_settings": {
                "units": {"weight": "kg", "dimensions": "cm"}
            },
            "parcels": [
                {
                    "items": [
                        {
                            "actual_weight": 1.2,
                            "quantity": 1,
                            "declared_currency": "USD",
                            "declared_customs_value": 100,
                            "origin_country_alpha2": warehouse.country_alpha2,
                            "category": "Toys",
                            "hs_code": "95030039",
                            "dimensions": {"length": 20, "width": 10, "height": 5},
                            "contains_battery_pi966": False,
                            "contains_battery_pi967": False,
                            "contains_liquids": False,
                        }
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.EASYSHIP_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        api_response = requests.post(self.EASYSHIP_API_URL, json=payload, headers=headers)

        if api_response.status_code != 200:
            return Response({"error": "Easyship API failed", "details": api_response.json()}, status=api_response.status_code)

        data = api_response.json()
        all_rates = data.get("rates", [])

        if not all_rates:
            return Response({"error": "No shipping rates available", "details": data}, status=status.HTTP_404_NOT_FOUND)

        # Filter to only show DHL and FedEx rates
        filtered_rates = self.filter_allowed_couriers(all_rates)

        if not filtered_rates:
            return Response({
                "error": "No DHL or FedEx shipping rates available for this destination",
                "available_couriers": [rate.get("courier_service", {}).get("name", "Unknown") for rate in all_rates]
            }, status=status.HTTP_404_NOT_FOUND)

        # Get the cheapest rate from filtered results
        cheapest_rate = min(filtered_rates, key=lambda r: r.get("total_charge", float('inf')))
        shipping_rate = cheapest_rate.get("total_charge")

        # Apply comprehensive tax logic
        tax_rate, tax_reason = self.calculate_tax_rate(
            user_data["country"], 
            user_data["state"], 
            account_type, 
            has_resale_cert
        )
        estimated_tax = round(shipping_rate * tax_rate, 2)

        # Save request and response info
        shipping_record = ShippingRequest.objects.create(
            user_address=user_data,
            shipping_rate=shipping_rate,
            tax=estimated_tax,
            response_data=data,
        )

        response_payload = {
            "shipping_rate": shipping_rate,
            "tax": estimated_tax,
            "tax_rate": f"{tax_rate * 100:.2f}%",
            "tax_reason": tax_reason,
            "account_type": account_type,
            "courier_name": cheapest_rate["courier_service"]["name"],
            "estimated_delivery": f"{cheapest_rate['min_delivery_time']}-{cheapest_rate['max_delivery_time']} days",
            "shipping_request_id": shipping_record.id,
            "available_services": [
                {
                    "courier_name": rate["courier_service"]["name"],
                    "service_name": rate.get("service_name", ""),
                    "total_charge": rate.get("total_charge"),
                    "delivery_time": f"{rate['min_delivery_time']}-{rate['max_delivery_time']} days"
                }
                for rate in filtered_rates
            ]
        }

        return Response(response_payload, status=status.HTTP_200_OK)
    
class SaveShippingAPIView(APIView):
    """
    POST endpoint to save shipping info from frontend.
    """
    def post(self, request):
        serializer = ShippingRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Shipping info saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class ShippingRequestListAPIView(ListAPIView):
    queryset = ShippingRequest.objects.all().order_by('-created_at')
    serializer_class = ShippingRequestSerializer
class WarehouseListAPIView(ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer    