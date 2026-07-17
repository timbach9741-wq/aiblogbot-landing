import os
import re

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Isolate the pricing grid
grid_pattern = r'(<div class="pricing-grid".*?>)(.*)(<!-- Trust Microcopy -->)'

match = re.search(grid_pattern, html_content, flags=re.DOTALL)
if match:
    prefix = match.group(1)
    grid_inner = match.group(2)
    suffix = match.group(3)
    
    # Remove all <ul>...</ul> inside the grid
    new_grid_inner = re.sub(r'<ul>.*?</ul>', '', grid_inner, flags=re.DOTALL)
    
    # Reassemble
    new_content = html_content[:match.start()] + prefix + new_grid_inner + suffix + html_content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Deleted bullet lists from pricing grid successfully.")
else:
    print("Could not find pricing grid.")
