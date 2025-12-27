

# =============================================================================
# Category Skills Validation Rules
# =============================================================================
CATEGORY_RULES = {
    "title": ["required", "unique", "min:3", "no_html"]
}
# =============================================================================
# 
# 
# =============================================================================
# Skills Validation Rules  
# =============================================================================
SKILLS_RULES = {
    "title": ["required", "unique", "no_html"],
    "description": ["required", "no_html"],
    "category": ["required", "no_html"],
    "level": ["required", "no_html"],
    "percentage": ["required", "no_html"],
    "color": ["required", "no_html"],

    "icon": ["file", "size:200", "extensions:jpg,jpeg,png,gif"]  
}
# =============================================================================
