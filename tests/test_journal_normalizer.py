from scripts.parsers.normalize import normalize_guidelines

SAMPLE = """
The main text should be no more than 3000 words. Abstract up to 150 words.
References should be numbered in superscript (Vancouver).
Up to 4 figures and 2 tables are allowed. Images at least 300 dpi, width 86 mm.
Sections: Abstract, Introduction, Methods, Results, Discussion, References, Supplementary Information.
"""

def test_normalize_minimal_contract():
    d = normalize_guidelines(SAMPLE)
    assert d["word_counts"]["main"] == 3000
    assert d["word_counts"]["abstract"] == 150
    assert "Vancouver" in d["refs_style"]
    assert d["figures_limits"]["max"] == 4
    assert d["tables_limits"]["max"] == 2
    assert d["image_specs"]["dpi"] == 300
    assert 86 in (d["image_specs"]["width_mm"], d["image_specs"].get("width_mm"))
    assert "Methods" in d["sections"]

def test_word_counts_extraction():
    text = "Manuscripts should not exceed 2500 words. Abstract limited to 200 words maximum."
    d = normalize_guidelines(text)
    assert d["word_counts"]["main"] == 2500
    assert d["word_counts"]["abstract"] == 200

def test_reference_style_detection():
    vancouver_text = "References should be numbered consecutively in superscript (Vancouver style)."
    harvard_text = "Use author-year citation format (Harvard style)."
    
    d1 = normalize_guidelines(vancouver_text)
    d2 = normalize_guidelines(harvard_text)
    
    assert "Vancouver" in d1["refs_style"]
    assert "superscript" in d1["refs_style"] 
    assert "Harvard" in d2["refs_style"]

def test_figure_table_limits():
    text = "Maximum of 6 figures and 3 tables allowed."
    d = normalize_guidelines(text)
    assert d["figures_limits"]["max"] == 6
    assert d["tables_limits"]["max"] == 3

def test_image_specs_extraction():
    text = "Images must be at least 600 dpi resolution, width 180 mm."
    d = normalize_guidelines(text)
    assert d["image_specs"]["dpi"] == 600
    assert d["image_specs"]["width_mm"] == 180