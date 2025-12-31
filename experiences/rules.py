




EXPERIENCE_TYPE_RULES = {
    "title": ["required", "unique", "no_html"]
}

EXPERIENCE_RULES = {
    "title": ["required", "max:200", "unique", "no_html"],
    "company": ["min:3", "max:200", "no_html"],
    "description": ["no_html"],
    "start_date": ["no_html"],
    "end_date": ["min:3", "max:200", "no_html"],
    "type": ["required", "no_html"],
    "logo": ["file", "size:200", "extensions:jpg,jpeg,png,gif"]  
}