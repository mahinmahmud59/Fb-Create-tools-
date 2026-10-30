
# Fb Create tools — Mobile starter

This is a Kivy Android app starter matching the supplied screenshot layout:
- Top: UID, COOKIES, 2FA, 2FA OTP
- Bottom: AUTO CREATE, NUMBER SET, PW SET, DESKTOP, AGENT SET, RELOAD, ALL CLEAR

## Included 12 planned modules
1. Fictional AUTO PROFILE generator (demo-only)
2. AUTO DOB (2000–2003 demo dates)
3. UID entry + copy
4. COOKIES/data section (safe app backup placeholder; no third-party session-cookie access)
5. 2FA secret manager (user-owned secret)
6. 2FA OTP generator (TOTP)
7. NUMBER SET
8. Manual OTP confirmation note (does not contact or verify with a third-party service)
9. PW SET (local password field)
10. DESKTOP-style information panel
11. AGENT SET (local label)
12. RELOAD / ALL CLEAR controls

## Build APK using Android phone
1. Create a GitHub repository in your phone browser.
2. Upload all files from this folder, including `.github/workflows/build.yml`.
3. Open the repository's **Actions** tab.
4. Select **Build Fb Create tools APK** and press **Run workflow**.
5. When complete, open the run and download artifact `fb-create-tools-apk`.

This is source code, not a ready-made APK. The first build may need dependency/workflow adjustments.
Do not use this starter to create fake accounts or bypass another service's verification.
