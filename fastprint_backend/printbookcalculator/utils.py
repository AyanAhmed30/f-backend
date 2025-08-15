def get_available_bindings(page_count):
    bindings = []
    if page_count >= 3:
        bindings.append("Coil Bound")
    if page_count >= 4:
        bindings += ["Saddle Stitch"]
    if page_count >= 24:
        bindings += ["Case Wrap"]
    if page_count >= 32:
        bindings += ["Perfect Bound", "Linen Wrap"]
    if page_count > 48:
        bindings = [b for b in bindings if b != "Saddle Stitch"]
    if page_count > 470:
        bindings = [b for b in bindings if b != "Coil Bound"]
    return list(set(bindings))
