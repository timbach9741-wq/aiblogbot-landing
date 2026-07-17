import os

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_block = '''        <div class="hero-content">
            <span class="tag"><span class="tag-icon">🔥</span> AI 블로그 오토-파일럿 Pro V4</span>
            <h1>눈(Vision)을 가진 AI 마케터,<br><span class="gradient-text">사진만 올리면 현장 맞춤 포스팅 완성</span></h1>
            <p class="hero-description">따로 긴 글을 쓰지 않아도 시공·제품 사진을 직접 분석하여 생생한 실제 경험담을 창작합니다. 파스텔톤 자동 썸네일 생성부터 스마트에디터 로봇 회피까지 완벽한 100% 무인 포스팅을 경험하세요.</p>
            <a href="#download" class="btn-primary">지금 무료 다운로드</a>
        </div>
'''

# Find the start and end of the hero-content block
start_idx = 24
end_idx = 40
new_lines = lines[:start_idx] + [new_block] + lines[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated hero-content successfully.')
