#!/bin/bash

# معلومات الأداة
TOOL_NAME="atc"
TOOL_DIR="/usr/local/bin/$TOOL_NAME"
MAIN_SCRIPT="$TOOL_DIR/atc.py"
SYMLINK_PATH="/usr/local/bin/$TOOL_NAME"

# تأكد أن المجلد والسكربت موجودين
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "[!] لم يتم العثور على السكربت الرئيسي atc.py داخل $TOOL_DIR"
    exit 1
fi

# إعطاء صلاحية تنفيذ للسكربت
echo "[+] إعطاء صلاحيات تنفيذ لـ $MAIN_SCRIPT ..."
sudo chmod +x "$MAIN_SCRIPT"

# إنشاء اختصار لتشغيل الأداة بالأمر atc من أي مكان
echo "[+] إنشاء اختصار تنفيذي في /usr/local/bin/$TOOL_NAME ..."
sudo ln -sf "$MAIN_SCRIPT" "$SYMLINK_PATH"

# اختبار التشغيل
if command -v $TOOL_NAME &>/dev/null; then
    echo "[✔] تم التثبيت بنجاح! شغل أداتك بالأمر: $TOOL_NAME"
else
    echo "[!] حدث خطأ في إنشاء الاختصار. تأكد من المسارات."
fi