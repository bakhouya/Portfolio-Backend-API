



# =============================================================================
# Category Skills Validation Rules
# =============================================================================
EDUCATION_TYPE_RULES = {
    "title": ["required", "unique", "min:3", "no_html"]
}
# =============================================================================
# 
# 
# =============================================================================
# Education Validation Rules
# =============================================================================
EDUCATION_RULES = {
    "field_of_study": ["required", "no_html"],
    "description": ["required", "no_html"],
    "location": ["no_html"],
    "institution": ["required", "no_html"],
    "start_date": ["required", "no_html"],
    "end_date": ["no_html"],

    "type": ["required", "no_html"],

    "logo": ["file", "size:200", "extensions:jpg,jpeg,png,gif"]  
}
# =============================================================================