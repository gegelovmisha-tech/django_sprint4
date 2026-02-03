import os
import sys

# Read file
with open('blogicum/blog/views.py', 'r') as f:
    lines = f.readlines()

# Find edit_comment and add debug
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    
    if 'def edit_comment' in line:
        # Add debug after function start
        debug_lines = [
            '    print("=== DEBUG edit_comment START ===")\n',
            f'    print(f"Post ID: {{post_id}}, Comment ID: {{comment_id}}")\n',
            '    print(f"User: {request.user.username if request.user.is_authenticated else "Anonymous"}")\n',
        ]
        new_lines.extend(debug_lines)
    
    elif 'form = CommentForm(instance=comment)' in line:
        # Add debug after form creation
        new_lines.append('    print(f"DEBUG: Form created. Instance: {form.instance.id if form.instance else "None"}")\n')
        new_lines.append('    print(f"DEBUG: Form initial data: {form.initial}")\n')
    
    elif 'return render(request,' in line and 'edit_comment' in '\n'.join(lines[max(0,i-10):i]):
        # Add debug before return
        new_lines.append('    print("=== DEBUG edit_comment RENDERING ===")\n')
        new_lines.append('    print(f"DEBUG: Context keys: {list(locals().keys()) if "post" in locals() else "NO CONTEXT"}")\n')

# Write back
with open('blogicum/blog/views.py', 'w') as f:
    f.writelines(new_lines)

print("Debug added to edit_comment function")
