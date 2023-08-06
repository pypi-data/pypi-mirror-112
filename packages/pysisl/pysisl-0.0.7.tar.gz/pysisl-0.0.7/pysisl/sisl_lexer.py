# Copyright PA Knowledge Ltd 2021

#
# rYAMLfile       = grouping *255WSP
#
# grouping        = "{" *255WSP ( name ":" 1*255WSP "!" type 1*255WSP value *255WSP *( "," *255WSP name ":" 1*255WSP "!" type 1*255WSP value *255WSP ) / "" ) "}"
#
# name            = ( "_" / ALPHA ) *( "_" / "-" / "." / ALPHA / DIGIT )
#
# type            = ( "_" / ALPHA ) *254( "_" / "-" / "." / ALPHA / DIGIT )
#
# value           = ( DQUOTE *( PRINTABLE / ESCAPE) DQUOTE ) / grouping
#
# ESCAPE          = "\" ( LCR / LCT / LCN / DQUOTE / "\" / (LCX 2HEX) / (LCU 4HEX) / (UCU 8HEX) )
#
# HEX             = DIGIT / %x41-46 / %x61-66
#
# WSP             = SP / HTAB / CR / LF
#
# PRINTABLE       = %x20-21 / %x23-5B / %x5D-7E             ; Printable chars apart from '"' or '\'
# ALPHA           = %x41-5A / %x61-7A                       ; A-Z / a-z
# DIGIT           = %x30-39                                 ; 0-9
# DQUOTE          = %x22                                    ; " (double-quote)
# SP              = %x20                                    ; space
# HTAB            = %x09                                    ; horizontal tab
# CR              = %x0D                                    ; carriage return
# LF              = %x0A                                    ; line feed
# LCR             = %x72                                    ; lower case r
# LCT             = %x74                                    ; lower case t
# LCN             = %x6E                                    ; lower case n
# LCX             = %x78                                    ; lower case x
# LCU             = %x75                                    ; lower case u
# UCU             = %x55                                    ; upper case u
from .parser_error import ParserError


tokens = (
    'BEGIN_OBJECT',
    'END_OBJECT',
    'NAME',
    'TYPE',
    'VALUE',
    'LIST_SEPARATOR'
)

t_BEGIN_OBJECT = '{[\s]{0,255}'
t_END_OBJECT = '[\s]{0,255}}[\s]{0,255}'
t_LIST_SEPARATOR = r'[\s]{0,255},[\s]{0,255}'


# name = ( "_" / ALPHA ) *( "_" / "-" / "." / ALPHA / DIGIT ):
def t_NAME(t):
    r'[_a-zA-Z][a-zA-Z0-9-\_\.]*:[\s]{1,255}'
    t.value = t.value.rstrip()[:-1]
    return t


# type = ( "_" / ALPHA ) *254( "_" / "-" / "." / ALPHA / DIGIT )
def t_TYPE(t):
    r'\![_a-zA-Z][a-zA-Z0-9-\_\.]{0,254}[\s]{1,255}'
    t.value = t.value.rstrip()[1:]
    return t


# value = ( DQUOTE *( PRINTABLE / ESCAPE) DQUOTE ) / grouping
# ESCAPE = "\" ( LCR / LCT / LCN / DQUOTE / "\" / (LCX 2HEX) / (LCU 4HEX) / (UCU 8HEX) )
def t_VALUE(t):
    r'"([^"\\]|\\.)*"(?=\s{0,255},|\s{0,255}})'
    t.value = t.value[1:-1]  # Remove quotation marks
    return t


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    raise ParserError(t)
