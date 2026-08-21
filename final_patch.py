import os, re, subprocess

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

# ---------- 1. Patch build.gradle: debug suffix .debug -> .dev, stable filename ----------
gpath = "app/build.gradle"
with open(gpath) as f:
    g = f.read()

g = g.replace('versionNameSuffix = "-debug"', 'versionNameSuffix = "-dev"')
g = g.replace('applicationIdSuffix = ".debug"', 'applicationIdSuffix = ".dev"')
g = g.replace('manifestPlaceholders = [appName: "@string/app_label_debug"]',
              'manifestPlaceholders = [appName: "@string/app_label_dev"]')

old_variant_block = '''            if (variant.buildType == "nightly") {
                outputFileName = "Clock_${versionName}-nightly-${commitNumber}-${buildCommit}.apk"
            } else {
                def suffix = versionNameSuffix ?: (keystorePropertiesFile.exists() ? "-release" : "-unsigned")
                outputFileName = "Clock_${versionName}${suffix}.apk"
            }'''

new_variant_block = '''            if (variant.buildType == "nightly") {
                outputFileName = "MaxxClock_${versionName}-nightly-${commitNumber}-${buildCommit}.apk"
            } else if (variant.buildType == "release") {
                outputFileName = "MaxxClock_${versionName}-stable.apk"
            } else {
                def suffix = versionNameSuffix ?: (keystorePropertiesFile.exists() ? "-release" : "-unsigned")
                outputFileName = "MaxxClock_${versionName}${suffix}.apk"
            }'''

if old_variant_block in g:
    g = g.replace(old_variant_block, new_variant_block)
    print("build.gradle: output filename block patched - OK")
else:
    print("WARN: output filename block anchor not found in build.gradle")

with open(gpath, "w") as f:
    f.write(g)

print("build.gradle: debug suffix -> .dev, stable filename set")

# ---------- 2. Rename app_label strings across all strings.xml, rename any app_label_debug key ----------
renamed_files = 0
for root, dirs, files in os.walk("app/src"):
    if ".git" in root:
        continue
    for fname in files:
        if fname != "strings.xml":
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        original = content

        content = re.sub(r'(<string name="app_label">).*?(</string>)', r'\g<1>MaxxClock\g<2>', content)
        content = re.sub(r'(<string name="app_label_debug">).*?(</string>)', r'\g<1>MaxxClock Dev\g<2>', content)
        content = re.sub(r'name="app_label_debug"', 'name="app_label_dev"', content)
        content = re.sub(r'(<string name="app_label_nightly">).*?(</string>)', r'\g<1>MaxxClock Nightly\g<2>', content)
        content = re.sub(r'(<string name="app_name">).*?(</string>)', r'\g<1>MaxxClock\g<2>', content)

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            renamed_files += 1

print(f"strings.xml: rebranded in {renamed_files} files")

# ---------- 3. Ensure app_label_dev exists even if not found above ----------
main_strings = "app/src/main/res/values/strings.xml"
with open(main_strings, encoding="utf-8") as f:
    content = f.read()

if "app_label_dev" not in content and "app_label_debug" not in content:
    content = content.replace(
        '<string name="app_label">MaxxClock</string>',
        '<string name="app_label">MaxxClock</string>\n    <string name="app_label_dev">MaxxClock Dev</string>'
    )
    with open(main_strings, "w", encoding="utf-8") as f:
        f.write(content)
    print("strings.xml: app_label_dev added (fallback)")

if "app_label_nightly" not in content:
    with open(main_strings, encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        '<string name="app_label">MaxxClock</string>',
        '<string name="app_label">MaxxClock</string>\n    <string name="app_label_nightly">MaxxClock Nightly</string>'
    )
    with open(main_strings, "w", encoding="utf-8") as f:
        f.write(content)
    print("strings.xml: app_label_nightly added (fallback)")

# ---------- 4. GitHub Actions workflow to build APKs ----------
os.makedirs(".github/workflows", exist_ok=True)
workflow_path = ".github/workflows/build.yml"

workflow_yaml = '''name: Build MaxxClock APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Build debug (dev) APK
        run: ./gradlew assembleDebug

      - name: Build stable (release, unsigned) APK
        run: ./gradlew assembleRelease

      - name: Upload dev APK
        uses: actions/upload-artifact@v4
        with:
          name: MaxxClock-dev-apk
          path: app/build/outputs/apk/debug/*.apk

      - name: Upload stable APK
        uses: actions/upload-artifact@v4
        with:
          name: MaxxClock-stable-apk
          path: app/build/outputs/apk/release/*.apk
'''

if not os.path.exists(workflow_path):
    with open(workflow_path, "w") as f:
        f.write(workflow_yaml)
    print("GitHub Actions workflow created: .github/workflows/build.yml")
else:
    print("Workflow already exists, not overwritten")

print("\\n=== ALL PATCHES DONE ===")
