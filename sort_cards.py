import re
import datetime

def parse_date(text):
    # Regex for various formats
    
    # 2025.10.20 or 2025.9.9 or 2025/09/09
    match_ymd_dot = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', text)
    if match_ymd_dot:
        return datetime.datetime(int(match_ymd_dot.group(1)), int(match_ymd_dot.group(2)), int(match_ymd_dot.group(3)))

    # 2026 10 06 (Spaces)
    match_ymd_space = re.search(r'(\d{4})\s+(\d{1,2})\s+(\d{1,2})', text)
    if match_ymd_space:
        return datetime.datetime(int(match_ymd_space.group(1)), int(match_ymd_space.group(2)), int(match_ymd_space.group(3)))
        
    # Sinhala month names mapping
    sinhala_months = {
        'ජනවාරි': 1, 'පෙබරවාරි': 2, 'මාර්තු': 3, 'අප්‍රේල්': 4, 'මැයි': 5, 'ජුනි': 6,
        'ජූලි': 7, 'අගෝස්තු': 8, 'සැප්තැම්බර්': 9, 'ඔක්තොම්බර්': 10, 'නොවැම්බර්': 11, 'දෙසැම්බර්': 12
    }
    
    for month_name, month_num in sinhala_months.items():
        # 2024 ඔක්තොම්බර් මස 23
        pattern = r'(\d{4})\s*' + month_name + r'.*?(\d{1,2})'
        match_sinhala = re.search(pattern, text)
        if match_sinhala:
             return datetime.datetime(int(match_sinhala.group(1)), month_num, int(match_sinhala.group(2)))

    # Year only 2024
    match_year = re.search(r'20\d{2}', text)
    if match_year:
        # Default to Jan 1st if only year is found, but try to find month if possible
        return datetime.datetime(int(match_year.group(0)), 1, 1)

    return datetime.datetime(1900, 1, 1) # Default for no date

def sort_cards():
    file_path = r'c:\Users\pamud\OneDrive\Desktop\PamudithSamaranatha-main\service-teacher.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the gallery section
    gallery_start_marker = '<div class="gallery">'
    gallery_end_marker = '<div class="back-btn-wrap"' # Approximate end
    
    start_idx = content.find(gallery_start_marker)
    if start_idx == -1:
        print("Gallery not found")
        return

    # Find the closing div of gallery. It's risky to just look for </div>. 
    # Let's count divs or look for the specific structure.
    # The gallery ends before <div class="back-btn-wrap"
    
    end_idx = content.find(gallery_end_marker)
    if end_idx == -1:
         print("Gallery end not found")
         return
         
    # Adjust end_idx to include the closing </div> of the gallery
    # The `back-btn-wrap` is a sibling, so we need to find the last </div> before it.
    
    gallery_content_area = content[start_idx:end_idx]
    
    # We will split by <div class="img-box">
    # Note: This is a simple parser, assuming standard formatting in the file.
    
    cards = []
    
    # Regex to find all img-blocks
    # Non-greedy match for the div content
    card_pattern = re.compile(r'(<div class="img-box">.*?</div>)', re.DOTALL)
    
    found_cards = card_pattern.findall(gallery_content_area)
    
    print(f"Found {len(found_cards)} cards.")
    
    card_data = []
    for card_html in found_cards:
        # Extract text for date parsing
        clean_text = re.sub(r'<[^>]+>', ' ', card_html) # Remove tags
        date_obj = parse_date(clean_text)
        card_data.append({'html': card_html, 'date': date_obj})

    # Sort
    card_data.sort(key=lambda x: x['date'])
    
    # Reconstruct
    new_gallery_content = '\n\n      '.join([c['html'] for c in card_data])
    
    # Formatting
    new_gallery_html = f'{gallery_start_marker}\n\n      {new_gallery_content}\n\n    </div>\n    '
    
    # Replace in original content
    # We need to act carefully to replace exactly the gallery part.
    # The original gallery_content_area included everything from <div class="gallery"> up to the start of back-btn.
    # But card_pattern.findall might have missed whitespace between cards.
    
    # Let's verify what we are replacing.
    # We want to replace everything from `start_idx` to `end_idx` with `new_gallery_html + \n` basically.
    # However `end_idx` was start of `back-btn-wrap`. The `</div>` for gallery should be just before that.
    
    # Let's try to find the actual closing </div> of .gallery
    # It should be the last </div> before `back-btn-wrap`
    
    pre_footer = content[:end_idx]
    last_div_idx = pre_footer.rfind('</div>')
    
    if last_div_idx == -1: 
        print("Could not find closing div")
        return
        
    # Check if this </div> matches indentation or logic? 
    # Actually, looking at the file:
    # 526:     </div>
    # 527:     <div class="back-btn-wrap" style="margin-top: 40px;">
    
    # So `last_div_idx` should be the index of that `</div>` at line 526.
    
    # We will replace content[start_idx : last_div_idx + 6] with new_gallery_html
    
    final_html = content[:start_idx] + new_gallery_html + content[last_div_idx+6:] # +6 for </div> length
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Successfully sorted and saved.")

if __name__ == "__main__":
    sort_cards()
