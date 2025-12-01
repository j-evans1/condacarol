# UI Test Checklist - CondaCarol

## Purpose
Ensure NO white-on-white text issues exist in any view or widget.

## CSS Fixes Applied

### Comprehensive Input Styling
- All `input`, `textarea`, `select` elements: Dark background (#242938), white text (#FFFFFF)
- Explicit styling for `input[type="text"]`, `input[type="password"]`
- Placeholder text: Muted gray with reduced opacity
- Focus states: Green border with shadow glow
- Disabled states: Reduced opacity with muted text

### Widget-Specific Fixes
- `.bk-input`, `.bk-input-group`, `.bk-input-container`: All covered
- Select dropdown options: Dark background with white text
- Radio button groups: Custom styled with Anaconda green accent
- Labels: White text, transparent background
- All Bokeh elements: Force white text color

### Container Fixes
- `.bk-root`, `.bk`, all bokeh containers: Proper text color inheritance
- Widget boxes: Transparent backgrounds
- Panel panes: Proper color inheritance

## Test Views

### ✅ Setup View (Admin)
Test elements:
- [ ] Admin Password input (type="password") - Should show white text
- [ ] Question textarea - Should show white text
- [ ] Questions list (disabled textarea) - Should show white text with muted style
- [ ] All buttons - Should have proper colors

### ✅ Answer Questions View
Test elements:
- [ ] "Your Name" text input - Should show white text
- [ ] All question textarea inputs - Should show white text
- [ ] Participant count display - Should show white text
- [ ] All buttons - Should have proper colors

### ✅ Play Game View
Test elements:
- [ ] "Your Name" text input - Should show white text
- [ ] Radio button labels - Should show white text
- [ ] Answer cards - Should have proper contrast
- [ ] Selected radio button - Should have green accent
- [ ] All buttons - Should have proper colors

### ✅ Results View
Test elements:
- [ ] Leaderboard text - Should show white text
- [ ] All answers revealed - Should show white text
- [ ] Participant names - Should show white text
- [ ] All buttons - Should have proper colors

## Testing Instructions

1. **Setup View Test:**
   - Navigate to Setup tab
   - Type in the password field - text should be visible (hidden characters)
   - Type in the question textarea - text should be white on dark background
   - Add a question - should appear in the list below with white text

2. **Answer View Test:**
   - Navigate to Answer tab
   - Type your name in text input - should show white text
   - Click Refresh Questions
   - Type in all answer textareas - should show white text
   - Submit answers

3. **Game View Test:**
   - Navigate to Play tab
   - Type your name - should show white text
   - Click Refresh Game
   - Click on radio buttons - should see white text labels
   - Selected button should have green accent
   - All answer text should be visible

4. **Results View Test:**
   - Navigate to Results tab
   - All text should be white/visible
   - Leaderboard numbers should be visible
   - All participant names and answers should be visible

## Common Issues Fixed

1. **White-on-white dropdowns** - Fixed with explicit `select option` styling
2. **White-on-white text inputs** - Fixed with comprehensive `input` selectors
3. **White-on-white labels** - Fixed with `.bk-label` and related selectors
4. **Invisible placeholder text** - Fixed with `::placeholder` pseudo-element
5. **White text in white containers** - Fixed with `.bk *` global selector

## Browser Testing

Recommended browsers:
- Chrome/Edge (Chromium)
- Firefox
- Safari

All should display consistently with white text on dark backgrounds.

## Color Reference

- Background: #0E1117 (Deep Navy)
- Surface: #1A1F2E (Elevated Navy)
- Surface Variant: #242938 (Input backgrounds)
- Text: #FFFFFF (White)
- Text Muted: #8B92A7 (Gray)
- Primary: #43B02A (Anaconda Green)
- Border: #2A2F3D

## Quick Visual Check

Every text field should look like:
```
┌─────────────────────────────┐
│ [White text on #242938]     │ ← Input
│                             │
└─────────────────────────────┘
```

NOT like:
```
┌─────────────────────────────┐
│ [Invisible white on white]  │ ← WRONG!
│                             │
└─────────────────────────────┘
```
