import re

# ---------- 1. Fix desk_clock.xml: move pill background+clip to BlurView ----------
xml_path = "app/src/main/res/layout/desk_clock.xml"
with open(xml_path, "r") as f:
    xml = f.read()

old_blur_open = '''    <eightbitlab.com.blurview.BlurView
        android:id="@+id/bottom_nav_blur_view"
        android:layout_width="wrap_content"
        android:layout_height="64dp"
        android:layout_marginStart="60dp"
        android:layout_marginEnd="60dp"
        android:layout_marginBottom="24dp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent">

        <com.google.android.material.bottomnavigation.BottomNavigationView
            android:id="@+id/desk_clock_bottom_menu"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:background="@drawable/bg_bottom_nav_pill"
            app:elevation="0dp"'''

new_blur_open = '''    <eightbitlab.com.blurview.BlurView
        android:id="@+id/bottom_nav_blur_view"
        android:layout_width="wrap_content"
        android:layout_height="64dp"
        android:layout_marginStart="60dp"
        android:layout_marginEnd="60dp"
        android:layout_marginBottom="24dp"
        android:background="@drawable/bg_bottom_nav_pill"
        android:clipToOutline="true"
        android:outlineProvider="background"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent">

        <com.google.android.material.bottomnavigation.BottomNavigationView
            android:id="@+id/desk_clock_bottom_menu"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:background="@android:color/transparent"
            app:elevation="0dp"'''

if old_blur_open in xml:
    xml = xml.replace(old_blur_open, new_blur_open)
    print("desk_clock.xml: pill background moved to BlurView - OK")
else:
    print("desk_clock.xml: anchor NOT found, skipped (check manually)")

with open(xml_path, "w") as f:
    f.write(xml)

# ---------- 2. Patch DeskClock.java ----------
java_path = "app/src/main/java/com/best/deskclock/DeskClock.java"
with open(java_path, "r") as f:
    java = f.read()

changes = 0

# 2a. Add imports
old_imports = "import android.view.KeyEvent;\nimport android.view.Menu;\nimport android.view.MenuItem;\nimport android.view.View;"
new_imports = "import android.view.KeyEvent;\nimport android.view.Menu;\nimport android.view.MenuItem;\nimport android.view.MotionEvent;\nimport android.view.View;\nimport android.view.ViewGroup;"
if old_imports in java:
    java = java.replace(old_imports, new_imports)
    changes += 1
else:
    print("WARN: import anchor not found")

old_import2 = "import com.google.android.material.snackbar.Snackbar;"
new_import2 = "import com.google.android.material.snackbar.Snackbar;\n\nimport eightbitlab.com.blurview.RenderScriptBlur;"
if old_import2 in java:
    java = java.replace(old_import2, new_import2)
    changes += 1
else:
    print("WARN: snackbar import anchor not found")

# 2b. Fix applyWindowInsets to give the floating pill proper bottom margin
old_insets = '''    private void applyWindowInsets() {
        InsetsUtils.doOnApplyWindowInsets(mBinding.deskClockRootView, (v, insets) -> {
            // Get the system bar and notch insets
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());

            v.setPadding(bars.left, bars.top, bars.right, 0);

            mBinding.deskClockBottomMenu.setPadding(0, 0, 0, bars.bottom);
        });
    }'''

new_insets = '''    private void applyWindowInsets() {
        InsetsUtils.doOnApplyWindowInsets(mBinding.deskClockRootView, (v, insets) -> {
            // Get the system bar and notch insets
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());

            v.setPadding(bars.left, bars.top, bars.right, 0);

            ViewGroup.MarginLayoutParams pillParams =
                (ViewGroup.MarginLayoutParams) mBinding.bottomNavBlurView.getLayoutParams();
            pillParams.bottomMargin = bars.bottom + (int) (24 * getResources().getDisplayMetrics().density);
            mBinding.bottomNavBlurView.setLayoutParams(pillParams);
        });
    }'''

if old_insets in java:
    java = java.replace(old_insets, new_insets)
    changes += 1
else:
    print("WARN: applyWindowInsets anchor not found")

# 2c. Replace the background-color block, call blur+animation setup
old_bg_block = '''        if (ThemeUtils.isNight(getResources()) && SettingsDAO.getDarkMode(mPrefs).equals(AMOLED_DARK_MODE)) {
            mBinding.deskClockBottomMenu.setBackgroundColor(Color.BLACK);
            mBinding.deskClockBottomMenu.setItemTextColor(new ColorStateList(
                new int[][]{{android.R.attr.state_selected}, {android.R.attr.state_pressed}, {}},
                new int[]{primaryColor, primaryColor, Color.WHITE}));
        } else {
            final boolean isCardBackgroundDisplayed = SettingsDAO.isCardBackgroundDisplayed(mPrefs);

            if (isCardBackgroundDisplayed) {
                mBinding.deskClockBottomMenu.setBackgroundColor(surfaceColor);
            } else {
                mBinding.deskClockBottomMenu.setBackgroundColor(Color.TRANSPARENT);
            }

            mBinding.deskClockBottomMenu.setItemTextColor(new ColorStateList(
                new int[][]{{android.R.attr.state_selected}, {android.R.attr.state_pressed}, {}},
                new int[]{primaryColor, primaryColor, onBackgroundColor}));
        }
    }'''

new_bg_block = '''        mBinding.deskClockBottomMenu.setBackgroundColor(Color.TRANSPARENT);

        if (ThemeUtils.isNight(getResources()) && SettingsDAO.getDarkMode(mPrefs).equals(AMOLED_DARK_MODE)) {
            mBinding.deskClockBottomMenu.setItemTextColor(new ColorStateList(
                new int[][]{{android.R.attr.state_selected}, {android.R.attr.state_pressed}, {}},
                new int[]{primaryColor, primaryColor, Color.WHITE}));
        } else {
            mBinding.deskClockBottomMenu.setItemTextColor(new ColorStateList(
                new int[][]{{android.R.attr.state_selected}, {android.R.attr.state_pressed}, {}},
                new int[]{primaryColor, primaryColor, onBackgroundColor}));
        }

        setupBottomNavBlur();
        applyBottomNavTapAnimation();
    }'''

if old_bg_block in java:
    java = java.replace(old_bg_block, new_bg_block)
    changes += 1
else:
    print("WARN: background-color block anchor not found")

# 2d. Insert new helper methods before applyBottomNavTooltips()
old_tooltip_anchor = '''    @SuppressLint("RestrictedApi")
    private void applyBottomNavTooltips() {'''

new_methods = '''    /**
     * Sets up the Apple-style frosted glass blur on the floating bottom nav pill.
     */
    private void setupBottomNavBlur() {
        View decorView = getWindow().getDecorView();
        ViewGroup rootViewGroup = decorView.findViewById(android.R.id.content);
        Drawable windowBackground = decorView.getBackground();

        mBinding.bottomNavBlurView.setClipToOutline(true);
        mBinding.bottomNavBlurView.setupWith(rootViewGroup, new RenderScriptBlur(this))
            .setFrameClearDrawable(windowBackground)
            .setBlurRadius(16f);
        mBinding.bottomNavBlurView.setOverlayColor(Color.parseColor("#33000000"));
    }

    /**
     * Adds a quick scale-down/scale-up tap animation to each bottom nav icon.
     */
    @SuppressLint("RestrictedApi")
    private void applyBottomNavTapAnimation() {
        BottomNavigationMenuView menuView = (BottomNavigationMenuView) mBinding.deskClockBottomMenu.getChildAt(0);

        for (int i = 0; i < menuView.getChildCount(); i++) {
            View itemView = menuView.getChildAt(i);

            itemView.setOnTouchListener((v, event) -> {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN ->
                        v.animate().scaleX(0.85f).scaleY(0.85f).setDuration(120).start();
                    case MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL ->
                        v.animate().scaleX(1f).scaleY(1f).setDuration(150).start();
                }
                return false;
            });
        }
    }

    @SuppressLint("RestrictedApi")
    private void applyBottomNavTooltips() {'''

if old_tooltip_anchor in java:
    java = java.replace(old_tooltip_anchor, new_methods)
    changes += 1
else:
    print("WARN: applyBottomNavTooltips anchor not found")

with open(java_path, "w") as f:
    f.write(java)

print(f"DeskClock.java: {changes}/4 patches applied")
