import os
import re

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the hero-content again, injecting the ul before the button.
hero_old_pattern = r'<p class="hero-description">따로 긴 글을 쓰지 않아도 시공·제품 사진을 직접 분석하여 생생한 실제 경험담을 창작합니다. 파스텔톤 자동 썸네일 생성부터 스마트에디터 로봇 회피까지 완벽한 100% 무인 포스팅을 경험하세요.</p>\s*<a href="#download" class="btn-primary">지금 무료 다운로드</a>'

hero_new = '''<p class="hero-description">따로 긴 글을 쓰지 않아도 시공·제품 사진을 직접 분석하여 생생한 실제 경험담을 창작합니다. 파스텔톤 자동 썸네일 생성부터 스마트에디터 로봇 회피까지 완벽한 100% 무인 포스팅을 경험하세요.</p>
            <ul class="features">
                <li><span class="check-icon">✓</span> Vision AI 기반 로컬 사진 정밀 분석 글쓰기</li>
                <li><span class="check-icon">✓</span> 파스텔톤 1:1 카드뉴스 대표 썸네일 자동 빌더</li>
                <li><span class="check-icon">✓</span> 사진 직접 첨부 최대 15장 다중 제한 안전 장치</li>
                <li><span class="check-icon">✓</span> 사진 정렬 방식 최적화 매칭 연동</li>
                <li><span class="check-icon">✓</span> 본문 하단 고정 홍보 배너 및 광고 문구 직접 입력</li>
                <li><span class="check-icon">✓</span> 자바스크립트 기반 태그 편집기 정식 해시태그 강제 입력</li>
                <li><span class="check-icon">✓</span> 크롬 독립 세션 분리 및 좀비 크롬 정밀 강제 종료</li>
                <li><span class="check-icon">✓</span> 작업 완료 후 브라우저 독립 유지 (종료 실수 방지 패치)</li>
            </ul>
            <a href="#download" class="btn-primary">지금 무료 다운로드</a>'''

content = re.sub(hero_old_pattern, hero_new, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated hero-content with features ul list successfully.')
