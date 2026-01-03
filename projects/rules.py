




# ============================================================================
# Project Types Validation Rules
# ============================================================================
PROJECT_TYPES_RULES = {
    "title": ["required", "unique", "max:100", "no_html"]
}
# ============================================================================
# 
# 
# ============================================================================
# Project Validation Rules 
# ============================================================================
PROJECT_RULES = {
    "title": ["required", "unique", "max:200", "no_html"],
    "description": ["required","no_html"],
    "details": ["required", "no_html"],
    "type": ["required"],
    "demo_url": ["no_html"],
    "github_url": ["no_html"],
    "video_url": ["no_html"],
    "project_date": ["required", "no_html"],
    "skills": ["required"]
}
# ============================================================================
