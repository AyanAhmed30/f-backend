def get_allowed_binding_names(page_count):
    bindings = []
    if page_count >= 3:
        bindings.append("Coil Bound")
    if page_count >= 4:
        bindings.append("Saddle Stitch")
    if page_count >= 24:
        bindings.append("Case Wrap")
    if page_count >= 32:
        bindings.extend(["Perfect Bound", "Linen Wrap"])
    return list(set(bindings))