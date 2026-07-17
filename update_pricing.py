import os
import re

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace the pricing grid
new_grid = """<div class="pricing-grid" style="max-width: 1100px;">
            <div class="price-card standard">
                <h3>STANDARD <br><span style="font-size: 1rem; color:#64748b; font-weight: 500;">(1개월 이용권)</span></h3>
                <div class="price">89,000원</div>
                <ul>
                    <li>1개월 정품 라이선스</li>
                    <li>모든 AI 자동화 기능 무제한</li>
                    <li>지속적인 무상 업데이트</li>
                </ul>
                <a href="#pricing" class="btn-buy" id="btn-standard">1개월 신청하기</a>
            </div>
            <div class="price-card premium">
                <div class="best-badge">⭐ 추천 플랜 (약 10% 할인) ⭐</div>
                <h3>DELUXE <br><span style="font-size: 1rem; color:#64748b; font-weight: 500;">(3개월 이용권)</span></h3>
                <div class="price">239,000원</div>
                <ul>
                    <li><strong>3개월 정품 라이선스</strong></li>
                    <li>모든 AI 자동화 기능 무제한</li>
                    <li>지속적인 무상 업데이트</li>
                </ul>
                <a href="#pricing" class="btn-buy premium-btn" id="btn-deluxe">3개월 신청하기</a>
            </div>
            <div class="price-card standard">
                <div class="best-badge" style="background:#8b5cf6;">🔥 파격 특가 (약 16% 할인) 🔥</div>
                <h3 style="margin-top: 20px;">PREMIUM <br><span style="font-size: 1rem; color:#64748b; font-weight: 500;">(6개월 이용권)</span></h3>
                <div class="price">449,000원</div>
                <ul>
                    <li><strong>6개월 정품 라이선스</strong></li>
                    <li>모든 AI 자동화 기능 무제한</li>
                    <li>지속적인 무상 업데이트</li>
                </ul>
                <a href="#pricing" class="btn-buy" id="btn-premium">6개월 신청하기</a>
            </div>
        </div>"""

# Find and replace the old grid
pattern = r'<div class="pricing-grid">.*?</div>\s*<!-- Trust Microcopy -->'
html_content = re.sub(pattern, new_grid + '\n        \n        <!-- Trust Microcopy -->', html_content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated pricing grid to 3 tiers successfully.")
