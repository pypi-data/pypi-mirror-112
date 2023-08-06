__all__=['write', 'printerr', 'service', 'set_logfile', 'set_markup_keywords', 'set_markup_usage', 'flush_service', 'markup_codes']
import sys

terminal_codes={'':'\033[0m', 'red':'\033[31m', 'green':'\033[32m',
                'black':'\033[30m', 'yellow':'\033[33m', 'blue':'\033[34m',
                'magenta':'\033[35m', 'cyan':'\033[36m', 'white':'\033[37m',
                'bright':'\033[1m', 'dim':'\033[2m', 'underscore':'\033[4m',
                'blink':'\033[5m', 'reverse':'\033[7m', 'hidden':'\033[8m'}
markup_codes=set(terminal_codes.keys())
logfile=None
markup_keywords={}
printed_rchar=0
no_colors=False
    
def flush_service():
    """ Clears up the "sticky" messages printed with the service function, making use of \\r
    Args:    (None)
    Returns:  None
    """
    global printed_rchar
    if printed_rchar:
        sys.stderr.write('\r'+printed_rchar*' '+'\r' )
        printed_rchar=0    
    
def write(text, end='\n', how='', keywords={}, is_service=False, is_stderror=False):
    """Main function for printing a message to stdout. Note: prints to logfile too, if defined (see set_logfile)

    Args:
     text (any):       text to be printed, converted to str if necessary
     end (str):        newline is added to each input text, use end='' to avoid it
     how (str):        any number of comma-separated termcodes to markup your text, among:
      black blink blue bright cyan dim green hidden magenta red reverse underscore white yellow
     keywords (str):   dictionary like key:termcode, so that all occurrences of key in text is marked with termcode(s)

    Returns: None
    """  
    if not keywords and markup_keywords:
        keywords=markup_keywords
    msg=str(text)
    if end:
        msg=msg+end

    if not is_service and not logfile is None:
        no_color_msg=msg
        
    # colors and other markup
    if (how or keywords) and sys.stdout.isatty() and not no_colors:
        if how:
            for c in how.split(','): 
                if not c in terminal_codes:
                    raise Exception(f"ERROR option 'how' for write was not recognized: {c} ; possible values are: {','.join([i for i in terminal_codes if i])}")
                msg=terminal_codes[c]+msg+terminal_codes['']
        for word in keywords:
            code=''
            for c in keywords[word].split(','):
                code+=terminal_codes[c]
            msg=msg.replace(word, code+word+terminal_codes[''])

    # flushing rchars
    flush_service()
        
    if is_stderror or is_service:
        sys.stderr.write(msg)
    else: 
        sys.stdout.write(msg)
        
    if not is_service and not logfile is None:
        print(str(no_color_msg), end='', file=logfile)

        
def service(text, **kwargs):
    """ Print a message to screen (stderr) meant to be flushed out and re-printed again modified, e.g. in a progress bar style.
    
    Args:
     text (str):  message to be printed
     how (str):   termcodes for markup. See write() 

    Returns: None
    """
    if not sys.stdout.isatty(): return
    global printed_rchar
    write("\r"+text, end='', is_service=True, **kwargs)
    printed_rchar=len(text)

    
def printerr(text, *args, **kwargs):
    """ Prints message to stderr, optionally using markup (e.g. colored text). Note: it also prints to logfile if defined (see set_logfile).

    Args:    see write function
    Returns: None
    """ 
    write(text, *args, **kwargs, is_stderror=True)

    
def set_logfile(fileh_or_path):
    """ After setting this, all messages printed with write() or printerr() are also sent to logfile.
    
    Args:
     fileh_or_path (file|str): file path specification or buffer to print a copy of all messages to

    Returns: None
    """
    global logfile
    if type(fileh_or_path) is str:
        logfile=open(fileh_or_path, 'w')
    elif type(fileh_or_path) is file:
        logfile=fileh_or_path
    else:
        raise Exception(f"set_logfile ERROR expected string or file, got this instead: {type(fileh_or_path)} {fileh_or_path}")
    
def set_markup_keywords(kwords):
    """ Set a syntax to always print certain words using a specific markup
    
    Args:
     kwords (dict) key:termcode, where key is any string, and termcode any comma-separated combination of these:
      black blink blue bright cyan dim green hidden magenta red reverse underscore white yellow

    Returns: None
    """
    
    global markup_keywords
    markup_keywords=kwords


def set_markup_usage(setting):
    """ Turns off or on the usage of colors and other terminal markup
    
    Args:
     setting (bool): new setting, use False to turn off markup, True to turn back on

    Returns: None
    """
    global no_colors
    no_colors= not setting
