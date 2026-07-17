import os
import re

css_path = r'C:\Users\PC\Desktop\AIBlogBot_홈페이지\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# 1. Update .features to grid
css_content = re.sub(
    r'\.features\s*\{[^}]*\}',
    '''.features {
    list-style: none;
    padding: 0;
    margin: 0 0 40px 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}''',
    css_content
)

# 2. Update .features li font-size to 14px or 15px so it fits well in grid
css_content = re.sub(
    r'(\.features\s*li\s*\{[^}]*font-size:\s*)16px',
    r'\g<1>14.5px',
    css_content
)

# 3. Update .hero-content max-width
css_content = re.sub(
    r'(\.hero-content\s*\{[^}]*max-width:\s*)600px',
    r'\g<1>780px',
    css_content
)

# 4. Update .hero-image to center to close the gap
css_content = re.sub(
    r'(\.hero-image\s*\{[^}]*justify-content:\s*)flex-end',
    r'\g<1>flex-start',
    css_content
)
# Add padding-left to hero-image to act as a controlled gap
css_content = re.sub(
    r'(\.hero-image\s*\{[^}]*position:\s*relative;)',
    r'\g<1>\n    padding-left: 20px;',
    css_content
)

# 5. Decrease marquee height since left side is shorter
css_content = re.sub(
    r'(\.review-marquee-container\s*\{[^}]*height:\s*)650px',
    r'\g<1>560px',
    css_content
)

# 6. Change hero gap just in case
css_content = re.sub(
    r'(\.hero\s*\{[^}]*align-items:\s*center;)',
    r'\g<1>\n    gap: 40px;',
    css_content
)


with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print('Updated layout gaps and columns successfully.')
