import os
import sys
sys.path.append('blogicum')

with open('blogicum/blog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find function edit_comment
in_function = False
function_lines = []
for i, line in enumerate(lines, 1):
    if 'def edit_comment' in line:
        in_function = True
    if in_function:
        function_lines.append(f"{i}: {line.rstrip()}")
        if line.strip() == '' and len(function_lines) > 30:
            # Show first 30 lines of function
            break
        # If next function starts
        if i < len(lines) and lines[i].strip().startswith('def ') and len(function_lines) > 5:
            break

print("=== FUNCTION EDIT_COMMENT CODE ===")
for fline in function_lines:
    print(fline)
