import re

with open('blogicum/blog/views.py', 'r') as f:
    content = f.read()

# Find edit_comment function
pattern = r'(@login_required\s*\n)?def edit_comment\([^)]*\):.*?(?=\n\s*@|\n\s*def|\Z)'
match = re.search(pattern, content, re.DOTALL)

if match:
    print("Found edit_comment function:")
    print("-" * 50)
    print(match.group(0))
    print("-" * 50)
    
    # Count lines
    lines = match.group(0).count('\n') + 1
    print(f"Function is {lines} lines long")
    
    # Check what it returns
    if 'return render(' in match.group(0):
        print(" Function returns render()")
    elif 'return redirect(' in match.group(0):
        print(" Function returns redirect()")
    else:
        print(" Function doesn't return render() or redirect()")
else:
    print("Function not found with regex")
    
    # Try simpler search
    print("\nTrying simpler search...")
    lines = content.split('\n')
    in_function = False
    for i, line in enumerate(lines):
        if 'def edit_comment' in line:
            print(f"Found at line {i+1}: {line}")
            in_function = True
        elif in_function:
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                # End of function
                break
            print(f"{i+1}: {line}")
