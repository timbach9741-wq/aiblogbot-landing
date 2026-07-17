import os
import re

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Replace the license-info block with Trust Microcopy and Application CTA
old_license_block_pattern = r'<div class="license-info glass-card">.*?</div>\s*</div>\s*</section>'

new_cta_html = """
        <!-- Trust Microcopy -->
        <div class="trust-microcopy" style="text-align: center; margin-top: 30px; font-size: 16px; color: #475569; font-weight: 600; display: flex; flex-direction: column; gap: 10px;">
            <div><span style="color: #10b981; font-weight: 800; margin-right: 5px;">✅</span> 3일 무료체험 후 결제 결정 가능</div>
            <div><span style="color: #10b981; font-weight: 800; margin-right: 5px;">✅</span> 카카오톡으로 실제 담당자가 직접 안내</div>
            <div><span style="color: #10b981; font-weight: 800; margin-right: 5px;">✅</span> 설치·사용 중 문제 발생 시 1:1 지원</div>
        </div>

        <!-- Application CTA -->
        <div class="application-cta glass-card" style="margin-top: 40px; text-align: center; padding: 50px 30px; max-width: 800px; margin-left: auto; margin-right: auto;">
            <h3 style="font-size: 1.6rem; color: #1e293b; margin-bottom: 20px;">카드 결제, 계좌이체 등 편하신 방법으로 안내해드립니다.</h3>
            <p style="color: #64748b; font-size: 1.15rem; margin-bottom: 35px; line-height: 1.6;">아래 버튼을 눌러 몇 가지만 알려주시면, <br>가장 빠른 결제·설치 방법을 30분 내로 안내드릴게요.</p>
            <a href="#" id="open-app-modal" class="btn-primary" style="font-size: 1.3rem; padding: 20px 50px; display: inline-block;">신청하기</a>
            <p style="margin-top: 20px; font-size: 1rem; color: #94a3b8; font-weight: 500;">⏱️ 카카오톡 문의 기준 평균 30분 내 답변</p>
        </div>
        </div>
    </section>
"""

html_content = re.sub(old_license_block_pattern, new_cta_html, html_content, flags=re.DOTALL)

# 2. Inject Modal HTML before </body>
modal_html = """
    <!-- Application Modal -->
    <div id="application-modal" class="modal-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
        <div class="modal-content" style="background: white; border-radius: 20px; width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; padding: 40px; position: relative; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);">
            <button id="close-modal" style="position: absolute; top: 20px; right: 25px; background: none; border: none; font-size: 28px; cursor: pointer; color: #94a3b8; transition: color 0.2s;" onmouseover="this.style.color='#1e293b'" onmouseout="this.style.color='#94a3b8'">&times;</button>
            
            <!-- Form Step -->
            <div id="form-step">
                <h2 style="font-size: 1.8rem; font-weight: 800; color: #1e293b; margin-bottom: 10px; text-align: center;">신청서 작성</h2>
                <p style="text-align: center; color: #64748b; margin-bottom: 30px; font-size: 0.95rem;">간단한 정보만 남겨주시면 빠르게 안내해 드립니다.</p>
                
                <form id="app-form">
                    <!-- 1. 성함 / 상호명 -->
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label style="display: block; font-weight: 700; margin-bottom: 10px; color: #334155;">1. 성함 / 상호명 <span style="color: #ef4444;">*</span></label>
                        <input type="text" required placeholder="예. 홍길동 / OO미용실" style="width: 100%; padding: 15px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 1rem; outline: none; box-sizing: border-box; transition: border-color 0.3s;" onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#cbd5e1'">
                    </div>

                    <!-- 2. 연락 방법 -->
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label style="display: block; font-weight: 700; margin-bottom: 10px; color: #334155;">2. 연락 방법 <span style="color: #ef4444;">*</span></label>
                        <div style="display: flex; gap: 15px; margin-bottom: 12px; font-size: 0.95rem; color: #475569;">
                            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;"><input type="radio" name="contact_type" value="kakao" required> 카카오톡 ID</label>
                            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;"><input type="radio" name="contact_type" value="phone"> 전화번호</label>
                            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;"><input type="radio" name="contact_type" value="email"> 이메일</label>
                        </div>
                        <input type="text" required placeholder="선택하신 연락처를 입력해주세요" style="width: 100%; padding: 15px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 1rem; outline: none; box-sizing: border-box; transition: border-color 0.3s;" onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#cbd5e1'">
                    </div>

                    <!-- 3. 업종 -->
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label style="display: block; font-weight: 700; margin-bottom: 10px; color: #334155;">3. 업종을 알려주세요 <span style="color: #ef4444;">*</span></label>
                        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px; font-size: 0.95rem; color: #475569;">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="industry" value="인테리어/시공" required> 인테리어/시공</label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="industry" value="청소대행/입주청소"> 청소대행/입주청소</label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="industry" value="미용/네일/헤어"> 미용/네일/헤어</label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="industry" id="industry-other-radio" value="기타"> 기타 (직접 입력)</label>
                        </div>
                        <input type="text" id="industry-other-input" placeholder="기타 업종 입력" style="display: none; width: 100%; padding: 15px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 1rem; outline: none; box-sizing: border-box; transition: border-color 0.3s;" onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#cbd5e1'">
                    </div>

                    <!-- 4. 결제 방법 -->
                    <div class="form-group" style="margin-bottom: 25px;">
                        <label style="display: block; font-weight: 700; margin-bottom: 10px; color: #334155;">4. 선호하시는 결제 방법 <span style="color: #ef4444;">*</span></label>
                        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.95rem; color: #475569;">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="payment" value="카드 결제" required> 카드 결제 (크몽 경유 안내)</label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="payment" value="계좌이체"> 계좌이체</label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;"><input type="radio" name="payment" value="미정"> 아직 잘 모르겠음, 상담 후 결정</label>
                        </div>
                    </div>

                    <!-- 5. 질문 -->
                    <div class="form-group" style="margin-bottom: 35px;">
                        <label style="display: block; font-weight: 700; margin-bottom: 10px; color: #334155;">5. (선택) 가장 궁금하신 점이 있다면 남겨주세요</label>
                        <textarea placeholder="자유롭게 작성해주세요" rows="3" style="width: 100%; padding: 15px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 1rem; outline: none; box-sizing: border-box; resize: vertical; transition: border-color 0.3s;" onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#cbd5e1'"></textarea>
                    </div>

                    <button type="submit" class="btn-primary" style="width: 100%; font-size: 1.2rem; padding: 18px; border: none; cursor: pointer; border-radius: 30px;">제출하고 안내받기</button>
                </form>
            </div>

            <!-- Success Step -->
            <div id="success-step" style="display: none; text-align: center; padding: 30px 10px;">
                <div style="font-size: 70px; margin-bottom: 20px;">🎉</div>
                <h2 style="font-size: 2rem; font-weight: 800; color: #1e293b; margin-bottom: 15px;">신청이 완료되었습니다!</h2>
                <p style="color: #475569; font-size: 1.15rem; line-height: 1.6; margin-bottom: 35px;">
                    감사합니다! 남겨주신 연락처로 <strong>30분 내에</strong><br>결제 방법과 설치 가이드를 안내해드릴게요.
                </p>
                <div style="background: #f8fafc; border-radius: 15px; padding: 30px; margin-bottom: 30px;">
                    <p style="color: #64748b; font-size: 1.05rem; margin-bottom: 20px;">급하신 경우 카카오톡 채널로 문의 주시면<br>더 빠르게 도와드립니다.</p>
                    <a href="#" class="btn-kakao" style="display: inline-block; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold;">💬 카카오톡 바로가기</a>
                </div>
                <button id="close-success" style="background: none; border: none; color: #94a3b8; font-size: 1.1rem; cursor: pointer; text-decoration: underline;">닫기</button>
            </div>

        </div>
    </div>

    <!-- Modal Form Script -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('application-modal');
            const openBtn = document.getElementById('open-app-modal');
            const closeBtn = document.getElementById('close-modal');
            const closeSuccessBtn = document.getElementById('close-success');
            const formStep = document.getElementById('form-step');
            const successStep = document.getElementById('success-step');
            const appForm = document.getElementById('app-form');

            const industryRadios = document.querySelectorAll('input[name="industry"]');
            const industryOtherInput = document.getElementById('industry-other-input');
            
            industryRadios.forEach(radio => {
                radio.addEventListener('change', (e) => {
                    if (e.target.value === '기타') {
                        industryOtherInput.style.display = 'block';
                        industryOtherInput.required = true;
                    } else {
                        industryOtherInput.style.display = 'none';
                        industryOtherInput.required = false;
                    }
                });
            });

            if(openBtn) {
                openBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    modal.style.display = 'flex';
                    formStep.style.display = 'block';
                    successStep.style.display = 'none';
                    appForm.reset();
                    industryOtherInput.style.display = 'none';
                    document.body.style.overflow = 'hidden'; 
                });
            }

            const closeModal = () => {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            };

            if(closeBtn) closeBtn.addEventListener('click', closeModal);
            if(closeSuccessBtn) closeSuccessBtn.addEventListener('click', closeModal);
            
            modal.addEventListener('click', (e) => {
                if (e.target === modal) closeModal();
            });

            appForm.addEventListener('submit', (e) => {
                e.preventDefault();
                // UI 전환 애니메이션
                formStep.style.opacity = '0';
                setTimeout(() => {
                    formStep.style.display = 'none';
                    successStep.style.display = 'block';
                    successStep.style.opacity = '0';
                    setTimeout(() => {
                        formStep.style.opacity = '1';
                        successStep.style.transition = 'opacity 0.4s ease';
                        successStep.style.opacity = '1';
                    }, 50);
                }, 300);
            });
        });
    </script>
</body>"""

html_content = html_content.replace('</body>', modal_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Injected new Form UI and scripts successfully.')
