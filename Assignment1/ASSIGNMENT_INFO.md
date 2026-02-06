# Assignment 1: Hello Android - UI Basics

## Overview
This is the first assignment in the Android Development course. Students will create a simple Android application that displays "Hi Android" text centered on the screen.

## Assignment Details

### Language
Android (XML/Java)

### Topics Covered
- Activities and Intents
- XML Layout Files
- TextViews and Views
- Layout Management (LinearLayout)
- View Centering and Positioning
- Android Resource System

### Learning Objectives
By completing this assignment, students will:
1. Understand the basics of Android Activity structure
2. Learn how to create XML layout files
3. Master LinearLayout configuration
4. Implement TextViews with proper styling
5. Center views on the screen using Android layout attributes

---

## Requirements

### Task 1: Create activity_main.xml Layout

Create an XML layout file that:

1. **Root Element**: Use a `LinearLayout` as the root container
   - Width: `match_parent`
   - Height: `match_parent`
   - Orientation: `vertical`
   - Gravity: `center` (to center content)

2. **TextView Widget**: Add a TextView with the following properties:
   - Text: "Hi Android"
   - Width: `wrap_content`
   - Height: `wrap_content`
   - Text Size: At least `24sp` (recommended: `32sp`)
   - Text Style: `bold`
   - Text Color: Black or appropriate color

### File Location
`app/src/main/res/layout/activity_main.xml`

---

## Expected Output

The application should display:
- A single TextView with centered text reading "Hi Android"
- Large, bold font for visibility
- Text centered both horizontally and vertically on the screen

---

## Starter Code

The starter code is provided in `startercode.zip` and includes:
- `MainActivity.java` - Base Java activity class with TODOs
- `activity_main.xml` - XML layout file with TODOs

### MainActivity.java
```java
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // TODO: Set the content view to activity_main layout
        setContentView(R.layout.activity_main);
    }
}
```

### activity_main.xml (Starter)
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <!-- TODO: Add a TextView here -->

</LinearLayout>
```

---

## Solution

The complete solution is provided in `solution.zip`:

### activity_main.xml (Solution)
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hi Android"
        android:textSize="32sp"
        android:textStyle="bold"
        android:textColor="@android:color/black" />

</LinearLayout>
```

---

## Validation & Testing

### Test Cases

The following test cases validate the solution:

#### 1. Smoke Tests
- ✓ File exists and is valid XML
- ✓ XML can be parsed without errors

#### 2. Layout Structure Tests
- ✓ Root element is a layout (LinearLayout/RelativeLayout/FrameLayout)
- ✓ Layout dimensions are match_parent
- ✓ Layout has center gravity

#### 3. TextView Tests
- ✓ Layout contains at least one TextView
- ✓ TextView displays "Hi Android" text
- ✓ TextView uses wrap_content for dimensions
- ✓ TextView has adequate text size (≥24sp)

### Running Tests

To run the validation tests:

```bash
cd Assignment1
docker-compose up -d
docker-compose exec judge /app/runner.sh
```

### Docker Image

The `x86.tar` file contains a Docker image with:
- Android SDK
- Python 3 with pytest
- XML validation tools (lxml)
- All necessary dependencies for running tests

---

## Key Concepts

### LinearLayout
- Container that arranges views in a single row or column
- Orientation: Can be vertical or horizontal
- Gravity: Controls alignment of child views

### TextView
- Display text to the user
- Cannot be edited by the user (use EditText for input)
- Properties: text, textSize, textColor, textStyle

### Android Namespace
- `android:` - Standard Android framework namespace
- `app:` - App-specific or library attributes
- `tools:` - Tools-only attributes (not included in APK)

---

## Submission

To submit the solution:

1. Modify the `activity_main.xml` file as required
2. Package your solution in a ZIP file
3. Upload to the assignment platform

---

## Hints

1. **Centering**: Use `android:gravity="center"` on the parent LinearLayout to center child views
2. **Text Size**: Use `sp` (scale-independent pixels) instead of `dp` for text
3. **Bold Text**: Use `android:textStyle="bold"` attribute
4. **XML Validation**: Ensure proper namespace declarations at the top of the file
5. **Preview**: Use Android Studio's Layout Preview to check your work

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Text not centered | Add `android:gravity="center"` to LinearLayout |
| Text too small | Increase `android:textSize` value |
| XML parsing error | Check for missing closing tags and proper namespace declarations |
| Layout not full screen | Ensure root layout has `match_parent` for both dimensions |

---

## Resources

- [Android Layout Documentation](https://developer.android.com/guide/topics/ui/declaring-layout)
- [TextView Documentation](https://developer.android.com/reference/android/widget/TextView)
- [LinearLayout Documentation](https://developer.android.com/reference/android/widget/LinearLayout)

---

## Grading Criteria

| Criteria | Points |
|----------|--------|
| XML is well-formed and valid | 10 |
| Layout structure correct | 20 |
| TextView displays "Hi Android" | 25 |
| Text is properly centered | 20 |
| Text styling (size and weight) | 15 |
| Code organization and comments | 10 |
| **Total** | **100** |

---

**Assignment Version**: 1.0  
**Last Updated**: February 6, 2026  
**Difficulty Level**: Beginner  
**Estimated Time**: 15-20 minutes
