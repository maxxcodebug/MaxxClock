import re

changes = []

# ---------- 1. Fix label visibility bug ----------
path = "app/src/main/java/com/maxxcodebug/maxxclock/settings/PreferencesDefaultValues.java"
with open(path) as f:
    content = f.read()

old = 'public static final String DEFAULT_TAB_TITLE_VISIBILITY = "1";'
new = 'public static final String DEFAULT_TAB_TITLE_VISIBILITY = "2";'
if old in content:
    content = content.replace(old, new)
    changes.append("PreferencesDefaultValues.java: DEFAULT_TAB_TITLE_VISIBILITY -> 2 (was colliding with NEVER)")
with open(path, "w") as f:
    f.write(content)

# ---------- 2. AboutFragment.java links ----------
path = "app/src/main/java/com/maxxcodebug/maxxclock/settings/AboutFragment.java"
with open(path) as f:
    content = f.read()

count = content.count("github.com/BlackyHawky/Clock")
content = content.replace("github.com/BlackyHawky/Clock", "github.com/maxxcodebug/MaxxClock")
changes.append(f"AboutFragment.java: {count} link(s) updated")
with open(path, "w") as f:
    f.write(content)

# ---------- 3. FirstLaunch.java link ----------
path = "app/src/main/java/com/maxxcodebug/maxxclock/setup/FirstLaunch.java"
with open(path) as f:
    content = f.read()

count = content.count("github.com/BlackyHawky/Clock")
content = content.replace("github.com/BlackyHawky/Clock", "github.com/maxxcodebug/MaxxClock")
changes.append(f"FirstLaunch.java: {count} link(s) updated")
with open(path, "w") as f:
    f.write(content)

# ---------- 4. App slogan ----------
path = "app/src/main/res/values/strings.xml"
with open(path) as f:
    content = f.read()

old_slogan = '<string name="app_slogan">100% FOSS Clock, based on AOSP</string>'
new_slogan = '<string name="app_slogan">MaxxClock — reimagined for MaxxPixel OS</string>'
if old_slogan in content:
    content = content.replace(old_slogan, new_slogan)
    changes.append("strings.xml: app_slogan updated")
with open(path, "w") as f:
    f.write(content)

for c in changes:
    print(c)
