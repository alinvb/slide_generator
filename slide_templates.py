"""
Professional slide_templates.py with full-featured renderers
These create actual charts, tables, and sophisticated layouts
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from datetime import datetime

# Removed circular import - _apply_standard_header_and_title is now defined locally


def get_brand_styling(brand_config=None, color_scheme=None, typography=None):
    """Extract brand styling or use defaults - FIXED VERSION"""
    print(f"[DEBUG] get_brand_styling called with brand_config: {brand_config is not None}")
    
    if brand_config:
        print(f"[DEBUG] Brand config keys: {list(brand_config.keys())}")
        brand_colors = brand_config.get('color_scheme', {})
        brand_fonts = brand_config.get('typography', {})
        
        print(f"[DEBUG] Brand colors keys: {list(brand_colors.keys())}")
        print(f"[DEBUG] Brand fonts keys: {list(brand_fonts.keys())}")
        
        # Handle different color formats - IMPROVED CONVERSION
        colors = {}
        color_defaults = {
            "primary": RGBColor(24, 58, 88),
            "secondary": RGBColor(181, 151, 91),
            "accent": RGBColor(64, 64, 64),
            "text": RGBColor(64, 64, 64),
            "background": RGBColor(255, 255, 255),
            "light_grey": RGBColor(240, 240, 240),
            "footer_grey": RGBColor(128, 128, 128)
        }
        
        for key, default_color in color_defaults.items():
            if key in brand_colors:
                brand_color = brand_colors[key]
                print(f"[DEBUG] Processing color {key}: {brand_color} (type: {type(brand_color)})")
                
                # Handle different color formats
                if hasattr(brand_color, 'r') and hasattr(brand_color, 'g') and hasattr(brand_color, 'b'):
                    # Already an RGBColor object
                    colors[key] = brand_color
                    print(f"[DEBUG] Using RGBColor: {key} = RGB({brand_color.r}, {brand_color.g}, {brand_color.b})")
                elif isinstance(brand_color, tuple) and len(brand_color) == 3:
                    # Tuple format (r, g, b)
                    colors[key] = RGBColor(*brand_color)
                    print(f"[DEBUG] Converted tuple to RGBColor: {key} = {brand_color}")
                elif isinstance(brand_color, str) and brand_color.startswith('#'):
                    # Hex format #RRGGBB
                    hex_color = brand_color.lstrip('#')
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16) 
                    b = int(hex_color[4:6], 16)
                    colors[key] = RGBColor(r, g, b)
                    print(f"[DEBUG] Converted hex to RGBColor: {key} = {brand_color} -> RGB({r}, {g}, {b})")
                else:
                    print(f"[DEBUG] Unknown color format for {key}: {brand_color}, using default")
                    colors[key] = default_color
            else:
                colors[key] = default_color
        
        # Handle fonts with better error handling
        font_defaults = {
            "primary_font": 'Arial',
            "title_size": Pt(24),
            "header_size": Pt(14),
            "body_size": Pt(11),
            "small_size": Pt(9)
        }
        
        fonts = {}
        for key, default_value in font_defaults.items():
            if key in brand_fonts:
                brand_value = brand_fonts[key]
                print(f"[DEBUG] Processing font {key}: {brand_value} (type: {type(brand_value)})")
                
                if key == "primary_font":
                    fonts[key] = str(brand_value)
                else:
                    # Handle font sizes
                    if hasattr(brand_value, 'pt'):
                        # Already a Pt object
                        fonts[key] = brand_value
                    elif isinstance(brand_value, (int, float)):
                        # Convert number to Pt
                        fonts[key] = Pt(int(brand_value))
                    else:
                        print(f"[DEBUG] Unknown font size format for {key}: {brand_value}, using default")
                        fonts[key] = default_value
            else:
                fonts[key] = default_value
        
        print(f"[DEBUG] Final colors: primary=RGB({colors['primary'].r},{colors['primary'].g},{colors['primary'].b})")
        print(f"[DEBUG] Final fonts: {fonts['primary_font']}, title={fonts['title_size']}")
        
    else:
        print("[DEBUG] No brand_config, using defaults")
        # Use passed parameters or defaults
        colors = color_scheme or {
            "primary": RGBColor(24, 58, 88),
            "secondary": RGBColor(181, 151, 91),
            "accent": RGBColor(64, 64, 64),
            "text": RGBColor(64, 64, 64),
            "background": RGBColor(255, 255, 255),
            "light_grey": RGBColor(240, 240, 240),
            "footer_grey": RGBColor(128, 128, 128)
        }
        
        fonts = typography or {
            "primary_font": 'Arial',
            "title_size": Pt(24),
            "header_size": Pt(14),
            "body_size": Pt(11),
            "small_size": Pt(9)
        }
    
    return colors, fonts


def _apply_standard_header_and_title(slide, title_text, brand_config=None, company_name="Moelis"):
    """Apply standardized header and title formatting to a slide"""
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config)
    
    # Add title with clean header style
    title_left = Inches(0.5)
    title_top = Inches(0.3)
    title_width = Inches(12.333)
    title_height = Inches(0.8)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_frame = title_box.text_frame
    title_frame.margin_left = 0
    title_frame.margin_top = 0
    title_frame.margin_right = 0
    title_frame.margin_bottom = 0
    
    title_p = title_frame.paragraphs[0]
    title_p.text = title_text
    title_p.alignment = PP_ALIGN.LEFT
    
    title_run = title_p.runs[0]
    title_run.font.name = fonts["primary_font"]
    title_run.font.size = fonts["title_size"]
    title_run.font.bold = True
    title_run.font.color.rgb = colors["primary"]
    
    # Add blue underline
    underline_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        title_left, Inches(1.0), title_width, Inches(0.05)
    )
    underline_shape.fill.solid()
    underline_shape.fill.fore_color.rgb = colors["primary"]
    underline_shape.line.fill.background()


def get_brand_styling(brand_config=None, color_scheme=None, typography=None):
    """Extract brand styling or use defaults - reusable across all functions"""
    if brand_config:
        brand_colors = brand_config.get('color_scheme', {})
        brand_fonts = brand_config.get('typography', {})
        
        colors = {
            "primary": brand_colors.get('primary', RGBColor(24, 58, 88)),
            "secondary": brand_colors.get('secondary', RGBColor(181, 151, 91)),
            "accent": brand_colors.get('accent', RGBColor(64, 64, 64)),
            "text": brand_colors.get('text', RGBColor(64, 64, 64)),
            "background": brand_colors.get('background', RGBColor(255, 255, 255)),
            "light_grey": brand_colors.get('light_grey', RGBColor(240, 240, 240)),
            "footer_grey": RGBColor(128, 128, 128)
        }
        
        fonts = {
            "primary_font": brand_fonts.get('primary_font', 'Arial'),
            "title_size": Pt(brand_fonts.get('title_size', 24)),
            "header_size": Pt(brand_fonts.get('header_size', 14)),
            "body_size": Pt(brand_fonts.get('body_size', 11)),
            "small_size": Pt(brand_fonts.get('small_size', 9))
        }
    else:
        # Use passed parameters or defaults
        colors = color_scheme or {
            "primary": RGBColor(24, 58, 88),
            "secondary": RGBColor(181, 151, 91),
            "accent": RGBColor(64, 64, 64),
            "text": RGBColor(64, 64, 64),
            "background": RGBColor(255, 255, 255),
            "light_grey": RGBColor(240, 240, 240),
            "footer_grey": RGBColor(128, 128, 128)
        }
        
        fonts = typography or {
            "primary_font": 'Arial',
            "title_size": Pt(24),
            "header_size": Pt(14),
            "body_size": Pt(11),
            "small_size": Pt(9)
        }
    
    return colors, fonts


def ensure_prs(prs=None):
    """Return a 16:9 Presentation object without isinstance() pitfalls."""
    from pptx.util import Inches
    # If it's already presentation-like, just return
    try:
        if prs is not None and hasattr(prs, "slides") and hasattr(prs, "slide_width"):
            try:
                prs.slide_width = Inches(13.333)
                prs.slide_height = Inches(7.5)
            except Exception:
                pass
            return prs
    except Exception:
        pass

    # If it's a path, try opening
    try:
        if isinstance(prs, (str, bytes)) or getattr(prs, "__fspath__", None):
            from pptx import Presentation as _PresentationFactory
            prs_obj = _PresentationFactory(prs)
        else:
            from pptx import Presentation as _PresentationFactory
            prs_obj = _PresentationFactory()
    except Exception:
        from pptx import Presentation as _PresentationFactory
        prs_obj = _PresentationFactory()

    # 16:9
    try:
        prs_obj.slide_width = Inches(13.333)
        prs_obj.slide_height = Inches(7.5)
    except Exception:
        pass
    return prs_obj


def render_management_team_slide(data=None, color_scheme=None, typography=None, company_name="Your Company", prs=None, brand_config=None, **kwargs):
    """
    Renders a sophisticated management team slide with brand configuration support
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # STANDARDIZED: Apply header and title
    title_text = (data or {}).get('title', 'Senior Management Team')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Function to add management profiles
    def add_management_profile(x_pos, y_pos, width, profile_data):
        # Role title
        title_box = slide.shapes.add_textbox(x_pos, y_pos, width, Inches(0.3))
        title_frame = title_box.text_frame
        title_frame.clear()
        p = title_frame.paragraphs[0]
        p.text = profile_data.get('role_title', 'Role Title')
        p.font.name = fonts["primary_font"]          # BRAND FONT
        p.font.size = fonts["header_size"]           # BRAND SIZE
        p.font.color.rgb = colors["primary"]         # BRAND COLOR
        p.font.bold = True
        
        # Experience bullets
        current_y = y_pos + Inches(0.35)
        experience_bullets = profile_data.get('experience_bullets', [])
        for bullet in experience_bullets:
            bullet_box = slide.shapes.add_textbox(x_pos, current_y, width, Inches(0.6))
            bullet_frame = bullet_box.text_frame
            bullet_frame.clear()
            p = bullet_frame.paragraphs[0]
            p.text = f"• {bullet}"
            p.font.name = fonts["primary_font"]      # BRAND FONT
            p.font.size = fonts["body_size"]         # BRAND SIZE
            p.font.color.rgb = colors["text"]        # BRAND COLOR
            bullet_frame.word_wrap = True
            current_y += Inches(0.5)
        
        return current_y
    
    # Add left column profiles
    current_y = Inches(1.5)
    left_profiles = (data or {}).get('left_column_profiles', [])
    for profile in left_profiles:
        current_y = add_management_profile(Inches(0.5), current_y, Inches(6), profile)
        current_y += Inches(0.2)
    
    # Add right column profiles  
    current_y = Inches(1.5)
    right_profiles = (data or {}).get('right_column_profiles', [])
    for profile in right_profiles:
        current_y = add_management_profile(Inches(7), current_y, Inches(5.8), profile)
        current_y += Inches(0.2)
    
    # Footer
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]              # BRAND FONT
    p.font.size = fonts["small_size"]                # BRAND SIZE
    p.font.color.rgb = colors["footer_grey"]         # BRAND COLOR
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(7.0), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name if company_name and company_name.strip() else "Moelis"
    p.font.name = fonts["primary_font"]              # BRAND FONT
    p.font.size = fonts["small_size"]                # BRAND SIZE
    p.font.color.rgb = colors["footer_grey"]         # BRAND COLOR
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_investor_considerations_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders an investor considerations slide with two-column layout (Considerations vs Mitigants)
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # STANDARDIZED: Apply header and title
    title_text = (data or {}).get('title', 'Investor Considerations & Mitigating Factors')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Add column headers
    # Considerations header
    cons_header = slide.shapes.add_textbox(Inches(1), Inches(1.4), Inches(5.5), Inches(0.5))
    cons_frame = cons_header.text_frame
    cons_frame.clear()
    p = cons_frame.paragraphs[0]
    p.text = "Considerations"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["body_size"]
    p.font.color.rgb = colors["primary"]
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    
    # Mitigants header
    mit_header = slide.shapes.add_textbox(Inches(7), Inches(1.4), Inches(5.5), Inches(0.5))
    mit_frame = mit_header.text_frame
    mit_frame.clear()
    p = mit_frame.paragraphs[0]
    p.text = "Mitigants"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["body_size"]
    p.font.color.rgb = colors["primary"]
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    
    # Content positioning
    y_start = 2.0
    row_height = 1.1
    
    # Add considerations and mitigants
    considerations = (data or {}).get('considerations', [])
    mitigants = (data or {}).get('mitigants', [])
    
    max_items = max(len(considerations), len(mitigants))
    
    for i in range(max_items):
        y_pos = y_start + (i * row_height)
        
        # Add consideration if exists
        if i < len(considerations):
            # Question mark circle
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), Inches(y_pos), Inches(0.3), Inches(0.3))
            circle.fill.solid()
            circle.fill.fore_color.rgb = colors["primary"]
            circle.line.fill.background()
            
            # Question mark text
            q_text = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos), Inches(0.3), Inches(0.3))
            q_frame = q_text.text_frame
            q_frame.clear()
            p = q_frame.paragraphs[0]
            p.text = "?"
            p.font.name = fonts["primary_font"]
            p.font.size = fonts["body_size"]
            p.font.color.rgb = colors["background"]
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
            q_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            # Consideration text
            cons_text = slide.shapes.add_textbox(Inches(1.1), Inches(y_pos - 0.1), Inches(5.2), Inches(1.0))
            cons_text_frame = cons_text.text_frame
            cons_text_frame.clear()
            p = cons_text_frame.paragraphs[0]
            p.text = considerations[i]
            p.font.name = fonts["primary_font"]
            p.font.size = fonts["body_size"]
            p.font.color.rgb = colors["text"]
            p.font.bold = False
            cons_text_frame.word_wrap = True
            cons_text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Add mitigant if exists
        if i < len(mitigants):
            # Info circle
            circle2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.7), Inches(y_pos), Inches(0.3), Inches(0.3))
            circle2.fill.solid()
            circle2.fill.fore_color.rgb = colors["secondary"]
            circle2.line.fill.background()
            
            # Info icon text
            bulb_text = slide.shapes.add_textbox(Inches(6.7), Inches(y_pos), Inches(0.3), Inches(0.3))
            bulb_frame = bulb_text.text_frame
            bulb_frame.clear()
            p = bulb_frame.paragraphs[0]
            p.text = "i"
            p.font.name = fonts["primary_font"]
            p.font.size = fonts["body_size"]
            p.font.color.rgb = colors["background"]
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
            bulb_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            # Mitigant text
            mit_text = slide.shapes.add_textbox(Inches(7.1), Inches(y_pos - 0.1), Inches(5.7), Inches(1.0))
            mit_text_frame = mit_text.text_frame
            mit_text_frame.clear()
            p = mit_text_frame.paragraphs[0]
            p.text = mitigants[i]
            p.font.name = fonts["primary_font"]
            p.font.size = fonts["body_size"]
            p.font.color.rgb = colors["text"]
            p.font.bold = False
            mit_text_frame.word_wrap = True
            mit_text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(7.0), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_product_service_footprint_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Render a product & service / market footprint slide for investment banking presentations
    """
    
    # FIXED: Extract slide_data from data parameter (matching your system's pattern)
    slide_data = data or {}
    
    # Create presentation if not provided (standard 16:9 dimensions)
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add slide with blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Set white background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = colors["background"]
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Product & Service / Market Footprint')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    def add_clean_text(slide, left, top, width, height, text, font_size=14, 
                       color=None, bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        """Add text with consistent styling"""
        if color is None:
            color = colors["text"]
            
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = str(text)  # Convert to string to avoid issues
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        return textbox
    
    # Left side - Service descriptions with gold icons (ALL FROM DATA)
    services = slide_data.get('services', [])
    
    y_start = Inches(1.4)
    for i, service in enumerate(services):
        y_pos = y_start + Inches(i * 0.85)
        
        # Service icon (gold circle background)
        icon_bg = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), y_pos, Inches(0.3), Inches(0.3))
        icon_bg.fill.solid()
        icon_bg.fill.fore_color.rgb = colors["secondary"]
        icon_bg.line.fill.background()
        
        # Service title
        add_clean_text(slide, Inches(1.2), y_pos, Inches(5.5), Inches(0.25), 
                       service.get("title", ""), 12, colors["primary"], True)
        
        # Service description
        add_clean_text(slide, Inches(1.2), y_pos + Inches(0.25), Inches(5.5), Inches(0.55), 
                       service.get("desc", ""), 10, colors["text"])
    
    # Right side - Product/Market Table (ALL FROM DATA)
    table_left = Inches(7.2)
    table_width = Inches(5.5)
    
    # Table title from data
    table_title = slide_data.get('table_title', 'Product & Service Market Coverage')
    add_clean_text(slide, table_left, Inches(1.4), table_width, Inches(0.3), 
                   table_title, 14, colors["primary"], True, PP_ALIGN.CENTER)
    
    # Create table from data
    table_data = slide_data.get('coverage_table', [])
    
    if table_data:  # Only create table if data exists
        rows, cols = len(table_data), len(table_data[0])
        table_top = Inches(1.8)
        table_height = Inches(2.8)
        
        table = slide.shapes.add_table(rows, cols, table_left, table_top, table_width, table_height).table
        
        # Style table
        for i, row_data in enumerate(table_data):
            for j, cell_text in enumerate(row_data):
                cell = table.cell(i, j)
                cell.text = str(cell_text)
                cell.margin_left = Inches(0.05)
                cell.margin_right = Inches(0.05)
                cell.margin_top = Inches(0.05)
                cell.margin_bottom = Inches(0.05)
                
                # Style cell text
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.alignment = PP_ALIGN.CENTER
                    for run in paragraph.runs:
                        run.font.name = fonts["primary_font"]
                        run.font.size = Pt(9)
                        
                        if i == 0:  # Header row
                            run.font.bold = True
                            run.font.color.rgb = colors["background"]
                            cell.fill.solid()
                            cell.fill.fore_color.rgb = colors["primary"]
                        else:
                            run.font.color.rgb = colors["text"]
                            if i % 2 == 0:  # Alternate row colors
                                cell.fill.solid()
                                cell.fill.fore_color.rgb = colors["light_grey"]
                            else:
                                cell.fill.solid()
                                cell.fill.fore_color.rgb = colors["background"]
        
        # Adjust column widths dynamically based on number of columns
        if cols > 0:
            for i in range(cols):
                if i == 0:  # First column wider for location names
                    table.columns[i].width = Inches(1.2)
                else:
                    table.columns[i].width = Inches(0.8)
    
    # Key Operational Metrics (ALL FROM DATA)
    metrics_title_top = Inches(4.8)
    metrics_box_top = Inches(5.1)
    
    # Metrics title from data
    metrics_title = slide_data.get('metrics_title', 'Key Operational Metrics')
    add_clean_text(slide, table_left, metrics_title_top, table_width, Inches(0.3), 
                   metrics_title, 14, colors["primary"], True, PP_ALIGN.CENTER)
    
    # Metrics background box
    metrics_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, table_left, metrics_box_top, table_width, Inches(1.4))
    metrics_bg.fill.solid()
    metrics_bg.fill.fore_color.rgb = colors["light_grey"]
    metrics_bg.line.fill.background()
    
    # Get metrics data - completely flexible
    metrics = slide_data.get('metrics', {})
    metric_keys = list(metrics.keys())
    
    # Dynamic metrics layout
    metrics_left_col = table_left + Inches(0.3)
    metrics_right_col = table_left + Inches(2.8)
    col_width = Inches(2.2)
    
    # Left column metrics (first half)
    left_metrics = metric_keys[:len(metric_keys)//2]
    for i, key in enumerate(left_metrics):
        metric_data = metrics[key]
        label = metric_data.get('label', key.replace('_', ' ').title())
        value = metric_data.get('value', '')
        
        y_offset = Inches(0.2 + i * 0.55)
        add_clean_text(slide, metrics_left_col, metrics_box_top + y_offset, col_width, Inches(0.2), 
                       label, 10, colors["text"])
        add_clean_text(slide, metrics_left_col, metrics_box_top + y_offset + Inches(0.2), col_width, Inches(0.25), 
                       value, 16, colors["primary"], True)
    
    # Right column metrics (second half)
    right_metrics = metric_keys[len(metric_keys)//2:]
    for i, key in enumerate(right_metrics):
        metric_data = metrics[key]
        label = metric_data.get('label', key.replace('_', ' ').title())
        value = metric_data.get('value', '')
        
        y_offset = Inches(0.2 + i * 0.55)
        add_clean_text(slide, metrics_right_col, metrics_box_top + y_offset, col_width, Inches(0.2), 
                       label, 10, colors["text"])
        add_clean_text(slide, metrics_right_col, metrics_box_top + y_offset + Inches(0.2), col_width, Inches(0.25), 
                       value, 16, colors["primary"], True)
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT
    footer_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT
    footer_right = slide.shapes.add_textbox(Inches(9.5), Inches(7.0), Inches(3.5), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_competitive_positioning_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Render a competitive positioning slide for investment banking presentations
    """
    
    # Create presentation if not provided
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add slide with blank layout
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set white background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = colors["background"]
    
    def add_clean_text(slide, left, top, width, height, text, font_size=14, 
                       color=None, bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        """Add text with consistent styling"""
        if color is None:
            color = colors["text"]
            
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        return textbox
    
    # Extract slide data
    slide_data = data or {}
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Competitive Positioning')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Left side - Revenue Comparison Chart
    add_clean_text(slide, Inches(0.5), Inches(1.3), Inches(6), Inches(0.3), 
                   "Revenue Comparison vs. Competitors", 14, colors["primary"], True)
    
    # Create bar chart data
    competitors_data = slide_data.get('competitors', [
        {'name': 'Central Health', 'revenue': 450},
        {'name': 'HK Sanatorium', 'revenue': 380},
        {'name': 'Matilda Intl', 'revenue': 320},
        {'name': 'OT&P Healthcare', 'revenue': 280},
        {'name': 'Quality HealthCare', 'revenue': 250},
        {'name': 'Union Hospital', 'revenue': 220}
    ])
    
    chart_data = ChartData()
    chart_data.categories = [comp['name'] for comp in competitors_data]
    chart_data.add_series('Revenue (HK$ M)', [comp['revenue'] for comp in competitors_data])
    
    # Add chart
    chart_left = Inches(0.5)
    chart_top = Inches(1.7)
    chart_width = Inches(6)
    chart_height = Inches(2.5)
    
    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, chart_left, chart_top, chart_width, chart_height, chart_data
    )
    
    chart = chart_shape.chart
    
    # Style the chart
    chart.has_legend = False
    chart.chart_title.has_text_frame = True
    chart.chart_title.text_frame.clear()
    
    # Style chart elements
    category_axis = chart.category_axis
    category_axis.has_major_gridlines = False
    category_axis.tick_labels.font.size = Pt(9)
    category_axis.tick_labels.font.name = fonts["primary_font"]
    
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.tick_labels.font.size = Pt(9)
    value_axis.tick_labels.font.name = fonts["primary_font"]
    value_axis.maximum_scale = 500
    
    # Highlight specific bar in gold/secondary color
    series = chart.series[0]
    points = series.points
    for i, point in enumerate(points):
        if competitors_data[i]['name'] == 'OT&P Healthcare':  # Find target company
            point.format.fill.solid()
            point.format.fill.fore_color.rgb = colors["secondary"]
        else:
            point.format.fill.solid()
            point.format.fill.fore_color.rgb = colors["primary"]
    
    # Right side - Competitive Assessment Table
    add_clean_text(slide, Inches(7.5), Inches(1.3), Inches(5.5), Inches(0.3), 
                   "Competitive Assessment", 14, colors["primary"], True)
    
    # Assessment table data
    assessment_data = slide_data.get('assessment', [
        ["Provider", "Services", "Digital", "Intl. Focus", "Locations"],
        ["OT&P Healthcare", "●●●●●", "●●●●", "●●●●●", "●●●"],
        ["Central Health", "●●●●●", "●●●", "●●●●", "●●"],
        ["HK Sanatorium", "●●●●●", "●●", "●●●", "●"],
        ["Matilda Intl.", "●●●●", "●●●", "●●●●", "●"]
    ])
    
    # Create assessment table
    table_left = Inches(7.5)
    table_top = Inches(1.7)
    table_width = Inches(5.5)
    table_height = Inches(1.5)
    
    rows, cols = len(assessment_data), len(assessment_data[0])
    table = slide.shapes.add_table(rows, cols, table_left, table_top, table_width, table_height).table
    
    # Style assessment table
    for i, row_data in enumerate(assessment_data):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)
            cell.text = cell_text
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)
            
            for paragraph in cell.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                for run in paragraph.runs:
                    run.font.name = fonts["primary_font"]
                    run.font.size = Pt(8)
                    
                    if i == 0:  # Header row
                        run.font.bold = True
                        run.font.color.rgb = colors["background"]
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = colors["primary"]
                    elif i == 1:  # Target company row (highlighted)
                        run.font.color.rgb = colors["primary"]
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = colors["light_grey"]
                    else:
                        run.font.color.rgb = colors["text"]
                        if i % 2 == 0:
                            cell.fill.solid()
                            cell.fill.fore_color.rgb = colors["light_grey"]
    
    # Adjust table column widths
    col_widths = [Inches(1.5), Inches(0.8), Inches(0.7), Inches(0.9), Inches(0.8)]
    for i, width in enumerate(col_widths):
        table.columns[i].width = width
    
    # Source note for assessment
    add_clean_text(slide, Inches(7.5), Inches(3.3), Inches(5.5), Inches(0.2), 
                   "Source: Management estimates, competitor websites, July 2024 [Medium Confidence]", 
                   8, colors["text"])
    
    # Bottom left - Barriers to Entry
    add_clean_text(slide, Inches(0.5), Inches(4.5), Inches(6), Inches(0.3), 
                   "Barriers to Entry", 14, colors["primary"], True)
    
    barriers = slide_data.get('barriers', [
        {"title": "Regulatory Compliance:", "desc": "Stringent healthcare licensing requirements and facility standards"},
        {"title": "Specialist Recruitment:", "desc": "Challenging acquisition of multilingual medical talent"},
        {"title": "Prime Real Estate:", "desc": "Limited availability and high cost of clinic locations"},
        {"title": "Insurance Relationships:", "desc": "Established direct billing partnerships with 35+ insurers"}
    ])
    
    y_start = Inches(4.9)
    for i, barrier in enumerate(barriers):
        y_pos = y_start + Inches(i * 0.35)
        
        # Gold bullet
        bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), y_pos, Inches(0.06), Inches(0.06))
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = colors["secondary"]
        bullet.line.fill.background()
        
        # Barrier text
        barrier_text = f"{barrier['title']} {barrier['desc']}"
        add_clean_text(slide, Inches(0.85), y_pos - Inches(0.05), Inches(5.5), Inches(0.3), 
                       barrier_text, 9, colors["text"])
    
    # Bottom right - Company's Unique Advantages
    add_clean_text(slide, Inches(7.5), Inches(3.8), Inches(5.5), Inches(0.3), 
                   "Company's Unique Advantages", 14, colors["primary"], True)
    
    advantages = slide_data.get('advantages', [
        {"title": "International Accreditation:", "desc": "First Hong Kong clinic accredited by Australian Council"},
        {"title": "Multi-specialty Integration:", "desc": "Comprehensive holistic care model spanning physical and mental health"},
        {"title": "In-house Pharmacy:", "desc": "Holder of wholesale pharmacy license with dedicated pharmacy team"},
        {"title": "Teaching Status:", "desc": "Recognized undergraduate and postgraduate teaching unit"}
    ])
    
    y_start = Inches(4.2)
    for i, advantage in enumerate(advantages):
        y_pos = y_start + Inches(i * 0.35)
        
        # Gold bullet
        bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.7), y_pos, Inches(0.06), Inches(0.06))
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = colors["secondary"]
        bullet.line.fill.background()
        
        # Advantage text
        advantage_text = f"{advantage['title']} {advantage['desc']}"
        add_clean_text(slide, Inches(7.85), y_pos - Inches(0.05), Inches(5), Inches(0.3), 
                       advantage_text, 9, colors["text"])
    
    # Source note for chart
    add_clean_text(slide, Inches(0.5), Inches(4.3), Inches(6), Inches(0.15), 
                   "Source: Company analysis, industry reports, 2024 [High Confidence]", 
                   8, colors["text"])
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(4), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT
    footer_right = slide.shapes.add_textbox(Inches(9.5), Inches(7.0), Inches(3.5), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_investor_process_overview_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders an investor considerations & process overview slide with 4-quadrant layout
    IMPROVED: Better spacing and text fitting for comprehensive content
    """
    
    # FIXED: Extract slide_data from data parameter
    slide_data = data or {}
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Investor Process Overview - Comprehensive Due Diligence')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Helper function to add clean text with better wrapping
    def add_clean_text(slide, left, top, width, height, text, font_size=10, 
                       color=colors["text"], bold=False, align=PP_ALIGN.LEFT):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.08)
        text_frame.margin_right = Inches(0.08)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        text_frame.auto_size = None  # Prevent auto-sizing issues
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            paragraph.line_spacing = 1.1  # Better line spacing
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        return textbox
    
    # Debug logging
    print(f"[DEBUG] Investor process overview data keys: {list(slide_data.keys())}")
    
    # TOP LEFT: Key Diligence Topics - IMPROVED SPACING
    add_clean_text(slide, Inches(0.5), Inches(1.5), Inches(6), Inches(0.3), 
                   "Key Diligence Topics", 14, colors["primary"], True)
    
    diligence_items = slide_data.get('diligence_topics', [])
    print(f"[DEBUG] Diligence topics count: {len(diligence_items)}")
    
    y_start = Inches(1.85)  # Moved down for more breathing room
    for i, item in enumerate(diligence_items[:5]):  # Allow 5 items now
        y_pos = y_start + Inches(i * 0.34)  # Slightly more spacing
        
        # Gold bullet
        bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.65), y_pos, Inches(0.06), Inches(0.06))
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = colors["secondary"]
        bullet.line.fill.background()
        
        # Item text - LARGER TEXT BOX
        if isinstance(item, dict):
            item_text = f"{item.get('title', '')}: {item.get('description', '')}"
        else:
            item_text = str(item)
        add_clean_text(slide, Inches(0.8), y_pos - Inches(0.05), Inches(5.6), Inches(0.28), 
                       item_text, 9, colors["text"])  # Smaller font, more space
    
    # BOTTOM LEFT: Risk Factors & Mitigants - REPOSITIONED
    add_clean_text(slide, Inches(0.5), Inches(3.6), Inches(6), Inches(0.3), 
                   "Risk Factors & Mitigants", 14, colors["primary"], True)
    
    risk_factors = slide_data.get('risk_factors', [])
    mitigants = slide_data.get('mitigants', [])
    
    print(f"[DEBUG] Risk factors count: {len(risk_factors)}")
    print(f"[DEBUG] Mitigants count: {len(mitigants)}")
    
    y_start = Inches(3.95)  # Moved down slightly
    max_items = max(len(risk_factors), len(mitigants), 5)  # Allow 5 items
    
    for i in range(min(max_items, 5)):  # Max 5 to fit properly
        y_pos = y_start + Inches(i * 0.28)  # Slightly more spacing
        
        # Risk factor (if exists)
        if i < len(risk_factors):
            # Red circle for risk
            risk_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.65), y_pos, Inches(0.06), Inches(0.06))
            risk_circle.fill.solid()
            risk_circle.fill.fore_color.rgb = RGBColor(220, 20, 60)  # Red color
            risk_circle.line.fill.background()
            
            # Risk factor text - IMPROVED SIZING
            add_clean_text(slide, Inches(0.8), y_pos - Inches(0.05), Inches(2.6), Inches(0.22), 
                           risk_factors[i], 8, RGBColor(220, 20, 60))
        
        # Mitigant (if exists)
        if i < len(mitigants):
            # Green circle for mitigant
            mitigant_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(3.6), y_pos, Inches(0.06), Inches(0.06))
            mitigant_circle.fill.solid()
            mitigant_circle.fill.fore_color.rgb = RGBColor(34, 139, 34)  # Green color
            mitigant_circle.line.fill.background()
            
            # Mitigant text - IMPROVED SIZING
            add_clean_text(slide, Inches(3.75), y_pos - Inches(0.05), Inches(2.8), Inches(0.22), 
                           mitigants[i], 8, RGBColor(34, 139, 34))
    
    # TOP RIGHT: Investment Highlights - IMPROVED
    synergy_items = slide_data.get('synergy_opportunities', [])
    
    # If no synergy opportunities, show investment highlights instead
    if not synergy_items:
        add_clean_text(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(0.3), 
                       "Investment Highlights", 14, colors["primary"], True)
        
        investment_highlights = slide_data.get('investment_highlights', [])
        
        y_start = Inches(1.85)  # Moved down to match left side
        for i, highlight in enumerate(investment_highlights[:5]):  # Allow 5 highlights
            y_pos = y_start + Inches(i * 0.34)  # Match spacing with left side
            
            # Gold bullet
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.15), y_pos, Inches(0.06), Inches(0.06))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            # Highlight text - BETTER SIZING
            add_clean_text(slide, Inches(7.3), y_pos - Inches(0.05), Inches(5.5), Inches(0.28), 
                           highlight, 9, colors["text"])
    else:
        add_clean_text(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(0.3), 
                       "Synergy Opportunities", 14, colors["primary"], True)
        
        y_start = Inches(1.85)  # Moved down to match
        for i, item in enumerate(synergy_items[:5]):
            y_pos = y_start + Inches(i * 0.34)  # Match spacing
            
            # Gold bullet
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.15), y_pos, Inches(0.06), Inches(0.06))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            # Item text
            if isinstance(item, dict):
                item_text = f"{item.get('title', '')}: {item.get('description', '')}"
            else:
                item_text = str(item)
            add_clean_text(slide, Inches(7.3), y_pos - Inches(0.05), Inches(5.5), Inches(0.28), 
                           item_text, 9, colors["text"])
    
    # BOTTOM RIGHT: Process Next Steps - IMPROVED
    timeline_items = slide_data.get('timeline', [])
    
    if not timeline_items:
        add_clean_text(slide, Inches(7), Inches(3.6), Inches(5.8), Inches(0.3), 
                       "Process Next Steps", 14, colors["primary"], True)
        
        next_steps = slide_data.get('next_steps', [])
        
        y_start = Inches(3.95)  # Moved down slightly to match left side
        for i, item in enumerate(next_steps[:5]):  # Allow 5 steps
            y_pos = y_start + Inches(i * 0.28)  # Match spacing with left side
            
            # Gold circle marker
            marker = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.15), y_pos, Inches(0.06), Inches(0.06))
            marker.fill.solid()
            marker.fill.fore_color.rgb = colors["secondary"]
            marker.line.fill.background()
            
            # Combined date and description in one line for better space usage
            combined_text = f"{item.get('date', '')}: {item.get('description', '')}"
            add_clean_text(slide, Inches(7.3), y_pos - Inches(0.05), Inches(5.5), Inches(0.22), 
                           combined_text, 8, colors["text"])
    else:
        add_clean_text(slide, Inches(7), Inches(3.6), Inches(5.8), Inches(0.3), 
                       "Transaction Timeline", 14, colors["primary"], True)
        
        y_start = Inches(3.95)  # Match positioning
        for i, item in enumerate(timeline_items[:5]):
            y_pos = y_start + Inches(i * 0.28)  # Match spacing
            
            # Gold circle marker
            marker = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.15), y_pos, Inches(0.06), Inches(0.06))
            marker.fill.solid()
            marker.fill.fore_color.rgb = colors["secondary"]
            marker.line.fill.background()
            
            # Combined date and description
            combined_text = f"{item.get('date', '')}: {item.get('description', '')}"
            add_clean_text(slide, Inches(7.3), y_pos - Inches(0.05), Inches(5.5), Inches(0.22), 
                           combined_text, 8, colors["text"])
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT (light grey)
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(6.9), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_margin_cost_resilience_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a margin & cost resilience slide with charts and detailed analysis
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Helper function to add clean text
    def add_clean_text(slide, left, top, width, height, text, font_size=10, 
                       color=colors["text"], bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        # Remove shadow/outline
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        
        return textbox
    
    # Debug logging
    print(f"[DEBUG] Margin cost resilience data keys: {list((data or {}).keys())}")
    
    # Extract slide data - handle both data formats
    slide_data = data or {}
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Margin & Cost Resilience')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # EBITDA Margin Trend Chart
    chart_title = slide_data.get('chart_title', 'EBITDA Margin Trend')
    add_clean_text(slide, Inches(1), Inches(1.4), Inches(6), Inches(0.3), 
                   chart_title, 14, colors["primary"], True)
    
    # Create line chart for EBITDA margins
    chart_data_info = slide_data.get('chart_data', {})
    
    # Create chart if we have data
    if chart_data_info:
        try:
            chart_data = ChartData()
            
            categories = chart_data_info.get('categories', ['2020', '2021', '2022', '2023', '2024E'])
            values = chart_data_info.get('values', [15.0, 16.6, 17.2, 19.0, 19.6])
            
            print(f"[DEBUG] Chart categories: {categories}")
            print(f"[DEBUG] Chart values: {values}")
            
            chart_data.categories = categories
            chart_data.add_series('EBITDA Margin %', values)
            
            # Add line chart
            chart_left = Inches(1)
            chart_top = Inches(1.8)
            chart_width = Inches(6)
            chart_height = Inches(2.2)
            
            chart_shape = slide.shapes.add_chart(
                XL_CHART_TYPE.LINE_MARKERS, chart_left, chart_top, chart_width, chart_height, chart_data
            )
            
            chart = chart_shape.chart
            
            # Style the chart
            chart.has_legend = False
            chart.chart_title.has_text_frame = True
            chart.chart_title.text_frame.clear()
            
            # Style chart elements
            try:
                category_axis = chart.category_axis
                category_axis.has_major_gridlines = False
                category_axis.tick_labels.font.size = Pt(10)
                category_axis.tick_labels.font.name = fonts["primary_font"]
                
                value_axis = chart.value_axis
                value_axis.has_major_gridlines = True
                value_axis.tick_labels.font.size = Pt(10)
                value_axis.tick_labels.font.name = fonts["primary_font"]
                value_axis.maximum_scale = 500
                
                # Style the line series (secondary color)
                series = chart.series[0]
                series.format.line.color.rgb = colors["secondary"]
                series.format.line.width = Pt(3)
                
                # Style the markers
                for point in series.points:
                    point.format.fill.solid()
                    point.format.fill.fore_color.rgb = colors["secondary"]
                    point.format.line.color.rgb = colors["secondary"]
            except Exception as e:
                print(f"[DEBUG] Chart styling error: {e}")
                
        except Exception as e:
            print(f"[DEBUG] Chart creation error: {e}")
            # Add fallback text if chart fails
            add_clean_text(slide, Inches(1), Inches(2), Inches(6), Inches(1), 
                           "EBITDA margin trend chart will be displayed here.", 12, colors["text"])
    else:
        # Add fallback if no chart data
        add_clean_text(slide, Inches(1), Inches(2), Inches(6), Inches(1), 
                       "EBITDA margin trend chart will be displayed here.", 12, colors["text"])
    
    # Chart source note
    chart_source = slide_data.get('chart_source', 'Source: Company financials')
    add_clean_text(slide, Inches(5), Inches(4.1), Inches(2.5), Inches(0.15), 
                   chart_source, 8, colors["text"], False, PP_ALIGN.RIGHT)
    
    # Left side - Cost Management Strategies
    cost_section = slide_data.get('cost_management', {})
    cost_title = cost_section.get('title', 'Cost Management & Efficiency Initiatives')
    add_clean_text(slide, Inches(1), Inches(4.4), Inches(6), Inches(0.3), 
                   cost_title, 14, colors["primary"], True)
    
    # Cost management items - FIXED POSITIONING
    cost_items = cost_section.get('items', [
        {
            "title": "Operational Efficiency",
            "description": "Streamlined processes and resource optimization initiatives"
        },
        {
            "title": "Technology Investment", 
            "description": "Digital transformation reducing administrative overhead"
        },
        {
            "title": "Supply Chain Management",
            "description": "Centralized procurement and vendor consolidation"
        }
    ])
    
    y_start = Inches(4.8)
    
    for i, item in enumerate(cost_items[:3]):  # Max 3 items to fit properly
        y_pos = y_start + Inches(i * 0.45)  # Reduced spacing from 0.5 to 0.45
        
        # Gold bullet (no shadow)
        bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.2), y_pos, Inches(0.06), Inches(0.06))
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = colors["secondary"]
        bullet.line.fill.background()
        bullet.shadow.inherit = False
        
        # Item title (bold) - reduced height
        add_clean_text(slide, Inches(1.35), y_pos - Inches(0.05), Inches(5.5), Inches(0.15), 
                       item.get('title', ''), 10, colors["primary"], True)
        
        # Item description - reduced height and adjusted position
        add_clean_text(slide, Inches(1.35), y_pos + Inches(0.1), Inches(5.5), Inches(0.28), 
                       item.get('description', ''), 9, colors["text"])
    
    # Right side - Risk Mitigation Strategies
    risk_section = slide_data.get('risk_mitigation', {})
    risk_title = risk_section.get('title', 'Risk Mitigation Strategies')
    add_clean_text(slide, Inches(8), Inches(1.4), Inches(5), Inches(0.3), 
                   risk_title, 14, colors["primary"], True)
    
    # Main strategy box (no shadow)
    main_strategy = risk_section.get('main_strategy', {
        'title': 'Diversified Revenue Base',
        'description': 'Multiple service lines and geographic markets reduce concentration risk',
        'benefits': ['Lower volatility', 'Stable cash flows', 'Reduced dependency']
    })
    
    strategy_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8), Inches(1.8), Inches(5), Inches(1.8))
    strategy_box.fill.solid()
    strategy_box.fill.fore_color.rgb = colors["light_grey"]
    strategy_box.line.fill.background()
    strategy_box.shadow.inherit = False  # Remove shadow
    
    # Gold stripe (no shadow)
    gold_stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8), Inches(1.8), Inches(0.1), Inches(1.8))
    gold_stripe.fill.solid()
    gold_stripe.fill.fore_color.rgb = colors["secondary"]
    gold_stripe.line.fill.background()
    gold_stripe.shadow.inherit = False  # Remove shadow
    
    # Strategy content
    strategy_title = main_strategy.get('title', 'Revenue Diversification Strategy')
    add_clean_text(slide, Inches(8.3), Inches(1.9), Inches(4.5), Inches(0.25), 
                   strategy_title, 12, colors["secondary"], True)
    
    strategy_desc = main_strategy.get('description', 'Multiple revenue streams provide stability')
    add_clean_text(slide, Inches(8.3), Inches(2.15), Inches(4.5), Inches(0.35), 
                   strategy_desc, 10, colors["text"])
    
    # Benefits
    benefits_title = "Key Benefits:"
    add_clean_text(slide, Inches(8.3), Inches(2.55), Inches(4.5), Inches(0.18), 
                   benefits_title, 10, colors["primary"], True)
    
    benefits = main_strategy.get('benefits', ['Lower volatility', 'Stable cash flows', 'Reduced risk'])
    for i, benefit in enumerate(benefits[:3]):  # Max 3 benefits
        add_clean_text(slide, Inches(8.5), Inches(2.75 + i * 0.13), Inches(4.3), Inches(0.11), 
                       f"• {benefit}", 9, colors["text"])
    
    # Banker's view box (no shadow)
    banker_view = risk_section.get('banker_view', {
        'title': "BANKER'S VIEW",
        'text': 'Strong operational resilience and margin expansion demonstrate effective cost management and revenue diversification strategies.'
    })
    
    banker_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8), Inches(3.8), Inches(5), Inches(0.8))
    banker_box.fill.solid()
    banker_box.fill.fore_color.rgb = RGBColor(240, 255, 240)  # Light green
    banker_box.line.fill.background()
    banker_box.shadow.inherit = False  # Remove shadow
    
    banker_title = banker_view.get('title', "BANKER'S VIEW")
    add_clean_text(slide, Inches(8.2), Inches(3.9), Inches(4.6), Inches(0.15), 
                   banker_title, 10, RGBColor(34, 139, 34), True)
    
    banker_text = banker_view.get('text', 'Strong margin expansion demonstrates operational excellence.')
    add_clean_text(slide, Inches(8.2), Inches(4.05), Inches(4.6), Inches(0.5), 
                   banker_text, 9, colors["text"])
    
    # Bottom summary - FIXED POSITIONING to avoid overlap
    summary = slide_data.get('summary', '')
    if summary:
        # Moved summary higher to avoid overlapping with footer
        add_clean_text(slide, Inches(1), Inches(6.2), Inches(12), Inches(0.5), 
                       summary, 10, colors["primary"])
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer - "Confidential | [today's date]" on LEFT (light grey) - FIXED POSITION
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer - Company name on RIGHT - FIXED POSITION
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(6.9), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_historical_financial_performance_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a historical financial performance slide with chart and metrics
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Helper function to add clean text
    def add_clean_text(slide, left, top, width, height, text, font_size=10, 
                       color=colors["text"], bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        # Remove shadow/outline
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        
        return textbox
    
    # Set white background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = colors["background"]
    
    # STANDARDIZED: Apply header and title
    title_text = (data or {}).get('title', 'Historical Financial Performance (I)')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Main chart title
    chart_info = (data or {}).get('chart', {})
    chart_title = chart_info.get('title', 'Company - 5-Year Financial Performance')
    add_clean_text(slide, Inches(1), Inches(1.3), Inches(11), Inches(0.3), 
                   chart_title, 16, colors["primary"], True, PP_ALIGN.CENTER)
    
    # Create combination chart
    chart_data = ChartData()
    categories = chart_info.get('categories', ['2020', '2021', '2022', '2023', '2024'])
    revenue_data = chart_info.get('revenue', [26, 24, 33, 40, 42])
    ebitda_data = chart_info.get('ebitda', [6.5, 5.8, 8.2, 10.0, 11.2])
    
    chart_data.categories = categories
    chart_data.add_series('Revenue (USD millions)', revenue_data)
    chart_data.add_series('EBITDA (USD millions)', ebitda_data)
    
    # Add chart
    chart_left = Inches(2)
    chart_top = Inches(1.7)
    chart_width = Inches(9)
    chart_height = Inches(2.3)
    
    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, chart_left, chart_top, chart_width, chart_height, chart_data
    )
    
    chart = chart_shape.chart
    
    # Style the chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.TOP
    chart.legend.font.size = Pt(10)
    
    # Style chart elements
    category_axis = chart.category_axis
    category_axis.has_major_gridlines = False
    category_axis.tick_labels.font.size = Pt(10)
    category_axis.tick_labels.font.name = fonts["primary_font"]
    
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.tick_labels.font.size = Pt(10)
    value_axis.tick_labels.font.name = fonts["primary_font"]
    value_axis.maximum_scale = 45
    
    # Color the series
    series = chart.series
    
    # Revenue series (primary color)
    revenue_series = series[0]
    revenue_series.format.fill.solid()
    revenue_series.format.fill.fore_color.rgb = colors["primary"]
    for point in revenue_series.points:
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = colors["primary"]
    
    # EBITDA series (secondary color)
    ebitda_series = series[1]
    ebitda_series.format.fill.solid()
    ebitda_series.format.fill.fore_color.rgb = colors["secondary"]
    for point in ebitda_series.points:
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = colors["secondary"]
    
    # Chart footnote
    chart_footnote = chart_info.get('footnote', '*Historical figures represent estimated performance based on market trends.')
    add_clean_text(slide, Inches(2), Inches(4.1), Inches(9), Inches(0.2), 
                   chart_footnote, 8, colors["text"], False, PP_ALIGN.CENTER)
    
    # Key metrics section (removed shadows from boxes)
    metrics_section = (data or {}).get('key_metrics', {})
    metrics_y = Inches(4.4)
    metrics = metrics_section.get('metrics', [])
    
    # If no metrics provided, create default ones
    if not metrics:
        metrics = [
            {
                'title': 'Patient Growth (CAGR)',
                'value': '12.4%',
                'period': '(2020-2024)',
                'note': '✓ Consistent growth despite pandemic disruptions'
            },
            {
                'title': 'Patient Retention Rate',
                'value': '87%',
                'period': '(2024)',
                'note': '✓ Premium market segment leading indicator'
            },
            {
                'title': 'Avg. Revenue Per Patient',
                'value': '$980',
                'period': 'USD (2024)',
                'note': '↗ +8.2% increase from 2023'
            },
            {
                'title': 'Corporate Contracts',
                'value': '35+',
                'period': '(2024)',
                'note': '● Major financial institutions & MNCs'
            }
        ]
    
    # Calculate positions to fit exactly 4 boxes across slide width
    slide_content_width = Inches(12.5)  # Total usable width
    box_width = Inches(2.8)             # Width of each box
    total_boxes_width = box_width * 4   # Total width of all boxes
    spacing_width = slide_content_width - total_boxes_width  # Remaining space
    box_spacing = spacing_width / 5     # Space between boxes (5 gaps: before, between 3, after)
    
    for i, metric in enumerate(metrics[:4]):  # Max 4 metrics
        x_pos = Inches(0.5) + box_spacing + i * (box_width + box_spacing)
        
        # Metric box (NO SHADOW)
        metric_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, metrics_y, box_width, Inches(1.1))
        metric_bg.fill.solid()
        metric_bg.fill.fore_color.rgb = colors["light_grey"]
        metric_bg.line.fill.background()
        metric_bg.shadow.inherit = False  # Remove shadow
        
        add_clean_text(slide, x_pos + Inches(0.1), metrics_y + Inches(0.1), box_width - Inches(0.2), Inches(0.2), 
                       metric.get('title', ''), 10, colors["text"], True)
        add_clean_text(slide, x_pos + Inches(0.1), metrics_y + Inches(0.3), box_width - Inches(0.2), Inches(0.25), 
                       metric.get('value', ''), 18, colors["primary"], True)
        add_clean_text(slide, x_pos + Inches(0.1), metrics_y + Inches(0.55), box_width - Inches(0.2), Inches(0.15), 
                       metric.get('period', ''), 9, colors["text"])
        add_clean_text(slide, x_pos + Inches(0.1), metrics_y + Inches(0.75), box_width - Inches(0.2), Inches(0.25), 
                       metric.get('note', ''), 8, RGBColor(34, 139, 34))
    
    # Revenue Growth section
    revenue_section = (data or {}).get('revenue_growth', {})
    covid_y = Inches(5.7)
    section_title = revenue_section.get('title', 'Revenue Growth')
    add_clean_text(slide, Inches(1), covid_y, Inches(7), Inches(0.2), 
                   section_title, 12, colors["primary"], True)
    
    # Five bullet points for revenue growth
    revenue_points = revenue_section.get('points', [])
    for i, point in enumerate(revenue_points[:5]):  # Max 5 points
        add_clean_text(slide, Inches(1), covid_y + Inches(0.25 + i * 0.18), Inches(7), Inches(0.16), 
                       f"● {point}", 9, colors["text"])
    
    # Banker's view section (NO SHADOW)
    banker_view = (data or {}).get('banker_view', {})
    banker_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), covid_y, Inches(4.3), Inches(0.7))
    banker_box.fill.solid()
    banker_box.fill.fore_color.rgb = RGBColor(240, 255, 240)  # Light green
    banker_box.line.fill.background()  # Remove outline
    banker_box.shadow.inherit = False  # Remove shadow
    
    add_clean_text(slide, Inches(8.7), covid_y + Inches(0.05), Inches(3.9), Inches(0.15), 
                   banker_view.get('title', "BANKER'S VIEW"), 10, RGBColor(34, 139, 34), True)
    add_clean_text(slide, Inches(8.7), covid_y + Inches(0.2), Inches(3.9), Inches(0.45), 
                   banker_view.get('text', ''), 9, colors["text"])
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Footer
    add_clean_text(slide, Inches(0.5), Inches(6.9), Inches(4), Inches(0.2), 
                   f"Confidential | {today}", 9, colors["footer_grey"])
    
    add_clean_text(slide, Inches(9.5), Inches(6.9), Inches(3.5), Inches(0.2), 
                   f"{company_name} Investment Opportunity    6", 9, colors["footer_grey"], False, PP_ALIGN.RIGHT)
    
    return prs


def render_business_overview_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Render a business & operational overview slide for investment banking presentations
    """
    
    # Create presentation if not provided (standard 16:9 dimensions)
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)  # Standard 16:9 width
        prs.slide_height = Inches(7.5)    # Standard 16:9 height
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add slide with blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Set clean white background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = colors["background"]
    
    def add_clean_text(slide, left, top, width, height, text, font_size=14, 
                       color=None, bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        """Add text with consistent sizing and NO OUTLINES"""
        if color is None:
            color = colors["text"]
            
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        # Style the text consistently
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        # Background (if needed) - NO OUTLINES
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        # Remove all borders/outlines
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        
        return textbox
    
    # Debug logging
    print(f"[DEBUG] Business overview data keys: {list((data or {}).keys())}")
    
    # Extract slide data - handle both data formats
    slide_data = data or {}
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Business & Operational Overview')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Company description - FIXED POSITIONING
    company_desc = slide_data.get('description', 'Leading healthcare services provider with comprehensive medical care and operational excellence.')
    print(f"[DEBUG] Company description: {company_desc}")
    
    add_clean_text(slide, Inches(0.8), Inches(1.3), Inches(12), Inches(1.2), 
                   company_desc, 14, colors["text"])
    
    # Timeline elements - FIXED POSITIONING AND SPACING
    timeline_data = slide_data.get('timeline', {
        'start_year': '2015',
        'end_year': '2024',
        'years_note': '(9+ years of operation)'
    })
    
    timeline_y = Inches(2.8)  # Moved down to avoid overlap
    
    try:
        # Start year circle
        start_year = timeline_data.get('start_year', '2015')
        circle1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1), timeline_y, Inches(0.12), Inches(0.12))
        circle1.fill.solid()
        circle1.fill.fore_color.rgb = colors["secondary"]
        circle1.line.fill.background()
        
        # Timeline line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.12), timeline_y + Inches(0.05), 
                                      Inches(4), Inches(0.02))  # Shorter line
        line.fill.solid()
        line.fill.fore_color.rgb = colors["secondary"]
        line.line.fill.background()
        
        # End year circle
        end_year = timeline_data.get('end_year', '2024')
        circle2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5), timeline_y, Inches(0.12), Inches(0.12))
        circle2.fill.solid()
        circle2.fill.fore_color.rgb = colors["secondary"]
        circle2.line.fill.background()
        
        # Timeline labels - BETTER POSITIONING
        add_clean_text(slide, Inches(0.9), timeline_y - Inches(0.3), Inches(0.5), Inches(0.2), 
                       start_year, 11, colors["primary"], True, PP_ALIGN.CENTER)
        
        add_clean_text(slide, Inches(4.9), timeline_y - Inches(0.3), Inches(0.5), Inches(0.2), 
                       end_year, 11, colors["primary"], True, PP_ALIGN.CENTER)
        
        years_operation = timeline_data.get('years_note', '(9+ years of growth and expansion)')
        add_clean_text(slide, Inches(5.4), timeline_y - Inches(0.1), Inches(3), Inches(0.3), 
                       years_operation, 9, colors["text"])
    except Exception as e:
        print(f"[DEBUG] Timeline creation error: {e}")
    
    # Operational Highlights box - REPOSITIONED FOR 16:9
    try:
        highlights_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.2), Inches(1.3), 
                                               Inches(4.5), Inches(3.5))  # Taller box
        highlights_bg.fill.solid()
        highlights_bg.fill.fore_color.rgb = colors["light_grey"]
        highlights_bg.line.fill.background()
        highlights_bg.shadow.inherit = False
        
        # Highlights title
        highlights_title = slide_data.get('highlights_title', 'Key Operational Highlights')
        add_clean_text(slide, Inches(8.4), Inches(1.4), Inches(4.1), Inches(0.3), 
                       highlights_title, 14, colors["primary"], True, PP_ALIGN.CENTER)
        
        # Highlight items with bullets - BETTER SPACING
        highlights = slide_data.get('highlights', [
            '15 premium clinic locations across Southeast Asia',
            '18,000+ active patients with high retention rates',
            '35+ corporate wellness contracts with major employers',
            'Advanced digital health platform and telemedicine capabilities',
            'Board-certified specialists across multiple medical disciplines',
            'International accreditation and quality certifications'
        ])
        
        for i, item in enumerate(highlights[:6]):  # Max 6 items to fit properly
            y_pos = Inches(1.8 + i * 0.4)  # More spacing between items
            
            # Gold bullet
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.5), y_pos, Inches(0.06), Inches(0.06))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            # Text
            add_clean_text(slide, Inches(8.65), y_pos - Inches(0.05), Inches(3.8), Inches(0.35), 
                           item, 10, colors["text"])
    except Exception as e:
        print(f"[DEBUG] Highlights section error: {e}")
    
    # Service Lines section - REPOSITIONED
    try:
        services_title = slide_data.get('services_title', 'Core Service Lines')
        add_clean_text(slide, Inches(0.8), Inches(3.4), Inches(5), Inches(0.3), 
                       services_title, 14, colors["primary"], True)
        
        # Service items - BETTER SPACING
        services = slide_data.get('services', [
            'Primary Care & Preventive Medicine',
            'Specialty Medical Services',
            'Diagnostic Imaging & Laboratory',
            'Corporate Wellness Programs',
            'Digital Health & Telemedicine',
            'Executive Health Assessments'
        ])
        
        service_cols = 2  # Split into 2 columns
        items_per_col = (len(services) + 1) // 2
        
        for i, service in enumerate(services[:8]):  # Support up to 8 detailed services
            if i < items_per_col:  # Left column
                x_pos = Inches(0.9)
                y_pos = Inches(3.4 + i * 0.5)  # Proper spacing for detailed text
            else:  # Right column
                x_pos = Inches(4.2)  # Optimized column positioning
                y_pos = Inches(3.4 + (i - items_per_col) * 0.5)
            
            # Gold bullet - aligned with text baseline
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_pos, y_pos + Inches(0.08), Inches(0.04), Inches(0.04))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            # Text with proper width for detailed service descriptions
            add_clean_text(slide, x_pos + Inches(0.12), y_pos, Inches(3.5), Inches(0.45), 
                           service, 9, colors["text"])
    except Exception as e:
        print(f"[DEBUG] Services section error: {e}")
    
    # Strategic Positioning section - REPOSITIONED TO AVOID OVERLAP
    try:
        positioning_title = slide_data.get('positioning_title', 'Strategic Market Positioning')
        add_clean_text(slide, Inches(0.8), Inches(5.8), Inches(7), Inches(0.3), 
                       positioning_title, 14, colors["primary"], True)
        
        positioning_desc = slide_data.get('positioning_desc', 
            'The company has established itself as the leading premium healthcare provider in Southeast Asia, '
            'serving both individual patients and corporate clients with comprehensive medical services and exceptional care standards.')
        
        add_clean_text(slide, Inches(0.8), Inches(6.2), Inches(11.5), Inches(0.6), 
                       positioning_desc, 11, colors["text"])
    except Exception as e:
        print(f"[DEBUG] Positioning section error: {e}")
    
    # Footer with proper formatting
    footer_top = Inches(7.0)
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Left footer - Confidential with date
    footer_left = slide.shapes.add_textbox(Inches(0.8), footer_top, Inches(4), Inches(0.2))
    footer_left_frame = footer_left.text_frame
    footer_left_p = footer_left_frame.paragraphs[0]
    footer_left_p.text = f"Confidential | {current_date}"
    footer_left_p.alignment = PP_ALIGN.LEFT
    footer_left_run = footer_left_p.runs[0]
    footer_left_run.font.name = fonts["primary_font"]
    footer_left_run.font.size = fonts["small_size"]
    footer_left_run.font.color.rgb = colors["footer_grey"]
    
    # Right footer - Company name
    footer_right = slide.shapes.add_textbox(Inches(9.5), footer_top, Inches(3.5), Inches(0.2))
    footer_right_frame = footer_right.text_frame
    footer_right_p = footer_right_frame.paragraphs[0]
    footer_right_p.text = f"{company_name}"
    footer_right_p.alignment = PP_ALIGN.RIGHT
    footer_right_run = footer_right_p.runs[0]
    footer_right_run.font.name = fonts["primary_font"]
    footer_right_run.font.size = fonts["small_size"]
    footer_right_run.font.color.rgb = colors["footer_grey"]
    
    return prs


def render_precedent_transactions_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Simple, reliable precedent transactions slide
    """
    
    # FIXED: Extract slide_data from data parameter
    slide_data = data or {}
    
    # Create presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add slide
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Extract data
    transactions = slide_data.get('transactions', [])
    
    print(f"[DEBUG] Precedent transactions: Found {len(transactions)} transactions")
    
    if not transactions:
        # STANDARDIZED: Apply header and title even if no data
        title_text = slide_data.get('title', 'Precedent Transactions Analysis')
        _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
        
        # Add placeholder message
        placeholder = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(8), Inches(1))
        placeholder_frame = placeholder.text_frame
        placeholder_frame.text = "Transaction analysis will be displayed here when data is available."
        placeholder_para = placeholder_frame.paragraphs[0]
        placeholder_para.font.name = fonts["primary_font"]
        placeholder_para.font.size = Pt(14)
        placeholder_para.alignment = PP_ALIGN.CENTER
        
        return prs
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Precedent Transactions Analysis')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # For now, let's create a simple visual representation using text boxes
    # This eliminates matplotlib corruption issues
    
    # Chart area placeholder
    chart_title = slide.shapes.add_textbox(Inches(2.0), Inches(1.5), Inches(9.0), Inches(0.5))
    chart_title_frame = chart_title.text_frame
    chart_title_frame.text = "EV/Revenue Multiples by Transaction"
    chart_title_para = chart_title_frame.paragraphs[0]
    chart_title_para.font.name = fonts["primary_font"]
    chart_title_para.font.size = Pt(14)
    chart_title_para.font.color.rgb = colors["primary"]
    chart_title_para.font.bold = True
    chart_title_para.alignment = PP_ALIGN.CENTER
    
    # Simple bar representation using rectangles
    num_transactions = len(transactions)
    bar_area_left = Inches(2.0)
    bar_area_width = Inches(9.0)
    bar_width = bar_area_width / num_transactions
    bar_top = Inches(2.2)
    
    for i, transaction in enumerate(transactions):
        multiple = transaction.get('ev_revenue_multiple', 0)
        # Scale bar height (max 2 inches for 3.0x multiple)
        bar_height = Inches(multiple * 0.6) if multiple > 0 else Inches(0.1)
        
        bar_left = bar_area_left + (bar_width * i) + Inches(0.05)  # Small margin
        bar_actual_width = bar_width - Inches(0.1)  # Space between bars
        
        # Create bar rectangle
        bar_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            bar_left, bar_top + Inches(2.0) - bar_height, bar_actual_width, bar_height
        )
        bar_shape.fill.solid()
        bar_shape.fill.fore_color.rgb = colors["primary"]
        bar_shape.line.fill.background()
        
        # Add value label
        if multiple > 0:
            label_shape = slide.shapes.add_textbox(
                bar_left, bar_top + Inches(2.0) - bar_height - Inches(0.3), 
                bar_actual_width, Inches(0.25)
            )
            label_frame = label_shape.text_frame
            label_frame.text = f"{multiple:.1f}x"
            label_para = label_frame.paragraphs[0]
            label_para.font.name = fonts["primary_font"]
            label_para.font.size = Pt(9)
            label_para.font.bold = True
            label_para.alignment = PP_ALIGN.CENTER
        
        # Add T1, T2, etc. labels
        t_label_shape = slide.shapes.add_textbox(
            bar_left, bar_top + Inches(2.1), bar_actual_width, Inches(0.25)
        )
        t_label_frame = t_label_shape.text_frame
        t_label_frame.text = f"T{i+1}"
        t_label_para = t_label_frame.paragraphs[0]
        t_label_para.font.name = fonts["primary_font"]
        t_label_para.font.size = Pt(9)
        t_label_para.alignment = PP_ALIGN.CENTER
    
    # Create table
    row_labels = ['Date', 'Target', 'Acquirer', 'Country', 'EV ($M)', 'Revenue ($M)', 'EV/Revenue']
    num_rows = len(row_labels)
    
    # Table positioning - aligned with bars
    labels_left = Inches(0.5)
    labels_width = Inches(1.4)
    table_left = Inches(2.0)  # Same as bar area
    table_top = Inches(4.8)
    table_width = Inches(9.0)  # Same as bar area
    row_height = Inches(0.35)
    
    # Create row labels table
    labels_table = slide.shapes.add_table(
        num_rows, 1, 
        labels_left, table_top, 
        labels_width, row_height * num_rows
    ).table
    
    # Create data table
    data_table = slide.shapes.add_table(
        num_rows, num_transactions, 
        table_left, table_top, 
        table_width, row_height * num_rows
    ).table
    
    # Format row labels
    for i, label in enumerate(row_labels):
        cell = labels_table.cell(i, 0)
        cell.text = label
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["light_grey"]
        
        para = cell.text_frame.paragraphs[0]
        para.font.name = fonts["primary_font"]
        para.font.size = Pt(12)
        para.font.color.rgb = colors["text"]
        para.font.bold = True
        para.alignment = PP_ALIGN.RIGHT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Format data table
    for col_idx, transaction in enumerate(transactions):
        target = transaction.get('target', 'N/A')
        acquirer = transaction.get('acquirer', 'N/A')
        
        # Truncate long names
        if len(target) > 15:
            target = target[:15] + '...'
        if len(acquirer) > 15:
            acquirer = acquirer[:15] + '...'
            
        data_values = [
            transaction.get('date', 'N/A'),
            target,
            acquirer,
            transaction.get('country', 'N/A'),
            f"${transaction.get('enterprise_value', 0):,.0f}" if transaction.get('enterprise_value') else 'N/A',
            f"${transaction.get('revenue', 0):,.0f}" if transaction.get('revenue') else 'N/A',
            f"{transaction.get('ev_revenue_multiple', 0):.1f}x" if transaction.get('ev_revenue_multiple') else 'N/A'
        ]
        
        for row_idx, value in enumerate(data_values):
            cell = data_table.cell(row_idx, col_idx)
            cell.text = str(value)
            
            cell.fill.solid()
            cell.fill.fore_color.rgb = colors["background"]
            
            para = cell.text_frame.paragraphs[0]
            para.font.name = fonts["primary_font"]
            para.font.size = Pt(9)
            para.font.color.rgb = colors["text"]
            para.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Add footer
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.text = f"Confidential | {datetime.now().strftime('%B %Y')}"
    footer_left_para = footer_left_frame.paragraphs[0]
    footer_left_para.font.name = fonts["primary_font"]
    footer_left_para.font.size = fonts["small_size"]
    footer_left_para.font.color.rgb = colors["footer_grey"]
    
    footer_right = slide.shapes.add_textbox(Inches(7.333), Inches(7.0), Inches(6), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.text = company_name
    footer_right_para = footer_right_frame.paragraphs[0]
    footer_right_para.font.name = fonts["primary_font"]
    footer_right_para.font.size = fonts["small_size"]
    footer_right_para.font.color.rgb = colors["footer_grey"]
    footer_right_para.alignment = PP_ALIGN.RIGHT
    
    return prs


def render_valuation_overview_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a valuation overview slide with properly formatted text in boxes
    """
    
    # Helper functions
    def get_section_color(section_type, colors):
        """Get color for methodology section"""
        if section_type == 'precedent_transactions':
            return colors["primary"]
        elif section_type == 'trading_comps':
            return RGBColor(70, 100, 140)  # Medium blue
        elif section_type == 'dcf':
            return RGBColor(50, 80, 50)  # Dark green
        else:
            return colors["primary"]
    
    def get_section_name(section_type):
        """Get display name for methodology section"""
        if section_type == 'precedent_transactions':
            return 'PRECEDENT TRANSACTIONS'
        elif section_type == 'trading_comps':
            return 'TRADING COMPS'
        elif section_type == 'dcf':
            return 'DCF'
        else:
            return 'METHODOLOGY'
    
    # Create presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add slide
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Extract data - handle both direct data and nested structure
    if data is None:
        data = {}
    
    title_text = data.get('title', 'Valuation Overview')
    subtitle_text = data.get('subtitle', 'Implied EV/Post IRFS-16 EBITDA')
    valuation_data = data.get('valuation_data', [])
    
    # Debug print to see what data we're getting
    print(f"[DEBUG] Valuation slide data keys: {list(data.keys())}")
    print(f"[DEBUG] Valuation data length: {len(valuation_data)}")
    if valuation_data:
        print(f"[DEBUG] First valuation item keys: {list(valuation_data[0].keys())}")
    
    # If no valuation data, create a simple slide with title
    if not valuation_data:
        print("[DEBUG] No valuation data found, creating basic slide")
        
        # STANDARDIZED: Apply header and title
        _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
        
        # Add message about missing data
        message_box = slide.shapes.add_textbox(Inches(2), Inches(2), Inches(9), Inches(1))
        message_frame = message_box.text_frame
        message_frame.text = "Valuation data will be displayed here when available."
        message_para = message_frame.paragraphs[0]
        message_para.alignment = PP_ALIGN.CENTER
        message_para.font.name = fonts["primary_font"]
        message_para.font.size = Pt(14)
        message_para.font.color.rgb = colors["text"]
        
        # Add footer
        footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
        footer_left_frame = footer_left.text_frame
        footer_left_frame.text = f"Confidential | {datetime.now().strftime('%B %Y')}"
        footer_left_para = footer_left_frame.paragraphs[0]
        footer_left_para.font.name = fonts["primary_font"]
        footer_left_para.font.size = fonts["small_size"]
        footer_left_para.font.color.rgb = colors["footer_grey"]
        footer_left_para.alignment = PP_ALIGN.LEFT
        
        footer_right = slide.shapes.add_textbox(Inches(7.333), Inches(7.0), Inches(6), Inches(0.4))
        footer_right_frame = footer_right.text_frame
        footer_right_frame.text = company_name
        footer_right_para = footer_right_frame.paragraphs[0]
        footer_right_para.font.name = fonts["primary_font"]
        footer_right_para.font.size = fonts["small_size"]
        footer_right_para.font.color.rgb = colors["footer_grey"]
        footer_right_para.alignment = PP_ALIGN.RIGHT
        
        return prs
    
    # STANDARDIZED: Apply header and title
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Add subtitle header for EBITDA columns
    sub_header_x = Inches(7.8)
    sub_header_width = Inches(4.0)
    sub_header_box = slide.shapes.add_textbox(sub_header_x, Inches(1.1), sub_header_width, Inches(0.25))
    sub_header_frame = sub_header_box.text_frame
    sub_header_frame.text = subtitle_text
    sub_header_frame.margin_left = Inches(0.05)
    sub_header_frame.margin_right = Inches(0.05)
    
    sub_header_para = sub_header_frame.paragraphs[0]
    sub_header_para.alignment = PP_ALIGN.CENTER
    sub_header_para.font.name = fonts["primary_font"]
    sub_header_para.font.size = fonts["body_size"]
    sub_header_para.font.bold = True
    sub_header_para.font.color.rgb = colors["primary"]
    
    # Table positioning - better centered
    table_start_x = Inches(1.2)
    table_start_y = Inches(1.4)
    
    # Adjusted column widths for better text formatting
    col_widths = [
        Inches(2.2),  # Methodology - slightly smaller
        Inches(3.6),  # Commentary - larger for better text flow
        Inches(1.8),  # Enterprise Value
        Inches(1.6),  # Metric
        Inches(1.0),  # 22A'
        Inches(1.0)   # 23E (Rev)
    ]
    
    # Column headers
    headers = ["Methodology", "Commentary", "Enterprise Value", "Metric", "22A'", "23E (Rev)"]
    header_height = Inches(0.5)
    
    current_x = table_start_x
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        # Header background
        header_bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            current_x, table_start_y, width, header_height
        )
        header_bg.fill.solid()
        header_bg.fill.fore_color.rgb = colors["primary"]
        header_bg.line.color.rgb = colors["primary"]
        
        # Header text with better formatting
        header_text = slide.shapes.add_textbox(current_x, table_start_y, width, header_height)
        header_text_frame = header_text.text_frame
        header_text_frame.text = header
        header_text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        header_text_frame.margin_left = Inches(0.08)
        header_text_frame.margin_right = Inches(0.08)
        header_text_frame.margin_top = Inches(0.05)
        header_text_frame.margin_bottom = Inches(0.05)
        
        para = header_text_frame.paragraphs[0]
        para.alignment = PP_ALIGN.CENTER
        para.font.name = fonts["primary_font"]
        para.font.size = fonts["header_size"]
        para.font.bold = True
        para.font.color.rgb = colors["background"]
        
        current_x += width
    
    # Create data rows with better formatting
    row_height = Inches(0.8)  # Increased height for better text formatting
    current_y = table_start_y + header_height
    
    # Track methodology sections
    methodology_sections = []
    current_section = None
    section_start_y = current_y
    section_row_count = 0
    
    for row_idx, row_data in enumerate(valuation_data):
        current_x = table_start_x
        
        # Determine row color
        methodology_type = row_data.get('methodology_type', 'precedent_transactions')
        row_color = get_section_color(methodology_type, colors)
        
        # Track sections
        if current_section != methodology_type:
            if current_section is not None:
                methodology_sections.append((current_section, section_start_y, section_row_count, get_section_color(current_section, colors)))
            current_section = methodology_type
            section_start_y = current_y
            section_row_count = 1
        else:
            section_row_count += 1
        
        # Create cell data
        cell_data = [
            row_data.get('methodology', ''),
            row_data.get('commentary', ''),
            row_data.get('enterprise_value', ''),
            row_data.get('metric', ''),
            row_data.get('22a_multiple', ''),
            row_data.get('23e_multiple', '')
        ]
        
        for col_idx, (cell_text, width) in enumerate(zip(cell_data, col_widths)):
            # Cell background
            cell_bg = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                current_x, current_y, width, row_height
            )
            
            # Set cell formatting based on column
            if col_idx == 0:  # Methodology column
                cell_bg.fill.solid()
                cell_bg.fill.fore_color.rgb = row_color
                text_color = colors["background"]
                bold = True
                font_size = fonts["body_size"]
                alignment = PP_ALIGN.CENTER
            elif col_idx == 1:  # Commentary column
                cell_bg.fill.solid()
                cell_bg.fill.fore_color.rgb = colors["light_grey"]
                text_color = colors["text"]
                bold = False
                font_size = Pt(9)
                alignment = PP_ALIGN.LEFT
            else:  # Data columns
                cell_bg.fill.solid()
                cell_bg.fill.fore_color.rgb = colors["background"]
                text_color = colors["text"]
                bold = False
                font_size = fonts["body_size"]
                alignment = PP_ALIGN.CENTER
            
            cell_bg.line.color.rgb = RGBColor(128, 128, 128)
            cell_bg.line.width = Pt(0.5)
            
            # Create text box with proper formatting
            cell_text_box = slide.shapes.add_textbox(current_x, current_y, width, row_height)
            cell_text_frame = cell_text_box.text_frame
            cell_text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell_text_frame.margin_left = Inches(0.1)
            cell_text_frame.margin_right = Inches(0.1)
            cell_text_frame.margin_top = Inches(0.08)
            cell_text_frame.margin_bottom = Inches(0.08)
            cell_text_frame.word_wrap = True
            cell_text_frame.auto_size = None
            
            # Clear default text first
            cell_text_frame.clear()
            
            # Add properly formatted text
            para = cell_text_frame.paragraphs[0]
            para.text = cell_text
            para.alignment = alignment
            para.font.name = fonts["primary_font"]
            para.font.size = font_size
            para.font.bold = bold
            para.font.color.rgb = text_color
            para.line_spacing = 1.1  # Better line spacing
            
            # Handle long commentary text with better formatting
            if col_idx == 1 and len(cell_text) > 80:
                # Split at natural break points
                if '. ' in cell_text:
                    sentences = cell_text.split('. ')
                    para.text = sentences[0] + '.'
                    
                    for sentence in sentences[1:]:
                        if sentence.strip():
                            new_para = cell_text_frame.add_paragraph()
                            new_para.text = sentence + ('.' if not sentence.endswith('.') else '')
                            new_para.alignment = alignment
                            new_para.font.name = fonts["primary_font"]
                            new_para.font.size = font_size
                            new_para.font.bold = bold
                            new_para.font.color.rgb = text_color
                            new_para.line_spacing = 1.1
            
            current_x += width
        
        current_y += row_height
    
    # Add final section
    if current_section is not None:
        methodology_sections.append((current_section, section_start_y, section_row_count, get_section_color(current_section, colors)))
    
    # Add vertical methodology labels
    label_x = Inches(0.2)
    label_width = Inches(0.9)
    
    for section_type, start_y, row_count, section_color in methodology_sections:
        section_height = row_count * row_height
        section_name = get_section_name(section_type)
        
        # Background rectangle
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            label_x, start_y, label_width, section_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = section_color
        bg.line.color.rgb = section_color
        
        # Section label text
        text_box = slide.shapes.add_textbox(label_x, start_y, label_width, section_height)
        text_frame = text_box.text_frame
        text_frame.text = section_name
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        text_frame.margin_left = Inches(0.05)
        text_frame.margin_right = Inches(0.05)
        
        para = text_frame.paragraphs[0]
        para.alignment = PP_ALIGN.CENTER
        para.font.name = fonts["primary_font"]
        para.font.size = Pt(8)
        para.font.bold = True
        para.font.color.rgb = colors["background"]
    
    # Add footer
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.text = f"Confidential | {datetime.now().strftime('%B %Y')}"
    footer_left_para = footer_left_frame.paragraphs[0]
    footer_left_para.font.name = fonts["primary_font"]
    footer_left_para.font.size = fonts["small_size"]
    footer_left_para.font.color.rgb = colors["footer_grey"]
    footer_left_para.alignment = PP_ALIGN.LEFT
    
    footer_right = slide.shapes.add_textbox(Inches(7.333), Inches(7.0), Inches(6), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.text = company_name
    footer_right_para = footer_right_frame.paragraphs[0]
    footer_right_para.font.name = fonts["primary_font"]
    footer_right_para.font.size = fonts["small_size"]
    footer_right_para.font.color.rgb = colors["footer_grey"]
    footer_right_para.alignment = PP_ALIGN.RIGHT
    
    return prs


def render_growth_strategy_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a growth strategy & financial projections slide
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Helper function
    def add_clean_text(slide, left, top, width, height, text, font_size=10, 
                       color=colors["text"], bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        return textbox
    
    # Extract slide data - handle nested structure
    slide_info = data or {}
    if 'slide_data' in slide_info:
        slide_data = slide_info['slide_data']
    else:
        slide_data = slide_info
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Growth Strategy & Financial Projections')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Growth Strategy section
    growth_strategy = slide_data.get('growth_strategy', {})
    if growth_strategy:
        add_clean_text(slide, Inches(0.5), Inches(1.4), Inches(6), Inches(0.3), 
                       growth_strategy.get('title', 'Multi-Pronged Growth Strategy'), 
                       14, colors["primary"], True)
        
        strategies = growth_strategy.get('strategies', [])
        for i, strategy in enumerate(strategies[:6]):  # Max 6 strategies
            y_pos = Inches(1.8 + i * 0.35)
            
            # Gold bullet
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), y_pos, Inches(0.06), Inches(0.06))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            bullet.shadow.inherit = False
            
            # Strategy text
            add_clean_text(slide, Inches(0.85), y_pos - Inches(0.05), Inches(5.5), Inches(0.3), 
                           strategy, 9, colors["text"])
    
    # Financial Projections Chart
    projections = slide_data.get('financial_projections', {})
    if projections:
        chart_title = projections.get('chart_title', 'Revenue & EBITDA Projections')
        add_clean_text(slide, Inches(7.5), Inches(1.4), Inches(5.5), Inches(0.3), 
                       chart_title, 14, colors["primary"], True)
        
        # Create chart if we have data
        categories = projections.get('categories', [])
        revenue_data = projections.get('revenue', [])
        ebitda_data = projections.get('ebitda', [])
        
        if categories and revenue_data and ebitda_data:
            try:
                chart_data = ChartData()
                chart_data.categories = categories
                chart_data.add_series('Revenue (USD millions)', revenue_data)
                chart_data.add_series('EBITDA (USD millions)', ebitda_data)
                
                # Add chart
                chart_left = Inches(7.5)
                chart_top = Inches(1.8)
                chart_width = Inches(5.5)
                chart_height = Inches(2.5)
                
                chart_shape = slide.shapes.add_chart(
                    XL_CHART_TYPE.COLUMN_CLUSTERED, chart_left, chart_top, chart_width, chart_height, chart_data
                )
                
                chart = chart_shape.chart
                chart.has_legend = True
                chart.legend.position = XL_LEGEND_POSITION.BOTTOM
                
                # Style chart
                series = chart.series
                # Revenue series (primary color)
                series[0].format.fill.solid()
                series[0].format.fill.fore_color.rgb = colors["primary"]
                
                # EBITDA series (secondary color)
                series[1].format.fill.solid() 
                series[1].format.fill.fore_color.rgb = colors["secondary"]
                
            except Exception as e:
                print(f"[DEBUG] Chart creation error: {e}")
                add_clean_text(slide, Inches(7.5), Inches(2.5), Inches(5.5), Inches(1), 
                               "Financial projections chart will be displayed here.", 12, colors["text"])
    
    # Key Assumptions
    assumptions = slide_data.get('key_assumptions', {})
    if assumptions:
        add_clean_text(slide, Inches(0.5), Inches(4.8), Inches(12.5), Inches(0.3), 
                       assumptions.get('title', 'Key Planning Assumptions'), 14, colors["primary"], True)
        
        assumption_items = assumptions.get('assumptions', [])
        # Split into two columns
        left_items = assumption_items[:3]
        right_items = assumption_items[3:]
        
        # Left column
        for i, assumption in enumerate(left_items):
            y_pos = Inches(5.2 + i * 0.3)
            
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), y_pos, Inches(0.05), Inches(0.05))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            add_clean_text(slide, Inches(0.85), y_pos - Inches(0.05), Inches(5.8), Inches(0.25), 
                           assumption, 9, colors["text"])
        
        # Right column
        for i, assumption in enumerate(right_items):
            y_pos = Inches(5.2 + i * 0.3)
            
            bullet = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.2), y_pos, Inches(0.05), Inches(0.05))
            bullet.fill.solid()
            bullet.fill.fore_color.rgb = colors["secondary"]
            bullet.line.fill.background()
            
            add_clean_text(slide, Inches(7.35), y_pos - Inches(0.05), Inches(5.8), Inches(0.25), 
                           assumption, 9, colors["text"])
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(7.0), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs

def render_buyer_profiles_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a buyer profiles slide with table layout
    """
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Add blank slide
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Helper function
    def add_clean_text(slide, left, top, width, height, text, font_size=10, 
                       color=colors["text"], bold=False, align=PP_ALIGN.LEFT, bg_color=None):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.margin_left = Inches(0.1)
        text_frame.margin_right = Inches(0.1)
        text_frame.margin_top = Inches(0.05)
        text_frame.margin_bottom = Inches(0.05)
        text_frame.word_wrap = True
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(font_size)
                run.font.color.rgb = color
                run.font.bold = bold
        
        if bg_color:
            textbox.fill.solid()
            textbox.fill.fore_color.rgb = bg_color
        
        textbox.line.fill.background()
        textbox.shadow.inherit = False
        return textbox
    
    # Extract slide data
    slide_data = data or {}
    
    # STANDARDIZED: Apply header and title
    title_text = slide_data.get('title', 'Potential Strategic Buyers')
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Subtitle if provided
    subtitle = slide_data.get('subtitle', '')
    if subtitle:
        add_clean_text(slide, Inches(0.5), Inches(1.2), Inches(12), Inches(0.3), 
                       subtitle, 12, colors["accent"], False, PP_ALIGN.LEFT)
    
    # Get table data
    table_rows = slide_data.get('table_rows', [])
    table_headers = slide_data.get('table_headers', ['Buyer Profile', 'Strategic Rationale', 'Key Synergies', 'Concerns', 'Fit'])
    
    if table_rows:
        # Create table
        table_top = Inches(1.6)
        table_left = Inches(0.5)
        table_width = Inches(12.5)
        
        # Calculate rows needed
        num_rows = len(table_rows) + 1  # +1 for header
        num_cols = len(table_headers)
        
        # Adjust height based on number of rows
        row_height = Inches(0.8) if len(table_rows) <= 3 else Inches(0.6)
        table_height = row_height * num_rows
        
        # Create table
        table_shape = slide.shapes.add_table(num_rows, num_cols, table_left, table_top, table_width, table_height)
        table = table_shape.table
        
        # Set column widths
        if num_cols == 5:
            col_widths = [Inches(2.8), Inches(2.5), Inches(2.5), Inches(2.2), Inches(1.5)]
        else:
            # Distribute evenly
            col_width = table_width / num_cols
            col_widths = [col_width] * num_cols
        
        for i, width in enumerate(col_widths):
            table.columns[i].width = width
        
        # Format header row
        for j, header in enumerate(table_headers):
            cell = table.cell(0, j)
            cell.text = header
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)
            
            # Header styling
            cell.fill.solid()
            cell.fill.fore_color.rgb = colors["primary"]
            
            for paragraph in cell.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                for run in paragraph.runs:
                    run.font.name = fonts["primary_font"]
                    run.font.size = fonts["body_size"]
                    run.font.bold = True
                    run.font.color.rgb = colors["background"]
        
        # Format data rows
        for i, row_data in enumerate(table_rows):
            row_idx = i + 1
            
            # Handle different data formats
            if isinstance(row_data, dict):
                # Convert dict to list based on expected fields
                cell_data = [
                    row_data.get('buyer_name', row_data.get('name', '')),
                    row_data.get('strategic_rationale', row_data.get('rationale', '')),
                    row_data.get('key_synergies', row_data.get('synergies', '')),
                    row_data.get('concerns', ''),
                    row_data.get('fit_score', row_data.get('fit', ''))
                ]
            elif isinstance(row_data, list):
                cell_data = row_data
            else:
                continue
            
            for j, cell_text in enumerate(cell_data):
                if j < num_cols:
                    cell = table.cell(row_idx, j)
                    cell.text = str(cell_text)
                    cell.margin_left = Inches(0.05)
                    cell.margin_right = Inches(0.05)
                    cell.margin_top = Inches(0.05)
                    cell.margin_bottom = Inches(0.05)
                    
                    # Alternate row colors
                    if row_idx % 2 == 0:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = colors["light_grey"]
                    else:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = colors["background"]
                    
                    # Text styling
                    cell.text_frame.word_wrap = True
                    for paragraph in cell.text_frame.paragraphs:
                        paragraph.alignment = PP_ALIGN.LEFT
                        for run in paragraph.runs:
                            run.font.name = fonts["primary_font"]
                            run.font.size = Pt(9)
                            run.font.color.rgb = colors["text"]
                            # Make first column (buyer name) bold
                            if j == 0:
                                run.font.bold = True
    
    else:
        # No data - add placeholder
        add_clean_text(slide, Inches(2), Inches(3), Inches(9), Inches(1), 
                       "Buyer profiles data will be displayed here when available.", 
                       14, colors["text"], False, PP_ALIGN.CENTER)
    
    # Get today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Add footer
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.clear()
    p = footer_left_frame.paragraphs[0]
    p.text = f"Confidential | {today}"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.LEFT
    footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    footer_right = slide.shapes.add_textbox(Inches(10), Inches(7.0), Inches(3), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.clear()
    p = footer_right_frame.paragraphs[0]
    p.text = company_name or "Moelis"
    p.font.name = fonts["primary_font"]
    p.font.size = fonts["small_size"]
    p.font.color.rgb = colors["footer_grey"]
    p.alignment = PP_ALIGN.RIGHT
    footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs


def render_sea_conglomerates_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Render SEA conglomerates slide with brand configuration support
    """
    
    # FIXED: Extract slide_data from data parameter
    # Handle both list format and dict format
    if isinstance(data, list):
        slide_data = data
    elif isinstance(data, dict):
        slide_data = data.get('conglomerates', data.get('data', []))
    else:
        slide_data = []
    
    print(f"[DEBUG] SEA conglomerates: Found {len(slide_data)} companies")
    print(f"[DEBUG] First company data: {slide_data[0] if slide_data else 'No data'}")
    
    # Default data if none provided
    if not slide_data:
        slide_data = [
            {
                "name": "Ayala Corporation",
                "country": "Philippines",
                "description": "Leading diversified conglomerate with significant healthcare investments through Ayala Healthcare Holdings",
                "key_shareholders": "Ayala family trust and institutional investors",
                "key_financials": "Revenue: US$3.2B, Healthcare growing 15%+ annually",
                "moelis_contact": "Managing Director - SEA Healthcare"
            },
            {
                "name": "CP Group (Charoen Pokphand)",
                "country": "Thailand",
                "description": "Massive diversified conglomerate with healthcare retail exposure through pharmacy chains",
                "key_shareholders": "Chearavanont family and holding companies",
                "key_financials": "Revenue: US$45B+, Healthcare investments >US$500M",
                "moelis_contact": "Managing Director - Consumer Healthcare"
            },
            {
                "name": "Sinar Mas Group",
                "country": "Indonesia",
                "description": "Indonesian conglomerate with diversified portfolio and growing healthcare technology investments",
                "key_shareholders": "Widjaja family and investment vehicles",
                "key_financials": "Revenue: US$15B+, Active healthtech program",
                "moelis_contact": "Executive Director - Indonesia Coverage"
            },
            {
                "name": "Genting Group",
                "country": "Malaysia",
                "description": "Diversified conglomerate with strategic healthcare investments through integrated resort wellness",
                "key_shareholders": "Lim Kok Thay family trust",
                "key_financials": "Revenue: US$2.8B, Healthcare target US$200M+",
                "moelis_contact": "Managing Director - Malaysia Coverage"
            }
        ]
    
    # Create or use existing presentation
    if prs is None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs = ensure_prs(prs)
    
    # Get brand styling
    colors, fonts = get_brand_styling(brand_config, color_scheme, typography)
    
    # Pagination: Split data into chunks of 4
    max_entries_per_slide = 4
    slide_chunks = []
    
    for i in range(0, len(slide_data), max_entries_per_slide):
        chunk = slide_data[i:i + max_entries_per_slide]
        slide_chunks.append(chunk)
    
    # Create slides for each chunk
    for slide_index, chunk_data in enumerate(slide_chunks):
        # Add blank slide
        slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Title with pagination info
        title_text = "SEA Conglomerate Strategic Buyers"
        if len(slide_chunks) > 1:
            title_text += f" (cont'd)" if slide_index > 0 else ""
        
        # STANDARDIZED: Apply header and title
        _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
        
        # Table dimensions and positioning
        table_left = Inches(0.5)
        table_top = Inches(1.5)
        table_width = Inches(12.333)
        table_height = Inches(5.0)
        
        # Calculate number of rows (header + data rows)
        num_rows = len(chunk_data) + 1
        num_cols = 6
        
        # Create table
        table_shape = slide.shapes.add_table(num_rows, num_cols, table_left, table_top, table_width, table_height)
        table = table_shape.table
        
        # Column headers
        headers = ["Name", "Country", "Description", "Key shareholders", "Key financials (US$m)", "Moelis contact"]
        
        # Set column widths to match original
        col_widths = [Inches(1.8), Inches(1.0), Inches(4.2), Inches(2.2), Inches(1.8), Inches(1.333)]
        for i, width in enumerate(col_widths):
            table.columns[i].width = width
        
        # Format header row - DARK BLUE BACKGROUND
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            # DARK BLUE BACKGROUND
            cell.fill.solid()
            cell.fill.fore_color.rgb = colors["primary"]
            
            # Header text
            cell.text = header
            cell.text_frame.margin_left = Inches(0.1)
            cell.text_frame.margin_right = Inches(0.1)
            cell.text_frame.margin_top = Inches(0.05)
            cell.text_frame.margin_bottom = Inches(0.05)
            
            # Header formatting - WHITE TEXT on dark blue background
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.name = fonts["primary_font"]
                paragraph.font.size = fonts["header_size"]
                paragraph.font.bold = True
                paragraph.font.color.rgb = colors["background"]  # WHITE text on dark blue
                paragraph.alignment = PP_ALIGN.CENTER
        
        # Populate data rows - WHITE BACKGROUND
        for row_idx, company in enumerate(chunk_data, 1):
            # Define the data for each column - handle different data structures
            row_data = [
                company.get('name', ''),
                company.get('country', ''),
                company.get('description', company.get('healthcare_focus', '')),  # Fallback to healthcare_focus
                company.get('key_shareholders', 'N/A'),
                company.get('key_financials', company.get('revenue', '')),  # Fallback to revenue
                company.get('moelis_contact', 'To be assigned')
            ]
            
            for col_idx, data in enumerate(row_data):
                cell = table.cell(row_idx, col_idx)
                cell.text = str(data)
                
                # WHITE BACKGROUND
                cell.fill.solid()
                cell.fill.fore_color.rgb = colors["background"]
                
                # Cell margins
                cell.text_frame.margin_left = Inches(0.1)
                cell.text_frame.margin_right = Inches(0.1)
                cell.text_frame.margin_top = Inches(0.05)
                cell.text_frame.margin_bottom = Inches(0.05)
                
                # Text wrapping
                cell.text_frame.word_wrap = True
                
                # Text formatting - BLACK TEXT
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.font.name = fonts["primary_font"]
                    paragraph.font.size = fonts["body_size"]
                    paragraph.font.bold = False
                    paragraph.font.color.rgb = colors["text"]
                    paragraph.alignment = PP_ALIGN.LEFT
        
        # Set row heights
        header_row_height = Inches(0.6)
        data_row_height = Inches(1.1)
        
        # Set header row height
        table.rows[0].height = header_row_height
        
        # Set data row heights
        for i in range(1, num_rows):
            table.rows[i].height = data_row_height
        
        # Get today's date
        today = datetime.now().strftime("%B %d, %Y")
        
        # Add footer
        footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
        footer_left_frame = footer_left.text_frame
        footer_left_frame.clear()
        p = footer_left_frame.paragraphs[0]
        p.text = f"Confidential | {today}"
        p.font.name = fonts["primary_font"]
        p.font.size = fonts["small_size"]
        p.font.color.rgb = colors["footer_grey"]
        p.alignment = PP_ALIGN.LEFT
        footer_left_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        footer_right = slide.shapes.add_textbox(Inches(10), Inches(7.0), Inches(3), Inches(0.4))
        footer_right_frame = footer_right.text_frame
        footer_right_frame.clear()
        p = footer_right_frame.paragraphs[0]
        p.text = company_name or "Moelis"
        p.font.name = fonts["primary_font"]
        p.font.size = fonts["small_size"]
        p.font.color.rgb = colors["footer_grey"]
        p.alignment = PP_ALIGN.RIGHT
        footer_right_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return prs