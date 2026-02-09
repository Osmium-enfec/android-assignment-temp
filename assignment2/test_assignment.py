import pytest
from lxml import etree
import os

SUBMISSION_DIR = '/app/submission'

@pytest.fixture
def xml_tree():
    xml_file = os.path.join(SUBMISSION_DIR, 'activity_main.xml')
    if not os.path.exists(xml_file):
        pytest.skip(f"XML file not found at {xml_file}")
    try:
        tree = etree.parse(xml_file)
        return tree
    except Exception as e:
        pytest.fail(f"XML parsing failed: {e}")

@pytest.fixture
def root_element(xml_tree):
    return xml_tree.getroot()

class TestLayout:
    def test_xml_is_wellformed(self, xml_tree):
        assert xml_tree is not None, "XML file could not be parsed"

    def test_root_is_linear_layout(self, root_element):
        assert root_element.tag.endswith('LinearLayout'), f"Root element should be LinearLayout, got {root_element.tag}"

    def test_layout_dimensions(self, root_element):
        width = root_element.get('{http://schemas.android.com/apk/res/android}layout_width')
        height = root_element.get('{http://schemas.android.com/apk/res/android}layout_height')
        assert width == 'match_parent', f"Layout width should be match_parent, got {width}"
        assert height == 'match_parent', f"Layout height should be match_parent, got {height}"

    def test_layout_gravity_center(self, root_element):
        gravity = root_element.get('{http://schemas.android.com/apk/res/android}gravity')
        assert gravity is not None and 'center' in gravity.lower(), f"Layout gravity should be center, got {gravity}"

class TestTextView:
    def test_textview_exists(self, root_element):
        textviews = root_element.findall('.//TextView')
        assert len(textviews) > 0, "No TextView found in the layout"

    def test_textview_text(self, root_element):
        textviews = root_element.findall('.//TextView')
        found = any(tv.get('{http://schemas.android.com/apk/res/android}text') == 'Hi Android' or tv.get('android:text') == 'Hi Android' for tv in textviews)
        assert found, "TextView with text 'Hi Android' not found"

    def test_textview_dimensions(self, root_element):
        textviews = root_element.findall('.//TextView')
        assert any(tv.get('{http://schemas.android.com/apk/res/android}layout_width') in ['wrap_content', '400dp'] for tv in textviews), "TextView width should be wrap_content or 400dp"
        assert any(tv.get('{http://schemas.android.com/apk/res/android}layout_height') in ['wrap_content', '70dp'] for tv in textviews), "TextView height should be wrap_content or 70dp"

    def test_textview_textsize(self, root_element):
        textviews = root_element.findall('.//TextView')
        found = False
        for tv in textviews:
            size = tv.get('{http://schemas.android.com/apk/res/android}textSize')
            if size:
                try:
                    value = int(''.join(filter(str.isdigit, size)))
                    if value >= 24:
                        found = True
                        break
                except Exception:
                    continue
        assert found, "TextView textSize should be at least 24sp"

    def test_textview_textstyle_bold(self, root_element):
        textviews = root_element.findall('.//TextView')
        found = any('bold' in (tv.get('{http://schemas.android.com/apk/res/android}textStyle') or '') for tv in textviews)
        assert found, "TextView should have textStyle bold"
