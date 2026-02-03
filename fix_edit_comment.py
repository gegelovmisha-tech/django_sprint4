import os
import sys

with open('blogicum/blog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find edit_comment function
new_lines = []
in_function = False
function_changed = False

for i, line in enumerate(lines):
    new_lines.append(line)
    
    if 'def edit_comment' in line:
        in_function = True
    
    if in_function and 'return render(request,' in line:
        # Wrap the return in try-catch
        indent = ' ' * (len(line) - len(line.lstrip()))
        
        # Remove the original return line
        new_lines.pop()
        
        # Add try-catch block
        new_lines.append(f'{indent}try:\n')
        new_lines.append(f'{indent}    print("DEBUG: Trying to render template...")\n')
        new_lines.append(f'{indent}    result = render(request, \'blog/detail.html\', {{\n')
        new_lines.append(f'{indent}        \'post\': comment.post,\n')
        new_lines.append(f'{indent}        \'comments\': comments,\n')
        new_lines.append(f'{indent}        \'comment_form\': form,\n')
        new_lines.append(f'{indent}        \'editing_comment\': comment\n')
        new_lines.append(f'{indent}    }})\n')
        new_lines.append(f'{indent}    print(f"DEBUG: Render returned: {{type(result)}}")\n')
        new_lines.append(f'{indent}    return result\n')
        new_lines.append(f'{indent}except Exception as e:\n')
        new_lines.append(f'{indent}    print(f"DEBUG: ERROR in edit_comment: {{e}}")\n')
        new_lines.append(f'{indent}    import traceback\n')
        new_lines.append(f'{indent}    traceback.print_exc()\n')
        new_lines.append(f'{indent}    # Fallback: redirect to post\n')
        new_lines.append(f'{indent}    return redirect(\'blog:post_detail\', id=post_id)\n')
        
        function_changed = True
        in_function = False

# Write back
with open('blogicum/blog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

if function_changed:
    print("Added debug try-catch to edit_comment function")
else:
    print("Could not find edit_comment function to modify")
