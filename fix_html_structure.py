import os

html_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_marquee = """            <div class="review-marquee-container">
                <div class="marquee-mask-top"></div>
                <div class="marquee-mask-bottom"></div>
                
                <!-- Column 1 (Scrolls Up) -->
                <div class="marquee-col scroll-up">
                    <div class="marquee-track" id="review-track-1"></div>
                </div>

                <!-- Column 2 (Scrolls Down) -->
                <div class="marquee-col scroll-down">
                    <div class="marquee-track" id="review-track-2"></div>
                </div>
            </div>
"""

# Replace lines 41 to 337 inclusive with new_marquee
lines = lines[:41] + [new_marquee] + lines[338:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Restored HTML structure cleanly.')
