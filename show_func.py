import os
import sys

with open('blogicum/blog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find function
lines = content.split('\n')
start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if 'def edit_comment' in line:
        start_line = i
    elif start_line != -1 and i > start_line:
        if line.strip() and not line.startswith('    ') and not line.startswith('\t') and 'def ' in line:
            end_line = i
            break

if start_line != -1:
    if end_line == -1:
        end_line = len(lines)
    
    print("Lines", start_line+1, "to", end_line+1)
    print("-" * 50)
    for j in range(start_line, min(end_line, start_line + 40)):
        print(f"{j+1:3}: {lines[j]}")
else:
    print("Function edit_comment not found")
