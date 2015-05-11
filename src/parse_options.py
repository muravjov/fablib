# coding: utf-8

def parse_options(usage=None, parser_fnr=None, num_args=None, args=None):
    """ parser_fnr - to add options for parser
    num_args - required number of args
    args - if not None then use them instead of sys.argv[1:] """
    from optparse import OptionParser
    import sys
    parser = OptionParser(usage=usage)

    if parser_fnr:
        parser_fnr(parser)
    options, args = parser.parse_args(args)

    if num_args != None and len(args) != num_args:
        parser.print_help()
        sys.exit(1)

    return options, args

def parse_opts_args(parser_fnr, *args):
    return parse_options("usage: %prog [options] " + " ".join(args), parser_fnr=parser_fnr, num_args=len(args))

def parse_args(*args):
    return parse_opts_args(None, *args)[1]

def parse_one_arg(arg_name):
    return parse_args(arg_name)[0]

def add_bool_option(parser, name, var_name, help_str):
    """ name - "-s" либо "--long_bool_option" """
    parser.add_option(name, action="store_true", dest=var_name, default=False,
                      help=help_str)

def parse_1bool_args(b_name, b_var_name, b_help_str, *args):
    def add_options(parser):
        add_bool_option(parser, b_name, b_var_name, b_help_str)
    return parse_opts_args(add_options, *args)
        
