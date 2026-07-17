import os

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make all .btn-buy inside .pricing-grid open the modal
new_js = """
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

            // 추가: 가격표의 신청하기 버튼들 클릭 시에도 동일하게 모달 팝업 열기
            const priceBtns = document.querySelectorAll('.pricing-grid .btn-buy');
            priceBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    modal.style.display = 'flex';
                    formStep.style.display = 'block';
                    successStep.style.display = 'none';
                    appForm.reset();
                    industryOtherInput.style.display = 'none';
                    document.body.style.overflow = 'hidden'; 
                });
            });
"""

# Replace the specific openBtn logic chunk
old_js_pattern = """            if(openBtn) {
                openBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    modal.style.display = 'flex';
                    formStep.style.display = 'block';
                    successStep.style.display = 'none';
                    appForm.reset();
                    industryOtherInput.style.display = 'none';
                    document.body.style.overflow = 'hidden'; 
                });
            }"""

content = content.replace(old_js_pattern, new_js)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Linked pricing buttons to Modal successfully.")
