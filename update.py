import os

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_block = '''        <div class="guide-grid" style="max-width: 1200px; margin: 0 auto; gap: 20px; display: grid; grid-template-columns: repeat(3, 1fr);">
            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 01</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px;">👁️ Vision AI</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">눈을 가진 AI 사진 분석</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">현장 시공 사진이나 제품 사진을 툭 올리세요. AI가 사진을 정밀 분석해 실제 경험담처럼 생생한 맞춤형 본문을 대리 창작합니다.</p>
            </div>

            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 02</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px;">🎨 썸네일 메이커</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">자동 카드뉴스 썸네일</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">디자인을 전혀 몰라도 됩니다. 상호명과 키워드만 넣으면 트렌디한 파스텔톤 1:1 카드뉴스 대표 이미지를 즉석에서 완성합니다.</p>
            </div>

            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 03</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px;">📢 고정 배너 광고</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">하단 고정 홍보 배너</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">매 포스팅 하단에 매장 연락처, 주소, 상담 링크 등 나만의 고정 홍보 문구를 깔끔한 구분선과 함께 자동으로 자동 부착해 드립니다.</p>
            </div>
        </div>\n'''

# Find the start and end of the target block
start_idx = 290
end_idx = 321
new_lines = lines[:start_idx] + [new_block] + lines[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated successfully.')
