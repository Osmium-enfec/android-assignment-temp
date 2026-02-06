"""
Assignment 1 Test Suite

Tests for validating Android layout XML files.
Verifies that the activity_main.xml contains a TextView with proper configuration
displaying "Hi Android" text centered on the screen.
"""

import pytest
from pathlib import Path
from lxml import etree
import os
import sys

SUBMISSION_DIR = '/app/submission'

@pytest.fixture
def xml_tree():
    """Load and parse the activity_main.xml file."""
    xml_file = os.path.join(SUBMISSION_DIR, 'activity_main.xml')
    print(f"\n[DEBUG] Looking for XML file at: {xml_file}")
    print(f"[DEBUG] File exists: {os.path.exists(xml_file)}")
    
    if not os.path.exists(xml_file):
        print(f"[DEBUG] Contents of {SUBMISSION_DIR}:")
        if os.path.exists(SUBMISSION_DIR):
            for item in os.listdir(SUBMISSION_DIR):
                print(f"  - {item}")
        else:
            print(f"  Directory does not exist!")
        pytest.skip(f"XML file not found at {xml_file}")
    
    try:
        tree = etree.parse(xml_file)
        print(f"[DEBUG] XML parsed successfully")
        return tree
    except Exception as e:
        print(f"[DEBUG] XML parsing error: {e}")
        raise

@pytest.fixture
def root_element(xml_tree):
    """Get the root element of the XML tree."""
    return xml_tree.getroot()


class TestLayoutStructure:
    """Test the overall layout structure."""
    
    @pytest.mark.layout
    def test_xml_is_wellformed(self, xml_tree):
        """Test that the XML is well-formed and parseable."""
        assert xml_tree is not None, "XML file could not be parsed"
    
    @pytest.mark.layout
    def test_has_root_layout(self, root_element):
        """Test that the XML has a root layout element."""
        assert root_element.tag in ['LinearLayout', 'RelativeLayout', 'FrameLayout'], \
            f"Root element should be a layout, got {root_element.tag}"
    
    @pytest.mark.layout
    def test_layout_has_match_parent_dimensions(self, root_element):
        """Test that the root layout has match_parent dimensions."""
        width = root_element.get('{http://schemas.android.com/apk/res/android}layout_width')
        height = root_element.get('{http://schemas.android.com/apk/res/android}layout_height')
        
        assert width == 'match_parent', f"Layout width should be match_parent, got {width}"
        assert height == 'match_parent', f"Layout height should be match_parent, got {height}"


class TestTextView:
    """Test the TextView implementation."""
    
    @pytest.mark.textview
    def test_has_textview(self, root_element):
        """Test that the layout contains a TextView element."""
        textviews = root_element.findall('.//{http://schemas.android.com/apk/res/android}TextView')
        if not textviews:
            textviews = root_element.findall('.//TextView')
        assert len(textviews) > 0, "No TextView found in the layout"
    
    @pytest.mark.textview
    def test_textview_displays_hi_android(self, root_element):
        """Test that the TextView displays 'Hi Android' text."""
        textviews = root_element.findall('.//{http://schemas.android.com/apk/res/android}TextView')
        if not textviews:
            textviews = root_element.findall('.//TextView')
        
        text_found = False
        for textview in textviews:
            text = textview.get('{http://schemas.android.com/apk/res/android}text')
            if not text:
                text = textview.get('text')
            if text and 'Hi Android' in text:
                text_found = True
                break
        
        assert text_found, "No TextView with 'Hi Android' text found"
    
    @pytest.mark.textview
    def test_textview_has_wrap_content_dimensions(self, root_element):
        """Test that the TextView uses wrap_content for dimensions."""
        textviews = root_element.findall('.//{http://schemas.android.com/apk/res/android}TextView')
        if not textviews:
            textviews = root_element.findall('.//TextView')
        
        assert len(textviews) > 0, "No TextView found"
        
        first_textview = textviews[0]
        width = first_textview.get('{http://schemas.android.com/apk/res/android}layout_width')
        if not width:
            width = first_textview.get('layout_width')
        height = first_textview.get('{http://schemas.android.com/apk/res/android}layout_height')
        if not height:
            height = first_textview.get('layout_height')
        
        assert width == 'wrap_content', f"TextView width should be wrap_content, got {width}"
        assert height == 'wrap_content', f"TextView height should be wrap_content, got {height}"
    
    @pytest.mark.textview
    def test_textview_has_adequate_text_size(self, root_element):
        """Test that the TextView has a reasonable text size (at least 24sp)."""
        textviews = root_element.findall('.//{http://schemas.android.com/apk/res/android}TextView')
        if not textviews:
            textviews = root_element.findall('.//TextView')
        
        assert len(textviews) > 0, "No TextView found"
        
        first_textview = textviews[0]
        text_size = first_textview.get('{http://schemas.android.com/apk/res/android}textSize')
        if not text_size:
            text_size = first_textview.get('textSize')
        
        if text_size:
            # Extract numeric value
            size_value = int(''.join(filter(str.isdigit, text_size)))
            assert size_value >= 24, f"Text size should be at least 24sp, got {text_size}"
        # If no textSize specified, it's acceptable (default is used)


class TestCentering:
    """Test that content is properly centered."""
    
    @pytest.mark.layout
    def test_layout_is_centered(self, root_element):
        """Test that the root layout is configured for centering content."""
        gravity = root_element.get('{http://schemas.android.com/apk/res/android}gravity')
        
        assert gravity is not None, "Root layout should have gravity attribute"
        assert 'center' in gravity.lower(), \
            f"Layout should have center gravity, got {gravity}"


class TestSmokeTests:
    """Basic smoke tests to verify functionality."""
    
    @pytest.mark.smoke
    def test_file_exists(self):
        """Test that activity_main.xml file exists."""
        xml_file = os.path.join(SUBMISSION_DIR, 'activity_main.xml')
        assert os.path.exists(xml_file), f"File {xml_file} does not exist"
    
    @pytest.mark.smoke
    def test_file_is_valid_xml(self):
        """Test that the file is valid XML."""
        xml_file = os.path.join(SUBMISSION_DIR, 'activity_main.xml')
        try:
            etree.parse(xml_file)
            assert True
        except Exception as e:
            pytest.fail(f"XML parsing failed: {str(e)}")
