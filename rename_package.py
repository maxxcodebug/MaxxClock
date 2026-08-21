import os
import subprocess
import re

OLD_PKG = "com.best.deskclock"
NEW_PKG = "com.maxxcodebug.maxxclock"
OLD_PATH = "com/best/deskclock"
NEW_PATH = "com/maxxcodebug/maxxclock"
NEW_APP_NAME = "MaxxClock"

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

TEXT_EXTS = {".java", ".xml", ".gradle", ".kt", ".pro", ".properties", ".yml", ".yaml"}

changed_files = 0
skipped = []

# ---------- 1. Replace package string in all text files across repo ----------
for root, dirs, files in os.walk("."):
    if ".git" in root.split(os.sep):
        continue
    for fname in files:
        ext = os.path.splitext(fname)[1]
        if ext not in TEXT_EXTS:
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            skipped.append((fpath, str(e)))
            continue

        if OLD_PKG in content:
            new_content = content.replace(OLD_PKG, NEW_PKG)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed_files += 1

print(f"Step 1: Replaced package string in {changed_files} files")
if skipped:
    print(f"  (skipped {len(skipped)} unreadable files)")

# ---------- 2. Move java source directories to new package path ----------
old_src_dirs = [
    "app/src/main/java/" + OLD_PATH,
    "app/src/androidTest/java/" + OLD_PATH,
    "app/src/test/java/" + OLD_PATH,
]

for old_dir in old_src_dirs:
    if os.path.isdir(old_dir):
        base = old_dir.rsplit(OLD_PATH, 1)[0]
        new_dir = base + NEW_PATH
        os.makedirs(os.path.dirname(new_dir), exist_ok=True)
        rc, out, err = run(f'git mv "{old_dir}" "{new_dir}"')
        if rc == 0:
            print(f"Step 2: Moved {old_dir} -> {new_dir}")
        else:
            # fallback to plain mv if git mv fails (e.g. not tracked yet)
            rc2, out2, err2 = run(f'mv "{old_dir}" "{new_dir}"')
            print(f"Step 2: {'Moved (plain mv)' if rc2==0 else 'FAILED'}: {old_dir} -> {new_dir}")
            if rc2 != 0:
                print(f"  error: {err2}")
    else:
        print(f"Step 2: {old_dir} does not exist, skipping")

# ---------- 3. Fix namespace / applicationId explicitly ----------
build_gradle = "app/build.gradle"
with open(build_gradle, "r") as f:
    content = f.read()

content = re.sub(r'applicationId\s*=\s*"[^"]+"', f'applicationId = "{NEW_PKG}"', content)
content = re.sub(r"namespace\s*=\s*'[^']+'", f"namespace = '{NEW_PKG}'", content)
content = re.sub(r'namespace\s*=\s*"[^"]+"', f'namespace = "{NEW_PKG}"', content)

with open(build_gradle, "w") as f:
    f.write(content)
print("Step 3: applicationId & namespace fixed in app/build.gradle")

# ---------- 4. Set app_name everywhere it's declared ----------
app_name_files = 0
for root, dirs, files in os.walk("app/src/main/res"):
    if ".git" in root.split(os.sep):
        continue
    for fname in files:
        if fname != "strings.xml":
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        new_content, n = re.subn(
            r'(<string name="app_name">).*?(</string>)',
            rf'\g<1>{NEW_APP_NAME}\g<2>',
            content
        )
        if n > 0:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            app_name_files += 1

print(f"Step 4: app_name updated in {app_name_files} strings.xml files")

print("\n=== DONE. Run verification commands next. ===")
