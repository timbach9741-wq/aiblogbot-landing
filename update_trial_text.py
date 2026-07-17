import os

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences
content = content.replace('3일 무료 체험하기', '3회 무료 이용하기')
content = content.replace('3일 무료체험 후', '3회 무료이용 후')
content = content.replace('3일 무료 체험판', '3회 무료 이용권')
content = content.replace('무료 체험판', '무료 이용권')
content = content.replace('무료 체험 라이선스', '무료 이용 라이선스')
content = content.replace('무료 체험', '무료 이용')
content = content.replace('무료체험', '무료이용')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated trial texts to 3회 successfully.")
