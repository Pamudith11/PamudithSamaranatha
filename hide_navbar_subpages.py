import re
import os

def hide_navbar_subpages():
    base_dir = r'c:\Users\pamud\OneDrive\Desktop\PamudithSamaranatha-main'
    # Only sub-pages, keep Main Home page (service-teacher.html) as is
    sub_files = [
        'service-teacher-personal.html',
        'service-teacher-education.html',
        'service-teacher-philosophy.html',
        'service-teacher-programs.html',
        'service-teacher-gallery.html'
    ]
    
    for filename in sub_files:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove the <nav> block
        # Styles can stay, they won't affect anything if the HTML is gone.
        content = re.sub(r'<nav class="navbar.*?</nav>', '', content, flags=re.DOTALL)
        
        # Ensure there is a "Back to Home" button at the bottom
        # It usually is in <div class="back-btn-wrap"> ... </div>
        # Check if it exists, if acts correctly
        if 'href="service-teacher.html"' not in content:
             # Fix specific issue where it might point to index.html
             content = content.replace('href="index.html#services"', 'href="service-teacher.html"')
             content = content.replace('← Back to Main Site', '← Back to Home') # if that text was used
             
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Navbar removed from sub-pages.")

if __name__ == "__main__":
    hide_navbar_subpages()
