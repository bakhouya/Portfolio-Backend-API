


# =============================================================================
# User Validation Rules
# =============================================================================
USER_RULES = {
    "username": ["required", "unique", "min:3", "max:20", "no_html"],
    "email": ["required", "email", "unique", "max:100", "no_html"],
    "first_name": ["required", "min:2", "max:30", "no_html"],
    "last_name": ["required", "min:2", "max:30", "no_html"]
}
# =============================================================================



# =============================================================================
# User Validation Rules
# =============================================================================
PROFILE_RULES = {
    "job_title": ["required", "unique", "min:3", "max:200", "no_html"],
    "bio": ["required", "no_html"],
    "phone": ["required", "min:2", "max:20", "no_html"],
    "github_url": ["min:10", "no_html"],
    "linkedin_url": ["min:10", "no_html"],
    "youtube_url": ["min:10", "no_html"],
    "facebook_url": ["min:10", "no_html"],
    "instagram_url": ["min:10", "no_html"],
    "whatsapp_url": ["min:10", "no_html"],

    "avatar": ["file", "size:2", "extensions:jpg,jpeg,png,gif"], 
    "cv_file": ["file", "size:2", "extensions:pdf"]   
}
# =============================================================================