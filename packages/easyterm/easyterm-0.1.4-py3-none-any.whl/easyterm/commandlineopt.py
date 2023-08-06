import sys, shlex, string, copy, re, os, warnings
from .colorprint import write 
__all__ = ["command_line_options","NoTracebackError",  "set_up_no_traceback_error"]

# "CommandLineOptions", "CommandLineError" 

def custom_formatwarning(msg, *args, **kwargs):
    return str(msg) + '\n'
warnings.formatwarning = custom_formatwarning


class CommandLineOptions(dict):
    """ Subclass of dict designed to store options of the command line.
    Two differences with dict:
     - its representation looks good on screen
     - requesting a key which is absent returns None, instead of throwing an error
    """
    accepted_option_chars=set(string.ascii_uppercase + string.ascii_lowercase)
    accepted_option_types=set([bool, int, float, list, str])    

    def __repr__(self):
        max_charlen=max( [ len(k) for k in self] )
        return('\n'.join( [f"{k:<{max_charlen}} : {type(self[k]).__name__:<5} = {self[k]}" for k in sorted(self.keys())]) )
    
    def __getitem__(self, name):
        if name in self:            return dict.__getitem__(self, name)
        else:                       return None

        
class NoTracebackError(Exception):
    """Exception class which, when raised, shows the error message only, without traceback.
    Its usage requires running set_up_no_traceback_error()
    """
    pass

class CommandLineError(NoTracebackError):
    """Exception class indicating an error occured while reading command line options."""

def set_up_no_traceback_error(set_on=True):
    """After this, raising NoTracebackError or its subclasses results in single error line, without traceback.
    Under the hood, replaces sys.excepthook
    
    Args:
     set_on (bool): normally True. Call this fn with set_on=False to restore the default sys.excepthook

    Returns: None
    """
    def excepthook_allowing_notraceback(type, value, traceback):
        if issubclass(type, NoTracebackError):              sys.exit(str(value))
        return(sys.__excepthook__(type, value, traceback))  
    if set_on:
        sys.excepthook=excepthook_allowing_notraceback
    else: 
        sys.excepthook=sys.__excepthook__
        
set_up_no_traceback_error()

def command_line_options(default_opt,
                         help_msg='Command line usage:...',
                         positional_keys='io',
                         synonyms={},
                         tolerate_extra=False,
                         tolerated_regexp=[],
                         warning_extra=True,
                         advanced_help_msg={}):
    """Fetches command line keys (e.g. -i ) and theirs arguments from the command line, and returns them after filling with default values
    
    Args:
    * default_opt (dict):      default arguments for all keys. Their value types also define the typing enforced on command line arguments
         possible value types are int, float, str, bool (argument can be omitted), list (multiple args accepted)
    + help_msg (str):          if -h | -help | --help is provided, this help is displayed and the script exits
    + positional_keys (iter):  these keys will be associated, in order, to args with no explicit keys (e.g. script.py arg1 arg2)
    + synonyms (dict):         add synonyms for keys; e.g. {'inputfile':'i',  'p':'param'}; the built-in {'help':'h'} is added

    + tolerate_extra (bool):    normally any keys not found in default_opt raises an error; this allows to tolerate & accept unexpected keys
    + tolerated_regexp (list):  define which unexpected keys to tolerate using regexp employed by module re
    + warning_extra (bool):     when keys are tolerated (two previous fn args), normally a warning is printed; set to False to silence these
    + advanced_help_msg (dict): dictionary defining specialized help messages displayed only when invoked as argument to -h

    Returns: 
     opt (CommandLineOpt):      dictionary like structure with structure key:arg

  Examples:     

   command_line_options( default_opt={'i': 'input', 'o':'output', 'param':3} )
    script.py -i file1  -o file2   # --> {'i':'file1', 'o':'file2', 'param':3}
    script.py -i file1  -param -1  # --> {'i':'file1', 'o':'output', 'param':-1}   # note param is cast to int

   command_line_options( default_opt={'param':3, 'files':[]},  synonyms={'p':'param'})
    script.py -files a b c d e -p 10   # --> {'files':['a', 'b', 'c', 'd', 'e'], 'param':10}  # note -p as synonym

   command_line_options( default_opt={'i':'', 'o':'', 's':'', 'k':5.5},  positional_keys=['i', 'o'])
    script.py -k 4.5 in out     # --> {'i':'in', 'o':'out', 's':'', 'k':4.5}   # positional args
    script.py in out -k 10      # --> {'i':'in', 'o':'out', 's':'', 'k':10.0}  # this order also accepted  # note -k cast to float
    script.py in -s "multi word str"   # --> {'i':'', 'o':'', 's':'multi char str', 'k':5.5}  # multiword string as arg
    """
    
    default_opt=CommandLineOptions(default_opt)
    for builtin_opt in ['h', 'print_opt']:
        if not builtin_opt in default_opt:
            default_opt[builtin_opt]=False

    opt=CommandLineOptions()
    arglist=sys.argv[1:]
    synonyms['help']='h'                   # built-in synonym

    ## checking default_opt and positional_keys
    for opt_key in default_opt:
        expected_type=type(default_opt[opt_key])
        if not expected_type in CommandLineOptions.accepted_option_types:
            raise CommandLineError( (f"ERROR Only these value types are "
                                               f"accepted (default_opt): {CommandLineOptions.accepted_option_types} "
                                               f"-- Instead it was provided {expected_type} for -{opt_key}"))
        if expected_type is list and any( [not type(x) is str   for x in default_opt[opt_key]]  ):
            raise CommandLineError((f"ERROR default options: each list type option must "
                                              f"contain string values only! Instead this was "
                                              f"provided for -{opt_key} : {default_opt[opt_key]}"))        
    if len([pk for pk in positional_keys if not pk in default_opt]):
        raise CommandLineError((f"ERROR positional keys provided are absent from default option: "
                                f"{' '.join(['-'+pk for pk in positional_keys if not pk in default_opt])}"))

    
    ## below: identifying those bit which are an option, like '-k' or '-test' or '--char'
    opt_key_indices=[i     for i, bit in enumerate(arglist)   
                     if bit.startswith('-') and len(bit.split())==1 and 
                            len(bit)>1 and bit[1] in CommandLineOptions.accepted_option_chars]

    ## dealing with positional arguments, provided before explicit options (or with no options)
    positionals=None
    if len(arglist) and (not len(opt_key_indices) or opt_key_indices[0]!=0):
        positionals='before'
        from_here=0
        up_to=None if not len(opt_key_indices) else opt_key_indices[0]
        
    ## dealing with positional arguments, provided after explicit options
    if len(arglist) and len(opt_key_indices):
        last_ki=opt_key_indices[-1]
        last_k= arglist[last_ki].lstrip('-')        
        if ( last_ki < len(arglist)-2 and
               #(type(default_opt[last_k]) is bool and last_ki < len(arglist)-1) )
             not type(default_opt[last_k]) is list):
            if positionals=='before':
                raise CommandLineError(f"ERROR you can provide positional arguments before "
                                       f"OR after other options, not both! ")
            positionals='after'
            if type(default_opt[last_k]) is bool:
                if  len(arglist)>last_ki+1 and  arglist[last_ki+1] in ('0', '1'):
                    from_here=last_ki+2
                else:
                    from_here=last_ki+1
            else:
                from_here=last_ki+2
            up_to=None

    
            
    ## inserting implied positional option keys explicitly in arglist
    if positionals:
        if not positional_keys: positional_keys=[]  # will result in error below; just saving some code
        insert_these=[]
        for i, value in enumerate(arglist[from_here:up_to]):
            if len(positional_keys)<i+1:
                if tolerate_extra:
                    warnings.warn((f"command_line_options WARNING ignoring extra argument: "
                              f"{' '.join(arglist[from_here+1:up_to])}"))
                else:
                    raise CommandLineError((f"ERROR extra argument not accepted: "
                                            f"{' '.join(arglist[from_here+i:up_to])}"))
                break
            insert_these.append( [from_here+i, positional_keys[i]])
            if type(default_opt[ positional_keys[i] ]) is list: break

        for i, key_opt in insert_these[::-1]:
            arglist.insert(i, f"-{key_opt}")

        opt_key_indices=[i     for i, bit in enumerate(arglist)   
                                if bit.startswith('-') and len(bit.split())==1 and 
                                len(bit)>1 and bit[1] in CommandLineOptions.accepted_option_chars]


    ##### 
    ## main block: going one option at the time, parsing arglist
    for ni, i in enumerate(opt_key_indices):
        ## some internal bits are ignored: e.g.   -n 8 these are all ignored -k 7
        if (ni>0 and opt_key_indices[ni-1]+1 < i-1 and
            not type(default_opt[opt_key]) is list): # note here opt_key is the previous one
            if tolerate_extra:
                warnings.warn((f"command_line_options WARNING ignoring extra argument: "
                          f"{' '.join(arglist[opt_key_indices[ni-1]+2:i])}"))
            else:
                raise CommandLineError((f"ERROR extra argument not accepted: "
                                        f"{' '.join(arglist[opt_key_indices[ni-1]+2:i])}"))             
        
        bit=arglist[i]
        opt_key=bit.lstrip('-')
        if opt_key in synonyms:
            opt_key=synonyms[opt_key]

        ## Extra option, not present in default_opt
        if not opt_key in default_opt:
            if (tolerate_extra or 
                (len(tolerated_regexp)>0 and
                 match_any_word(opt_key, tolerated_regexp, ignore_case=False))):
                # not expecting this option but we tolerate it
                if warning_extra:
                    warnings.warn(f"command_line_options WARNING accepting unexpected command line option: -{opt_key}")
                expected_type=None                    
            else:
                raise CommandLineError(f"ERROR Unexpected command line option: -{opt_key}")
        else:
            expected_type=type(default_opt[opt_key])

        ## assigning a value of the appropriate type  
        next_ki=opt_key_indices[ni+1]   if len(opt_key_indices)>ni+1   else None #None if last option key

        if not expected_type is list:
            vi=i+1  #value index in arglist
            if ((not next_ki is None and  next_ki==vi) or
                (next_ki is None) and len(arglist)-1==i):
                # option is provided without argument
                if expected_type is bool or expected_type is None:
                    value=True
                else:
                    raise CommandLineError((f"ERROR {expected_type} expected type "
                                            f"for option -{opt_key} but no argument provided!"))
            else:
                if expected_type is None:  # if this option was not in default_opt, we cast it to string (unless it had no argument, in which case to bool)
                    expected_type=str
                if expected_type is bool:
                    if   arglist[i+1]=='1':
                        value=True
                    elif arglist[i+1]=='0':
                        value=False
                    else:
                        raise CommandLineError(f"ERROR boolean options can only take values 0, 1 or none. Received: -{opt_key} : {arglist[i+1]}") from None
                else:
                  try:
                      value= expected_type(  arglist[i+1] ) 
                  except ValueError as e:
                      raise CommandLineError(f"ERROR wrong type for option -{opt_key} : {e}") from None
        else:  # expected_type is list: takes all values after this
            vis=[vi for vi in range(i+1, next_ki   if not next_ki is None else len(arglist))]     # value indices
            value=[arglist[vi] for vi in vis]  # list of strings
        opt[opt_key]=value

    ## adding default values which were not specified in command line
    for opt_key in default_opt:
        if not opt_key in opt:
            opt[opt_key]=copy.copy(default_opt[opt_key])

    ## Printing help message
    if opt['h']:
        write(help_msg)        
        if advanced_help_msg and opt['h'] in advanced_help_msg:            
            write(advanced[opt['h']])
            
    if opt['print_opt']:
        write(opt)
            
    if 'h' in opt and opt['h']:
        sys.exit()            

    return(opt)

def match_any_word(main_string, word_list, is_pattern=True, ignore_case=True):
  """ Given a string and a list of strings/perl_patterns, it returns True is any of them matches the string, False otherwise  """
  for w in word_list:
      if is_pattern:
          if ignore_case:          pattern=re.compile(w, re.IGNORECASE)
          else:                    pattern=re.compile(w)
          if pattern.search(main_string):          return(True)
      else:
          if ignore_case:
              if w.lower() in main_string.lower():  return(True)
          elif w in main_string:                  return(True)
  return(False)

