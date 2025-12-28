


# ==========================================================================
# Certificate validate rules
# ==========================================================================
CERTIFICATE_RULES = {
    "title": {"required", "unique", "no_html"},
    "description": {"required", "no_html"},
    "issuing_organization": {"required", "no_html"},
    "issue_date": {"required", "no_html"},
    "expiration_date": {"no_html"},
    "credential_id": {"no_html"},
    "credential_url": {"no_html"},
    "skills": {"required"},
    "image": ["file", "size:200", "extensions:jpg,jpeg,png,gif"],
}
# ==========================================================================
