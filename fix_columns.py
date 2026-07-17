import os

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# I want to delete lines 352 to 430. (In 0-indexed, that's lines[352] to lines[430])
# But wait, python arrays are 0-indexed. My print statements used `i` which corresponds to the 0-indexed position.
# So `del lines[352:431]` will remove elements from index 352 up to index 430 inclusive.
del lines[352:431]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Orphaned 3rd column deleted successfully.")
