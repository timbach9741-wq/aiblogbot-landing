import os
import re

css_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

css_content = re.sub(r'(\.review-marquee-container\s*{[^}]*height:\s*)520px', r'\g<1>650px', css_content)
css_content = re.sub(r'(animation:\s*scroll-up\s*)25s', r'\g<1>40s', css_content)
css_content = re.sub(r'(animation:\s*scroll-down\s*)25s', r'\g<1>40s', css_content)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

new_marquee = '''<div class="review-marquee-container">
                <div class="marquee-mask-top"></div>
                <div class="marquee-mask-bottom"></div>
                
                <!-- Column 1 (Scrolls Up) -->
                <div class="marquee-col scroll-up">
                    <div class="marquee-track">
                        <!-- Unique Set Col 1 -->
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🍽️</div>
                                <div class="rc-user">
                                    <div class="rc-name">김*진 대표님</div>
                                    <div class="rc-sub">요식업 프랜차이즈</div>
                                </div>
                                <div class="rc-time">21분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">타사 프로그램 쓰다 저품질 걸려 피눈물 흘렸는데, 이건 <span class="highlight-text">안전 임시저장</span> 방식이라 너무 안심됩니다. 대박이에요!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💪</div>
                                <div class="rc-user">
                                    <div class="rc-name">이*훈 원장님</div>
                                    <div class="rc-sub">필라테스 스튜디오</div>
                                </div>
                                <div class="rc-time">4분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">컴맹이라 걱정했는데 클릭 한 번이면 끝나네요ㅋㅋ AI가 매일 써주니까 <span class="highlight-text">퇴근 시간이 2시간</span> 빨라졌어요!!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💼</div>
                                <div class="rc-user">
                                    <div class="rc-name">박*성 님</div>
                                    <div class="rc-sub">직장인 투잡</div>
                                </div>
                                <div class="rc-time">15분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">뉴스픽 자동 포스팅으로 월 50만원 추가 수익 내고 있습니다. 진짜 <span class="highlight-text">돈 버는 기계</span>네요. 진작 살 걸 그랬어요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🛠️</div>
                                <div class="rc-user">
                                    <div class="rc-name">황*철 소장님</div>
                                    <div class="rc-sub">인테리어/설비</div>
                                </div>
                                <div class="rc-time">41분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">공사 끝나고 지쳐서 블로그 쓸 엄두가 안 났는데, 현장 사진만 던져주면 알아서 글을 써주니 <span class="highlight-text">천국입니다</span>.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💅</div>
                                <div class="rc-user">
                                    <div class="rc-name">이*미 원장님</div>
                                    <div class="rc-sub">네일아트 뷰티샵</div>
                                </div>
                                <div class="rc-time">1시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매일 밤마다 시술 사진 올리느라 손목이 아팠는데 이젠 알아서 척척! 파스텔 썸네일도 <span class="highlight-text">너무 예뻐요</span>.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🚗</div>
                                <div class="rc-user">
                                    <div class="rc-name">최*호 대표님</div>
                                    <div class="rc-sub">중고차 매매</div>
                                </div>
                                <div class="rc-time">3시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매물 사진 10장 올리면 알아서 스펙 분석해서 글을 뽑아주네요. <span class="highlight-text">진짜 물건</span>입니다.</p>
                        </div>

                        <!-- Duplicated Set Col 1 for Infinite Scroll -->
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🍽️</div>
                                <div class="rc-user">
                                    <div class="rc-name">김*진 대표님</div>
                                    <div class="rc-sub">요식업 프랜차이즈</div>
                                </div>
                                <div class="rc-time">21분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">타사 프로그램 쓰다 저품질 걸려 피눈물 흘렸는데, 이건 <span class="highlight-text">안전 임시저장</span> 방식이라 너무 안심됩니다. 대박이에요!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💪</div>
                                <div class="rc-user">
                                    <div class="rc-name">이*훈 원장님</div>
                                    <div class="rc-sub">필라테스 스튜디오</div>
                                </div>
                                <div class="rc-time">4분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">컴맹이라 걱정했는데 클릭 한 번이면 끝나네요ㅋㅋ AI가 매일 써주니까 <span class="highlight-text">퇴근 시간이 2시간</span> 빨라졌어요!!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💼</div>
                                <div class="rc-user">
                                    <div class="rc-name">박*성 님</div>
                                    <div class="rc-sub">직장인 투잡</div>
                                </div>
                                <div class="rc-time">15분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">뉴스픽 자동 포스팅으로 월 50만원 추가 수익 내고 있습니다. 진짜 <span class="highlight-text">돈 버는 기계</span>네요. 진작 살 걸 그랬어요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🛠️</div>
                                <div class="rc-user">
                                    <div class="rc-name">황*철 소장님</div>
                                    <div class="rc-sub">인테리어/설비</div>
                                </div>
                                <div class="rc-time">41분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">공사 끝나고 지쳐서 블로그 쓸 엄두가 안 났는데, 현장 사진만 던져주면 알아서 글을 써주니 <span class="highlight-text">천국입니다</span>.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">💅</div>
                                <div class="rc-user">
                                    <div class="rc-name">이*미 원장님</div>
                                    <div class="rc-sub">네일아트 뷰티샵</div>
                                </div>
                                <div class="rc-time">1시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매일 밤마다 시술 사진 올리느라 손목이 아팠는데 이젠 알아서 척척! 파스텔 썸네일도 <span class="highlight-text">너무 예뻐요</span>.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🚗</div>
                                <div class="rc-user">
                                    <div class="rc-name">최*호 대표님</div>
                                    <div class="rc-sub">중고차 매매</div>
                                </div>
                                <div class="rc-time">3시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매물 사진 10장 올리면 알아서 스펙 분석해서 글을 뽑아주네요. <span class="highlight-text">진짜 물건</span>입니다.</p>
                        </div>
                    </div>
                </div>

                <!-- Column 2 (Scrolls Down) -->
                <div class="marquee-col scroll-down">
                    <div class="marquee-track">
                        <!-- Unique Set Col 2 -->
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">✂️</div>
                                <div class="rc-user">
                                    <div class="rc-name">최*영 원장님</div>
                                    <div class="rc-sub">헤어 살롱</div>
                                </div>
                                <div class="rc-time">32분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매일 블로그 글쓰는 게 스트레스였는데 이제 완벽 해방입니다. 글 퀄리티가 <span class="highlight-text">제가 쓴 것보다 훨씬</span> 자연스러워요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🛒</div>
                                <div class="rc-user">
                                    <div class="rc-name">정*우 대표님</div>
                                    <div class="rc-sub">온라인 쇼핑몰</div>
                                </div>
                                <div class="rc-time">3분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">쿠팡 파트너스 링크까지 알아서 척척 넣어주니까 너무 편합니다. 매출도 오르고 <span class="highlight-text">강력 추천</span>합니다!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">📈</div>
                                <div class="rc-user">
                                    <div class="rc-name">강*희 마케터</div>
                                    <div class="rc-sub">광고대행사</div>
                                </div>
                                <div class="rc-time">17분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">대행사 직원들 야근이 절반으로 줄었습니다. 요일별 페르소나 기능 덕분에 <span class="highlight-text">원고 퀄리티가 압도적</span>입니다.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🧘</div>
                                <div class="rc-user">
                                    <div class="rc-name">윤*아 강사님</div>
                                    <div class="rc-sub">요가 스튜디오</div>
                                </div>
                                <div class="rc-time">55분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">요일별 페르소나 기능 덕분에 월수금은 꿀팁, 화목은 홍보글로 <span class="highlight-text">알아서 변신</span>! 너무 똑똑해요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">⚖️</div>
                                <div class="rc-user">
                                    <div class="rc-name">장*혁 변호사</div>
                                    <div class="rc-sub">법률 사무소</div>
                                </div>
                                <div class="rc-time">2시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">전문적인 내용도 제법 그럴싸하게 작성해 줍니다. 해시태그까지 <span class="highlight-text">자동 매칭</span>되니 상위노출 짱짱합니다.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🐶</div>
                                <div class="rc-user">
                                    <div class="rc-name">오*진 사장님</div>
                                    <div class="rc-sub">애견 미용샵</div>
                                </div>
                                <div class="rc-time">4시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">크롬 독립 세션 덕분에 본컴퓨터 작업과 안 겹치고 <span class="highlight-text">100% 무인 포스팅</span>이 돌아가서 신기합니다.</p>
                        </div>

                        <!-- Duplicated Set Col 2 for Infinite Scroll -->
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">✂️</div>
                                <div class="rc-user">
                                    <div class="rc-name">최*영 원장님</div>
                                    <div class="rc-sub">헤어 살롱</div>
                                </div>
                                <div class="rc-time">32분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">매일 블로그 글쓰는 게 스트레스였는데 이제 완벽 해방입니다. 글 퀄리티가 <span class="highlight-text">제가 쓴 것보다 훨씬</span> 자연스러워요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🛒</div>
                                <div class="rc-user">
                                    <div class="rc-name">정*우 대표님</div>
                                    <div class="rc-sub">온라인 쇼핑몰</div>
                                </div>
                                <div class="rc-time">3분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">쿠팡 파트너스 링크까지 알아서 척척 넣어주니까 너무 편합니다. 매출도 오르고 <span class="highlight-text">강력 추천</span>합니다!</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">📈</div>
                                <div class="rc-user">
                                    <div class="rc-name">강*희 마케터</div>
                                    <div class="rc-sub">광고대행사</div>
                                </div>
                                <div class="rc-time">17분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">대행사 직원들 야근이 절반으로 줄었습니다. 요일별 페르소나 기능 덕분에 <span class="highlight-text">원고 퀄리티가 압도적</span>입니다.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🧘</div>
                                <div class="rc-user">
                                    <div class="rc-name">윤*아 강사님</div>
                                    <div class="rc-sub">요가 스튜디오</div>
                                </div>
                                <div class="rc-time">55분 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">요일별 페르소나 기능 덕분에 월수금은 꿀팁, 화목은 홍보글로 <span class="highlight-text">알아서 변신</span>! 너무 똑똑해요.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">⚖️</div>
                                <div class="rc-user">
                                    <div class="rc-name">장*혁 변호사</div>
                                    <div class="rc-sub">법률 사무소</div>
                                </div>
                                <div class="rc-time">2시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">전문적인 내용도 제법 그럴싸하게 작성해 줍니다. 해시태그까지 <span class="highlight-text">자동 매칭</span>되니 상위노출 짱짱합니다.</p>
                        </div>
                        <div class="review-card">
                            <div class="rc-header">
                                <div class="rc-avatar">🐶</div>
                                <div class="rc-user">
                                    <div class="rc-name">오*진 사장님</div>
                                    <div class="rc-sub">애견 미용샵</div>
                                </div>
                                <div class="rc-time">4시간 전</div>
                            </div>
                            <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                            <p class="rc-text">크롬 독립 세션 덕분에 본컴퓨터 작업과 안 겹치고 <span class="highlight-text">100% 무인 포스팅</span>이 돌아가서 신기합니다.</p>
                        </div>
                    </div>
                </div>
            </div>'''

old_pattern = r'<div class="review-marquee-container">.*?</div>\s*</div>\s*</div>'
html_content = re.sub(old_pattern, new_marquee, html_content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Updated reviews and styles successfully.')
