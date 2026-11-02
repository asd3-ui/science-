[app]
title = Science Play Learning
package.name = science_play_learning
package.domain = org.scienceplay
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.1.0
requirements = python3,pygame,numpy
orientation = landscape
fullscreen = 1

# --- التعديل الأساسي للأيقونة المضافة ---
# توجيه الأداة لقراءة ملف icon.png الحقيقي المضاف في المجلد الرئيسي للمشروع
icon.filename = %(source.dir)s/icon.png

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.private_storage = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
