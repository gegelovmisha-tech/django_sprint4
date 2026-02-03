import re

# Try different encodings
encodings = ['utf-8', 'latin-1', 'cp1252']

for encoding in encodings:
    try:
        with open('blogicum/blog/views.py', 'r', encoding=encoding) as f:
            content = f.read()
        print(f"Successfully read with {encoding} encoding")
        break
    except UnicodeDecodeError:
        continue
else:
    print("Failed to read file with any encoding")
    exit(1)

# Simple search for the function
lines = content.split('\n')
found_start = -1
found_end = -1

for i, line in enumerate(lines):
    if 'def edit_comment' in line:
        found_start = i
        # Find end of function
        for j in range(i+1, len(lines)):
            if lines[j].strip() and not lines[j].startswith((' ', '\t')):
                found_end = j
                break
        if found_end == -1:
            found_end = len(lines)
        break

if found_start != -1:
    print(f"\n=== EDIT_COMMENT FUNCTION (lines {found_start+1}-{found_end}) ===")
    print("-" * 60)
    for j in range(found_start, found_end):
        print(f"{j+1:3}: {lines[j]}")
    print("-" * 60)
    
    # Check returns
    function_text = '\n'.join(lines[found_start:found_end])
    if 'return render(' in function_text:
        print(" Function returns render()")
    elif 'return redirect(' in function_text:
        print(" Function returns redirect()")
    else:
        print(" Function doesn't have return statement")
else:
    print("Function edit_comment not found!")
    
    # Show what's around line 192
    print("\n=== LINES 185-220 ===")
    for j in range(184, 220):
        if j < len(lines):
            print(f"{j+1:3}: {lines[j]}")
