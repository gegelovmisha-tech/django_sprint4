#!/bin/bash
FILE="blogicum/templates/blog/detail.html"

# Add debug before comments loop
sed -i '/{% for comment in comments %}/i\<!-- DEBUG: comments count = {{ comments|length }}, editing_comment = {{ editing_comment.id|default:"None" }} -->' "$FILE"

# Add debug before editing condition
sed -i '/{% if editing_comment and editing_comment.id == comment.id %}/i\<!-- DEBUG: comment.id = {{ comment.id }}, editing_comment.id = {{ editing_comment.id|default:"None" }} -->' "$FILE"

# Add debug after form
sed -i '/{% endif %}/a\<!-- DEBUG: End editing_comment block -->' "$FILE"

echo "Debug added to template"
