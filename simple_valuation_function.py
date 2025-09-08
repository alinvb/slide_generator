def render_valuation_overview_slide(data=None, color_scheme=None, typography=None, company_name="Moelis", prs=None, brand_config=None, **kwargs):
    """
    Renders a clean, simple valuation overview slide with a standard table format
    """
    
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
    if data is None:
        data = {}
    
    title_text = data.get('title', 'Valuation Overview')
    subtitle_text = data.get('subtitle', 'Implied EV/Post IRFS-16 EBITDA')
    valuation_data = data.get('valuation_data', [])
    
    print(f"[DEBUG] Valuation slide - {len(valuation_data)} data rows")
    
    # STANDARDIZED: Apply header and title
    _apply_standard_header_and_title(slide, title_text, brand_config, company_name)
    
    # Add subtitle header
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(1.4), Inches(11), Inches(0.3))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle_text
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.alignment = PP_ALIGN.CENTER
    subtitle_para.font.name = fonts["primary_font"] 
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.bold = True
    subtitle_para.font.color.rgb = colors["primary"]
    
    if not valuation_data:
        # Add message about missing data
        message_box = slide.shapes.add_textbox(Inches(2), Inches(2.5), Inches(9), Inches(1))
        message_frame = message_box.text_frame
        message_frame.text = "Valuation data will be displayed here when available."
        message_para = message_frame.paragraphs[0]
        message_para.alignment = PP_ALIGN.CENTER
        message_para.font.name = fonts["primary_font"]
        message_para.font.size = Pt(14)
        message_para.font.color.rgb = colors["text"]
        
        return prs
    
    # Create simple table
    rows = len(valuation_data) + 1  # +1 for header
    cols = 5  # Methodology, Commentary, Enterprise Value, Metric, 22A'/23E
    
    table_left = Inches(0.5)
    table_top = Inches(1.8) 
    table_width = Inches(12.3)
    table_height = Inches(4.5)
    
    # Create table using PowerPoint's native table functionality
    table = slide.shapes.add_table(rows, cols, table_left, table_top, table_width, table_height).table
    
    # Set column widths
    table.columns[0].width = Inches(2.0)  # Methodology
    table.columns[1].width = Inches(4.5)  # Commentary  
    table.columns[2].width = Inches(2.0)  # Enterprise Value
    table.columns[3].width = Inches(1.5)  # Metric
    table.columns[4].width = Inches(2.3)  # 22A'/23E combined
    
    # Header row
    headers = ["Methodology", "Commentary", "Enterprise Value", "Metric", "22A' / 23E (Rev)"]
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["primary"]
        
        # Format header text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.name = fonts["primary_font"]
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = colors["background"]
    
    # Data rows
    for row_idx, row_data in enumerate(valuation_data, 1):
        print(f"[DEBUG] Processing valuation row {row_idx}: {row_data.get('methodology', '')}")
        
        # Methodology
        cell = table.cell(row_idx, 0)
        cell.text = row_data.get('methodology', '')
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["light_grey"]
        
        # Commentary  
        cell = table.cell(row_idx, 1)
        cell.text = row_data.get('commentary', '')
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["background"]
        
        # Enterprise Value
        cell = table.cell(row_idx, 2)
        cell.text = row_data.get('enterprise_value', '')
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["background"]
        
        # Metric
        cell = table.cell(row_idx, 3)
        cell.text = row_data.get('metric', '')
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["background"]
        
        # 22A' / 23E combined
        cell = table.cell(row_idx, 4)
        a22_val = row_data.get('22a_multiple', '')
        e23_val = row_data.get('23e_multiple', '')
        combined = f"{a22_val} / {e23_val}" if a22_val and e23_val else f"{a22_val}{e23_val}"
        cell.text = combined
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["background"]
        
        # Format all data cell text
        for col_idx in range(cols):
            cell = table.cell(row_idx, col_idx)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT  # Left-align commentary
                for run in paragraph.runs:
                    run.font.name = fonts["primary_font"]
                    run.font.size = Pt(9)
                    run.font.color.rgb = colors["text"]
    
    # Add footer
    footer_left = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(6), Inches(0.4))
    footer_left_frame = footer_left.text_frame
    footer_left_frame.text = f"Confidential | {datetime.now().strftime('%B %Y')}"
    footer_left_para = footer_left_frame.paragraphs[0]
    footer_left_para.font.name = fonts["primary_font"]
    footer_left_para.font.size = Pt(8)
    footer_left_para.font.color.rgb = colors["footer_grey"]
    footer_left_para.alignment = PP_ALIGN.LEFT
    
    footer_right = slide.shapes.add_textbox(Inches(7.333), Inches(7.0), Inches(6), Inches(0.4))
    footer_right_frame = footer_right.text_frame
    footer_right_frame.text = company_name
    footer_right_para = footer_right_frame.paragraphs[0]
    footer_right_para.font.name = fonts["primary_font"]
    footer_right_para.font.size = Pt(8)
    footer_right_para.font.color.rgb = colors["footer_grey"]
    footer_right_para.alignment = PP_ALIGN.RIGHT
    
    return prs

