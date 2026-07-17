import os

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Subtext for Standard
content = content.replace(
    '<div class="price">89,000원</div>',
    '<div class="price">89,000원</div>\n                <div style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 20px; font-weight: 500;">결제 후 즉시 이용 가능</div>'
)

# Subtext for Deluxe
content = content.replace(
    '<div class="price">239,000원</div>',
    '<div class="price">239,000원</div>\n                <div style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 20px; font-weight: 500;">월 79,667원 · 1개월권 대비 10% 저렴</div>'
)

# Subtext for Premium
content = content.replace(
    '<div class="price">449,000원</div>',
    '<div class="price">449,000원</div>\n                <div style="color: #64748b; font-size: 0.95rem; margin-top: 5px; margin-bottom: 20px; font-weight: 500;">월 74,833원 · 가장 합리적인 선택</div>'
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated pricing subtext successfully.")
