DOCUMENT_DEFAULT_OUTPUT_TYPE = "text/x-html-safe"
REQUIRED_TRANSFORM = ["ruid_to_url"]

TAG_PATTERN = r'(\<(img|a)[^>]*>)'
UID_PATTERN = r'[^"]*resolveuid/(?P<uid>[^/"#? ]*)'
