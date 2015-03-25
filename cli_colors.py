class fg():
    def black( text ):
        return "\033[30m" + text + "\033[0m"
    def red( text ):
        return "\033[31m" + text + "\033[0m"
    def green( text ):
        return "\033[32m" + text + "\033[0m"
    def yellow( text ):
        return "\033[33m" + text + "\033[0m"
    def blue( text ):
        return "\033[34m" + text + "\033[0m"
    def violett( text ):
        return "\033[35m" + text + "\033[0m"
    def cyan( text ):
        return "\033[36m" + text + "\033[0m"
    def white( text ):
        return "\033[37m" + text + "\033[0m"

class bg():
    def black( text ):
        return "\033[40m" + text + "\033[0m"
    def red( text ):
        return "\033[41m" + text + "\033[0m"
    def green( text ):
        return "\033[42m" + text + "\033[0m"
    def yellow( text ):
        return "\033[43m" + text + "\033[0m"
    def blue( text ):
        return "\033[44m" + text + "\033[0m"
    def violett( text ):
        return "\033[45m" + text + "\033[0m"
    def cyan( text ):
        return "\033[46m" + text + "\033[0m"
    def white( text ):
        return "\033[47m" + text + "\033[0m"

class style():
    def bold( text ):
        return "\033[1m" + text + "\033[0m"
    def italic( text ):
        return "\033[3m" + text + "\033[0m"
    def underlined( text ):
        return "\033[4m" + text + "\033[0m"
    def blink( text ):
        return "\033[4m" + text + "\033[0m"
