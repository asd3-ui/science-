[app]
title = مغامرات العلوم
package.name = scienceadventure
package.domain = org.example
source.dir = .
source.include_exts = py,txt,spec,ttf,otf
version = 1.0.0

requirements = python3,pygame,numpy,arabic-reshaper,python-bidi

orientation = landscape
fullscreen = 1
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
