

# =============================================================================
# Platform Settings Validation Rules
# =============================================================================
PLATFORM_SETTINGS_RULES = {
    "title": ["required", "no_html"],
    "description": ["no_html"],
    "contact_email": ["no_html"],
    "support_email": ["no_html"],
    "phone": ["no_html"],

    "dark_logo": ["file", "size:200", "extensions:jpg,jpeg,png,gif"],
    "light_logo": ["file", "size:200", "extensions:jpg,jpeg,png,gif"],
    "favicon": ["file", "size:200", "extensions:jpg,jpeg,png,gif"],
}
# =============================================================================
# 
# 
# 
# =============================================================================
# Content Validation Rules
# =============================================================================
CONTENT_RULES = {
    "about_title": ["required", "no_html"],
    "about_description": ["required", "no_html"],

    "skill_title": ["required", "no_html"],
    "skill_description": ["required", "no_html"],

    "project_title": ["required", "no_html"],
    "project_description": ["required", "no_html"],

    "experience_title": ["required", "no_html"],
    "experience_description": ["required", "no_html"],

    "education_title": ["required", "no_html"],
    "education_description": ["required", "no_html"],

    "certificate_title": ["required", "no_html"],
    "certificate_description": ["required", "no_html"],

    "service_title": ["required", "no_html"],
    "service_description": ["required", "no_html"],

    "contact_title": ["required", "no_html"],
    "contact_description": ["required", "no_html"],

    "faq_title": ["required", "no_html"],
    "faq_description": ["required", "no_html"],
} 
# =============================================================================
# 
# 
# 
# =============================================================================
# Faq Validation Rules
# =============================================================================
FAQ_RULES = {
    "title": ["required", "unique", "no_html"],
    "description": ["required", "unique", "no_html"],
}
# =============================================================================
