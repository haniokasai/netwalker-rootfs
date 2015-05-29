#!/bin/bash
XINIT=`which xinit`
XSERVER=`which X`
EVCALIBRATE=`which ev_calibrate || echo ./ev_calibrate`
UDI=$(hal-find-by-property --key input.x11_driver --string evtouch)
MYDPY=":1.0"
ZENITY=`which zenity`
KDIALOG=`which kdialog`
XDIALOG=`which Xdialog`

INFO="タッチパネルの位置補正を行ないます。\n\n\
まず、スタイラスを使って、画面の周囲に沿って、なぞってください。\n\n\
周囲をなぞり終えたら、Enterキーを押してください。\
画面左上から順番に×印が赤くなりますので、スタイラスを使ってタップしてください。\\n\
もし、タップを誤った場合、右クリックボタンを押せば、一つ前に戻ることができます。\n\n\
右下の×印をタップし終えたら位置補正は終了です。\n\
注意： 補正は次のログイン以降で有効になります。"

RESTARTINFO="タッチパネルの位置補正が完了しました。\n\
補正を有効化するために、再ログインしてください。"

FAILINFO="エラー：タッチパネルデバイスが見つかりません。"

if [ -z "$UDI" ];then
    if [ -x "${ZENITY}" ]; then
        $ZENITY --info --text="${FAILINFO}"
    elif [ -x "${XDIALOG}" ]; then
        $XDIALOG --fill --msgbox "${FAILINFO}" 20 40
    elif [ -x "${KDIALOG}" ]; then
        $KDIALOG --msgbox "${FAILINFO}"
    fi
    exit 0
fi

if [ -x "${ZENITY}" ]; then
    $ZENITY --info --text="${INFO}"
elif [ -x "${XDIALOG}" ]; then
    $XDIALOG --fill --msgbox "${INFO}" 30 40
elif [ -x "${KDIALOG}" ]; then
    $KDIALOG --msgbox "${INFO}"
fi

echo $EVCALIBRATE

if [ -n "$DISPLAY" ]; then
    DPY=$(echo $DISPLAY|sed -e 's/[a-z:]*//g'|cut -d'.' -f1)
    MYDPY=":$(($DPY+1)).0"
fi

if ! [ -x "$EVCALIBRATE" ] ; then
	echo "ev_calibrate not found exiting ..."
	exit 1;
fi
echo "evalibrate located at $EVCALIBRATE"

if [ -z "$XINIT" ]; then
    echo "xinit not found exiting ..."
    exit 1;
fi
echo "xinit located at $XINIT"
if [ -z "$XSERVER" ]; then
    echo "X not found exiting ..."
    exit 1;
fi
echo "xserver located at $XSERVER"
if [ -e /tmp/ev_calibrate ]; then
	rm /tmp/ev_calibrate;
fi
echo "Creating FIFO..."
mknod /tmp/ev_calibrate p

#for development only :)
#cp evtouch_drv.o /usr/X11R6/lib/modules/input
#xinit /usr/bin/ddd ev_calibrate -- /usr/X11R6/bin/X
echo "Starting calibration program..."
sleep 2
hal-set-property --udi $UDI --key input.x11_options.calibrate --string "1"

$XINIT $EVCALIBRATE -- $XSERVER $MYDPY -auth /dev/null

hal-set-property --remove --udi $UDI --key input.x11_options.calibrate

invoke-rc.d --quiet xserver-xorg-input-evtouch start

rm /tmp/ev_calibrate

if [ -x "${ZENITY}" ]; then
    $ZENITY --info --text="${RESTARTINFO}"
elif [ -x "${XDIALOG}" ]; then
    $XDIALOG --fill --msgbox "${RESTARTINFO}" 10 40
elif [ -x "${KDIALOG}" ]; then
    $KDIALOG --msgbox "${RESTARTINFO}"
fi

exit 0
