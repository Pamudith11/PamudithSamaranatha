import re
import os

def redesign_navbar():
    base_dir = r'c:\Users\pamud\OneDrive\Desktop\PamudithSamaranatha-main'
    files = [
        'service-teacher.html',
        'service-teacher-personal.html',
        'service-teacher-education.html',
        'service-teacher-philosophy.html',
        'service-teacher-programs.html',
        'service-teacher-gallery.html'
    ]
    
    # 1. New Menu HTML for service-teacher.html (Home)
    # We will insert this AFTER the intro text/profile section and BEFORE the footer/scripts.
    # Actually, the original 'service-teacher.html' had all sections. Now it only has Home section.
    # We need to insert the menu there.
    
    dashboard_menu_html = """
    <section id="dashboard-menu" class="container reveal">
        <h2 class="section-title">Explore My Portfolio</h2>
        <div class="services-grid" style="max-width: 1000px; margin: 0 auto;">
            
            <a href="service-teacher-personal.html" class="service-card" style="text-decoration: none;">
                <div style="padding: 30px; text-align: center;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Personal Details</h3>
                    <p>Biography, Family, and Contact Info</p>
                </div>
            </a>

            <a href="service-teacher-education.html" class="service-card" style="text-decoration: none;">
               <div style="padding: 30px; text-align: center;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Educational Qualifications</h3>
                    <p>Schools, Degrees, and Diplomas</p>
                </div>
            </a>

            <a href="service-teacher-philosophy.html" class="service-card" style="text-decoration: none;">
               <div style="padding: 30px; text-align: center;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Work Philosophy</h3>
                    <p>My Vision and Mission as a Teacher</p>
                </div>
            </a>

            <a href="service-teacher-programs.html" class="service-card" style="text-decoration: none;">
               <div style="padding: 30px; text-align: center;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">College Programmes</h3>
                    <p>Contributions to College Events</p>
                </div>
            </a>

            <a href="service-teacher-gallery.html" class="service-card" style="text-decoration: none; grid-column: 1 / -1;">
               <div style="padding: 30px; text-align: center;">
                    <h3 style="font-size: 1.8rem; margin-bottom: 10px;">Photo Gallery</h3>
                    <p>Societies, Extra-curricular, and Events</p>
                </div>
            </a>

        </div>
        <div class="back-btn-wrap" style="margin-top: 50px;">
           <a href="index.html#services" class="accent-btn">← Back to Main Site</a>
         </div>
    </section>
    """
    
    # Floating Home Button for Sub-pages
    home_button_html = """
    <a href="service-teacher.html" style="
        position: fixed;
        top: 20px;
        left: 20px;
        background: rgba(0, 0, 0, 0.6);
        color: var(--accent);
        padding: 10px 15px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        border: 1px solid var(--accent);
        z-index: 2000;
        backdrop-filter: blur(5px);
        box-shadow: 0 0 10px rgba(0,255,242,0.2);
        transition: all 0.3s ease;
    " onmouseover="this.style.background='var(--accent)'; this.style.color='#000';" onmouseout="this.style.background='rgba(0, 0, 0, 0.6)'; this.style.color='var(--accent)';">
        ← Home
    </a>
    """

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Remove Navbar
        # Regex to remove <nav class="navbar">...</nav>
        content = re.sub(r'<nav class="navbar">.*?</nav>', '', content, flags=re.DOTALL)
        
        # 2. Add specific content based on file
        if filename == 'service-teacher.html':
            # Add Dashboard Menu at the end of content, before body close
            # But inside the container or new section?
            # Existing structure: ... </section> <script> ...
            # Let's insert before <script>
            if ' Explore My Portfolio' not in content: # Avoid duplication if run twice
                 content = content.replace('<script>', f'{dashboard_menu_html}\n<script>')
        else:
            # Sub-pages: Add Floating Home Button
            # Insert after <body>
            if '← Home' not in content:
                content = content.replace('<body>', f'<body>\n{home_button_html}')
            
            # Ensure bottom back button points to Home (service-teacher.html) not index.html
            # The split script might have left "index.html#services"
            content = content.replace('href="index.html#services"', 'href="service-teacher.html"')
            content = content.replace('← Back to Services', '← Back to Menu')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Navigation redesigned successfully.")

if __name__ == "__main__":
    redesign_navbar()
