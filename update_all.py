import os
import re

path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Hero Content
hero_old_pattern = r'<div class="hero-content">.*?</div>\s*<div class="hero-image">'
hero_new = '''<div class="hero-content">
            <span class="tag"><span class="tag-icon">🔥</span> AI 블로그 오토-파일럿 Pro V4</span>
            <h1>눈(Vision)을 가진 AI 마케터,<br><span class="gradient-text">사진만 올리면 현장 맞춤 포스팅 완성</span></h1>
            <p class="hero-description">따로 긴 글을 쓰지 않아도 시공·제품 사진을 직접 분석하여 생생한 실제 경험담을 창작합니다. 파스텔톤 자동 썸네일 생성부터 스마트에디터 로봇 회피까지 완벽한 100% 무인 포스팅을 경험하세요.</p>
            <a href="#download" class="btn-primary">지금 무료 다운로드</a>
        </div>
        <div class="hero-image">'''
content = re.sub(hero_old_pattern, hero_new, content, flags=re.DOTALL)

# 2. Replace Guide Grid
# In the clean file, under `<section id="guide" class="guide-section">` there is `<h2>어떻게 사용하나요? (3분 가이드)</h2>` and then `<div class="guide-grid">`
guide_old_pattern = r'<section id="guide" class="guide-section">\s*<h2>어떻게 사용하나요\? \(3분 가이드\)</h2>\s*<div class="guide-grid">.*?</div>\s*</section>'
guide_new = '''<section id="guide" class="guide-section">
        <h2>어떻게 사용하나요? (3분 가이드)</h2>
        <div class="guide-grid">
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
    </section>'''
content = re.sub(guide_old_pattern, guide_new, content, flags=re.DOTALL)

# Also wait, the user's FIRST request was replacing the "핵심 기술 3가지" under features!
# I need to do that too because I restored the clean file!
# The killer features section has: `<div class="section-badge" ...>KILLER FEATURE</div>`
features_old_pattern = r'<section class="features-section"([^>]*)>.*?<div class="guide-grid"[^>]*>.*?</div>\s*</section>'
features_new = '''<section class="features-section"\\1>
        <div class="section-badge" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; margin-bottom: 20px;">KILLER FEATURE</div>
        <h2 style="font-size: 2.2rem; margin-bottom: 30px; line-height: 1.4; color: var(--text-main, #111827);">똑같은 글만 찍어내는 로봇은 그만.<br>당신의 블로그를 완벽한 '마케팅 오토-파일럿'으로.</h2>
        <p class="section-desc" style="margin-top: 15px; margin-bottom: 50px; color: var(--text-sub, #4b5563); font-size: 1.1rem;">AI Blogbot Pro에만 존재하는 독보적인 3가지 핵심 기술을 확인하세요.</p>
        
        <div class="guide-grid" style="max-width: 1200px; margin: 0 auto; gap: 20px; display: grid; grid-template-columns: repeat(3, 1fr);">
            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 01</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px; background: transparent; border: none; height: auto;">👁️ Vision AI</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">눈을 가진 AI 사진 분석</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">현장 시공 사진이나 제품 사진을 툭 올리세요. AI가 사진을 정밀 분석해 실제 경험담처럼 생생한 맞춤형 본문을 대리 창작합니다.</p>
            </div>

            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 02</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px; background: transparent; border: none; height: auto;">🎨 썸네일 메이커</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">자동 카드뉴스 썸네일</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">디자인을 전혀 몰라도 됩니다. 상호명과 키워드만 넣으면 트렌디한 파스텔톤 1:1 카드뉴스 대표 이미지를 즉석에서 완성합니다.</p>
            </div>

            <div class="guide-card" style="text-align: left; padding: 25px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-radius: 16px; word-break: keep-all;">
                <span class="step-number" style="display: inline-block; background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 30px; font-weight: 800; margin-bottom: 15px; font-size: 14px;">핵심 기술 03</span>
                <div class="img-placeholder" style="font-size: 2.5rem; margin-bottom: 15px; background: transparent; border: none; height: auto;">📢 고정 배너 광고</div>
                <h3 style="font-size: 1.25rem; color: #111827; margin-bottom: 15px; font-weight: 700; line-height: 1.4;">하단 고정 홍보 배너</h3>
                <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">매 포스팅 하단에 매장 연락처, 주소, 상담 링크 등 나만의 고정 홍보 문구를 깔끔한 구분선과 함께 자동으로 자동 부착해 드립니다.</p>
            </div>
        </div>
    </section>'''
content = re.sub(features_old_pattern, features_new, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated everything cleanly using regex.')
