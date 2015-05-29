# Default init script logging functions suitable for Ubuntu.
# See /lib/lsb/init-functions for usage help.

log_use_usplash () {
    if [ "${loop:-n}" = y ]; then
        return 1
    fi
    type usplash_write >/dev/null 2>&1
}

log_to_console () {
    [ "${loop:-n}" != y ] || return 0
    [ "${QUIET:-no}" != yes ] || return 0

    # Only output to the console when we're given /dev/null
    stdin=`readlink /proc/self/fd/0`
    [ "${stdin#/dev/null}" != "$stdin" ] || return 0

    func=$1
    shift

    loop=y $func "$@" </dev/console >/dev/console 2>&1 || true
}

log_success_msg () {
    if log_use_usplash; then
        usplash_write "TEXT   $*" || true
    fi

    log_to_console log_success_msg "$@"

    echo " * $@"
}

log_failure_msg () {
    if log_use_usplash; then
        usplash_write "TEXT   $*" || true
    fi

    log_to_console log_failure_msg "$@"

    if log_use_fancy_output; then
        RED=`$TPUT setaf 1`
        NORMAL=`$TPUT op`
        echo " $RED*$NORMAL $@"
    else
        echo " * $@"
    fi
}

log_warning_msg () {
    if log_use_usplash; then
        usplash_write "TEXT   $*" || true
    fi

    log_to_console log_warning_msg "$@"

    if log_use_fancy_output; then
        YELLOW=`$TPUT setaf 3`
        NORMAL=`$TPUT op`
        echo " $YELLOW*$NORMAL $@"
    else
        echo " * $@"
    fi
}

log_begin_msg () {
    log_daemon_msg "$1"
}

log_daemon_msg () {
    if [ -z "$1" ]; then
        return 1
    fi

    if log_use_usplash; then
        usplash_write "TEXT $*" || true
    fi

    log_to_console log_daemon_msg "$@"

    if log_use_fancy_output && $TPUT xenl >/dev/null 2>&1; then
        COLS=`$TPUT cols`
        if [ "$COLS" ] && [ "$COLS" -gt 6 ]; then
            COL=`$EXPR $COLS - 7`
        else
	    COLS=80
            COL=73
        fi
        # We leave the cursor `hanging' about-to-wrap (see terminfo(5)
        # xenl, which is approximately right). That way if the script
        # prints anything then we will be on the next line and not
        # overwrite part of the message.

        # Previous versions of this code attempted to colour-code the
        # asterisk but this can't be done reliably because in practice
        # init scripts sometimes print messages even when they succeed
        # and we won't be able to reliably know where the colourful
        # asterisk ought to go.

        printf " * $*       "
        # Enough trailing spaces for ` [fail]' to fit in; if the message
        # is too long it wraps here rather than later, which is what we
        # want.
        $TPUT hpa `$EXPR $COLS - 1`
        printf ' '
    else
        echo " * $@"
        COL=
    fi
}

log_progress_msg () {
    :
}

log_end_msg () {
    if [ -z "$1" ]; then
        return 1
    fi

    if log_use_usplash; then
        if [ "$1" -eq 0 ]; then
            usplash_write "SUCCESS OK" || true
        else
            usplash_write "FAILURE failed" || true
        fi
    fi

    log_to_console log_end_msg "$@"

    if [ "$COL" ] && [ -x "$TPUT" ]; then
        printf "\r"
        $TPUT hpa $COL
        if [ "$1" -eq 0 ]; then
            echo "[ OK ]"
        else
            printf '['
            $TPUT setaf 1 # red
            printf fail
            $TPUT op # normal
            echo ']'
        fi
    else
        if [ "$1" -eq 0 ]; then
            echo "   ...done."
        else
            echo "   ...fail!"
        fi
    fi
    return $1
}

log_action_msg () {
    if log_use_usplash; then
        usplash_write "TEXT $*" || true
    fi

    log_to_console log_action_msg "$@"

    echo " * $@"
}

log_action_begin_msg () {
    log_daemon_msg "$@..."
}

log_action_cont_msg () {
    log_daemon_msg "$@..."
}

log_action_end_msg () {
    # In the future this may do something with $2 as well.
    log_end_msg "$1" || true
}
