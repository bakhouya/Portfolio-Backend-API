

# =====================================================================
# Service ValidationRules
# =====================================================================
SERVICE_RULES = {
    "title": ["required", "max:200", "no_html"],
    "description": ["required", "no_html"],
    "color": ["required", "max:7"],
    "image": ["file", "size:5242880", "extensions:jpg,jpeg,png,gif"]
}
# =====================================================================
