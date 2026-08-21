#!/bin/bash
set -e

echo "--- Checking settings.gradle for jitpack repo ---"
if grep -q "jitpack.io" settings.gradle; then
    echo "jitpack already present, skipping"
else
    if grep -q "google()" settings.gradle; then
        sed -i "s#google()#google()\n        maven { url 'https://jitpack.io' }#" settings.gradle
        echo "jitpack added to settings.gradle"
    else
        echo "COULD NOT auto-add jitpack — paste settings.gradle content for manual patch"
    fi
fi

echo "--- Adding BlurView dependency to app/build.gradle ---"
if grep -q "Dimezis:BlurView" app/build.gradle; then
    echo "BlurView already present, skipping"
else
    sed -i "s#implementation 'com.google.android.material:material:1.14.0'#implementation 'com.google.android.material:material:1.14.0'\n    implementation 'com.github.Dimezis:BlurView:version-2.0.6'#" app/build.gradle
    echo "BlurView dependency added"
fi

echo "--- Done. Now showing result for verification ---"
echo "===== settings.gradle ====="
cat settings.gradle
echo "===== app/build.gradle (grep dependencies) ====="
grep -n "jitpack\|BlurView\|material:material" app/build.gradle settings.gradle 2>/dev/null
