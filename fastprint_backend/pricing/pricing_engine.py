def calculate_book_price(data):
    try:
        # Convert inputs to correct types
        binding_price = float(data.get('binding_price', 0))
        spine_price = float(data.get('spine_price', 0))
        exterior_color_price = float(data.get('exterior_color_price', 0))
        foil_stamping_price = float(data.get('foil_stamping_price', 0))
        screen_stamping_price = float(data.get('screen_stamping_price', 0))
        corner_protector_price = float(data.get('corner_protector_price', 0))
        interior_color_price = float(data.get('interior_color_price_per_page', 0))
        paper_type_price = float(data.get('paper_type_price_per_page', 0))
        page_count = int(data.get('page_count', 0))
        quantity = int(data.get('quantity', 0))

        # Calculate cost
        cost_per_book = (
            binding_price +
            spine_price +
            exterior_color_price +
            foil_stamping_price +
            screen_stamping_price +
            corner_protector_price +
            (interior_color_price * page_count) +
            (paper_type_price * page_count)
        )

        total_cost = cost_per_book * quantity
        discount = 0.1 if quantity >= 100 else 0
        discounted_amount = total_cost * discount
        amount_after_discount = total_cost - discounted_amount

        return {
            "cost_per_book": round(cost_per_book, 2),
            "total_cost": round(total_cost, 2),
            "discounted_amount": round(discounted_amount, 2),
            "amount_after_discount": round(amount_after_discount, 2),
        }

    except (TypeError, ValueError, KeyError) as e:
        raise Exception(f"Invalid input data: {e}")
