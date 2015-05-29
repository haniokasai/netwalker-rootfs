
# default eval_gettext() to ensure that we do not fail
# if gettext-base is not installed
eval_gettext() {
    echo "$1"
}
. gettext.sh
export TEXTDOMAIN=friendly-recovery
export TEXTDOMAINDIR=/usr/share/locale
