import os

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_block = '''        <div class="guide-grid">
            <!-- Step 1 Card -->
            <div class="guide-card">
                <span class="step-number">Step 1</span>
                <div class="img-placeholder" style="font-size: 1.5rem; font-weight: bold;">🛡️ 독립 세션 로그인</div>
                <h3>안전한 계정 연동</h3>
                <p>네이버 로봇의 매크로 차단 필터를 무력화하는 독점 크롬 프로필 격리 기술로 사장님의 소중한 아이디를 안전하게 보호합니다.</p>
            </div>

            <!-- Step 2 Card -->
            <div class="guide-card">
                <span class="step-number">Step 2</span>
                <div class="img-placeholder" style="font-size: 1.5rem; font-weight: bold;">🎨 1:1 카드뉴스 제작</div>
                <h3>파스텔 썸네일 자동 생성</h3>
                <p>제목과 상호명만 입력하면, 규격에 딱 맞는 라벤더·파스텔톤 감성의 고품질 대표 카드뉴스 이미지를 프로그램 내부에서 즉시 자동 완성합니다.</p>
            </div>

            <!-- Step 3 Card -->
            <div class="guide-card">
                <span class="step-number">Step 3</span>
                <div class="img-placeholder" style="font-size: 1.5rem; font-weight: bold;">📸 사진 정밀 분석 (Vision)</div>
                <h3>사진 분석 및 원클릭 포스팅</h3>
                <p>최대 15장의 현장 사진을 올리면 Vision AI가 사진을 직접 보고 맞춤형 글을 대리 작성하며, 매크로 탐지 우회 기술로 해시태그까지 확실하게 꽂아 넣습니다.</p>
            </div>
        </div>
'''

# Find the start of the guide-grid inside section id="guide"
# We know from earlier logs that lines 345 to 379 contain the guide-grid block
start_idx = 345
end_idx = 380
new_lines = lines[:start_idx] + [new_block] + lines[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated guide-content successfully.')
