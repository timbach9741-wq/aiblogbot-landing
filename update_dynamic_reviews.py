import os
import re

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace the inner contents of scroll-up marquee-track
up_pattern = r'(<div class="marquee-col scroll-up">\s*<div class="marquee-track").*?(</div>\s*</div>)'
html_content = re.sub(up_pattern, r'\1 id="review-track-1">\2', html_content, flags=re.DOTALL)

# Replace the inner contents of scroll-down marquee-track
down_pattern = r'(<div class="marquee-col scroll-down">\s*<div class="marquee-track").*?(</div>\s*</div>)'
html_content = re.sub(down_pattern, r'\1 id="review-track-2">\2', html_content, flags=re.DOTALL)

# Now append the Javascript just before </body>
js_code = """
    <!-- 후기 동적 렌더링 스크립트 -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const reviewPool = [
                { avatar: '🍽️', name: '김*진 대표님', sub: '요식업 프랜차이즈', text: '타사 프로그램 쓰다 저품질 걸려 피눈물 흘렸는데, 이건 <span class="highlight-text">안전 임시저장</span> 방식이라 너무 안심됩니다. 대박이에요!' },
                { avatar: '💪', name: '이*훈 원장님', sub: '필라테스 스튜디오', text: '컴맹이라 걱정했는데 클릭 한 번이면 끝나네요ㅋㅋ AI가 매일 써주니까 <span class="highlight-text">퇴근 시간이 2시간</span> 빨라졌어요!!' },
                { avatar: '💼', name: '박*성 님', sub: '직장인 투잡', text: '뉴스픽 자동 포스팅으로 월 50만원 추가 수익 내고 있습니다. 진짜 <span class="highlight-text">돈 버는 기계</span>네요. 진작 살 걸 그랬어요.' },
                { avatar: '🛠️', name: '황*철 소장님', sub: '인테리어/설비', text: '공사 끝나고 지쳐서 블로그 쓸 엄두가 안 났는데, 현장 사진만 던져주면 알아서 글을 써주니 <span class="highlight-text">천국입니다</span>.' },
                { avatar: '💅', name: '이*미 원장님', sub: '네일아트 뷰티샵', text: '매일 밤마다 시술 사진 올리느라 손목이 아팠는데 이젠 알아서 척척! 파스텔 썸네일도 <span class="highlight-text">너무 예뻐요</span>.' },
                { avatar: '🚗', name: '최*호 대표님', sub: '중고차 매매', text: '매물 사진 10장 올리면 알아서 스펙 분석해서 글을 뽑아주네요. <span class="highlight-text">진짜 물건</span>입니다.' },
                { avatar: '✂️', name: '최*영 원장님', sub: '헤어 살롱', text: '매일 블로그 글쓰는 게 스트레스였는데 이제 완벽 해방입니다. 글 퀄리티가 <span class="highlight-text">제가 쓴 것보다 훨씬</span> 자연스러워요.' },
                { avatar: '🛒', name: '정*우 대표님', sub: '온라인 쇼핑몰', text: '쿠팡 파트너스 링크까지 알아서 척척 넣어주니까 너무 편합니다. 매출도 오르고 <span class="highlight-text">강력 추천</span>합니다!' },
                { avatar: '📈', name: '강*희 마케터', sub: '광고대행사', text: '대행사 직원들 야근이 절반으로 줄었습니다. 요일별 페르소나 기능 덕분에 <span class="highlight-text">원고 퀄리티가 압도적</span>입니다.' },
                { avatar: '🧘', name: '윤*아 강사님', sub: '요가 스튜디오', text: '요일별 페르소나 기능 덕분에 월수금은 꿀팁, 화목은 홍보글로 <span class="highlight-text">알아서 변신</span>! 너무 똑똑해요.' },
                { avatar: '⚖️', name: '장*혁 변호사', sub: '법률 사무소', text: '전문적인 내용도 제법 그럴싸하게 작성해 줍니다. 해시태그까지 <span class="highlight-text">자동 매칭</span>되니 상위노출 짱짱합니다.' },
                { avatar: '🐶', name: '오*진 사장님', sub: '애견 미용샵', text: '크롬 독립 세션 덕분에 본컴퓨터 작업과 안 겹치고 <span class="highlight-text">100% 무인 포스팅</span>이 돌아가서 신기합니다.' },
                { avatar: '🏠', name: '정*미 대표님', sub: '부동산 공인중개', text: '매물 사진 올리면 알아서 주변 상권까지 분석해서 써주네요. <span class="highlight-text">진짜 똑똑합니다</span>.' },
                { avatar: '🏋️', name: '김*태 관장님', sub: '대형 피트니스', text: '트레이너들 블로그 쓰라고 눈치 안 줘도 됩니다. 알아서 척척 쓰니 <span class="highlight-text">가성비 최고</span>네요.' },
                { avatar: '💐', name: '이*주 플로리스트', sub: '꽃집 운영', text: '꽃 사진만 올려도 감성적인 멘트를 줄줄 뽑아줘요! AI의 <span class="highlight-text">글솜씨에 반했습니다</span>.' },
                { avatar: '🧽', name: '송*민 대표님', sub: '출장 스팀세차', text: '밖에서 일하느라 피곤한데 폰으로 사진만 찍어두면 알아서 올라가니 <span class="highlight-text">완전 효자템</span>입니다.' },
                { avatar: '🩺', name: '조*현 원장님', sub: '피부과 의원', text: '전문 의학 용어도 제법 자연스럽게 녹여내는 걸 보고 놀랐습니다. 까다로운 심의규정도 지켜주어 <span class="highlight-text">대만족</span>입니다.' },
                { avatar: '🏕️', name: '백*호 사장님', sub: '풀빌라 펜션', text: '매일 똑같은 펜션 사진인데도 AI가 매번 다른 스토리텔링을 해주네요. 예약 문의가 <span class="highlight-text">30% 늘었습니다</span>.' },
                { avatar: '📦', name: '강*주 대표님', sub: '스마트스토어', text: '상품 사진 던져주면 알아서 소구점 파악해서 영업글을 써줍니다. 썸네일도 기가막혀 <span class="highlight-text">매출 떡상</span> 중!' },
                { avatar: '📚', name: '한*영 원장님', sub: '영어 보습학원', text: '학원 일상 사진 올리면 학부모님들 취향 저격하는 글로 변신합니다. <span class="highlight-text">원생 모집에 큰 도움</span>이 됩니다.' },
                { avatar: '🔨', name: '신*철 소장님', sub: '간판 시공업', text: '노가다 뛰고 글 쓸 힘이 어딨습니까. 사진 던지면 끝. 하루에 3개씩 포스팅하니 <span class="highlight-text">문의 폭주</span>합니다.' },
                { avatar: '☕', name: '류*진 사장님', sub: '감성 카페', text: '신메뉴 사진만 올려도 인스타 감성으로 블로그 글을 뚝딱! <span class="highlight-text">단골 손님</span>이 이거 보고 오셨대요.' }
            ];

            // 랜덤 섞기
            function shuffle(array) {
                for (let i = array.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }
                return array;
            }

            // 랜덤 "X분 전" 생성 (1분 ~ 59분)
            function getRandomTime() {
                return Math.floor(Math.random() * 59) + 1;
            }

            // 렌더링 함수
            function renderReviewHTML(review) {
                return `
                <div class="review-card">
                    <div class="rc-header">
                        <div class="rc-avatar">${review.avatar}</div>
                        <div class="rc-user">
                            <div class="rc-name">${review.name}</div>
                            <div class="rc-sub">${review.sub}</div>
                        </div>
                        <div class="rc-time">${getRandomTime()}분 전</div>
                    </div>
                    <div class="rc-stars">⭐⭐⭐⭐⭐</div>
                    <p class="rc-text">${review.text}</p>
                </div>`;
            }

            const shuffledReviews = shuffle([...reviewPool]);
            
            // Col 1 에는 0~6번 데이터 할당
            const col1Data = shuffledReviews.slice(0, 6);
            let col1HTML = col1Data.map(renderReviewHTML).join('');
            // 무한 스크롤 복제
            col1HTML += col1HTML;
            document.getElementById('review-track-1').innerHTML = col1HTML;

            // Col 2 에는 6~12번 데이터 할당
            const col2Data = shuffledReviews.slice(6, 12);
            let col2HTML = col2Data.map(renderReviewHTML).join('');
            // 무한 스크롤 복제
            col2HTML += col2HTML;
            document.getElementById('review-track-2').innerHTML = col2HTML;
        });
    </script>
</body>"""

html_content = html_content.replace('</body>', js_code)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Dynamic random reviews injected via JavaScript successfully.')
