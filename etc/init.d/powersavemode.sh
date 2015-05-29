#! /bin/sh
### BEGIN INIT INFO
# Provides:          powersavemode.sh
# Required-Start:    $local_ff
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      1
# Short-Description: set usb device and dvfs low power mode
# Description        set usb device and dvfs low power mode.
### END INIT INFO

case "$1" in
  start)
	echo "set USB device Low power Mode"
	echo auto > /sys/bus/usb/devices/1-1/power/level
	echo auto > /sys/bus/usb/devices/2-1/power/level
	echo auto > /sys/bus/usb/devices/usb1/power/level
	echo auto > /sys/bus/usb/devices/usb2/power/level	
	echo "enable DVFS"
	echo 1 > /sys/devices/platform/mxc_dvfs_core.0/enable
	;;
  stop)
	echo "unset USB device Low power Mode"
	echo on > /sys/bus/usb/devices/1-1/power/level
	echo on > /sys/bus/usb/devices/2-1/power/level
	echo on > /sys/bus/usb/devices/usb1/power/level
	echo on > /sys/bus/usb/devices/usb2/power/level	
	echo "disable DVFS"
	echo 0 > /sys/devices/platform/mxc_dvfs_core.0/enable
	;;
  *)
	echo "Usage: powersavemode.sh start|stop" >&2
	exit 3
	;;
esac

exit 0
