# pySISL 

A Python library for serialising and deserialising SISL (Simple Information Serialization Language). SISL is a simple structured text format designed for use in the [NCSC Safely Importing Data Pattern](https://www.ncsc.gov.uk/guidance/pattern-safely-importing-data). This library provides the ability to serialise and deserialise SISL as well as perform semantic verification of the SISL.

Hardware enforced syntatic verification may be carried out by the [Oakdoor<sup>TM</sup> family of data diodes](https://www.paconsulting.com/services/product-design-and-engineering/data-diode/).

Also provides the functionality to wrap and unwrap files with an XOR scrambling technique used on the Oakdoor<sup>TM</sup> data diodes which is designed to render files inert if they fail the syntatic verification allowing the file to be safely transported or stored for later unwrapping and inspection.

## Examples
Encoding basic Python dictionary hierarchies to SISL:

    >>> import pysisl
    >>> pysisl.dumps({"hello": "world"}) 
    '{hello": !str "world"}'
    >>> pysisl.dumps({"name": "helpful_name", "flag": False, "count": 3}) 
    '{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'

Decoding SISL to Python:

    >>> import pysisl
    >>> pysisl.loads('{name: !str "helpful_name", flag: !bool "false", count: !int "3"}') 
    {'name': 'helpful_name', 'flag': False, 'count': 3}

## Basic Usage
    pysisl.dumps(dict)  
  Serialise a Python dictionary object into a SISL formatted str. 

    pysisl.loads(sisl, schema=None)  
  Deserialise SISL str to a Python dictionary. Optionally, verify the SISL schema using a json schema.

    pysisl.wraps(data)
  Applies an XOR data scrambling technique to wrap and render data inert, equivalent to the Oakdoor<sup>TM</sup> data diode hardware. The XOR key is internally generated and prepended as part of a header.

    pysisl.unwraps(data)
  Unwraps data scrambled with the above XOR data scrambling technique.
  

See the [conversion](#conversion-table) table on this page for more details.

### Splitting large objects into multiple SISL files
pySISL supports a maximum length in bytes for SISL files. If the input Python object exceeds this max length it is split into multiple SISL files. A Python list is returned where each item is a SISL string.

#### Split an object into SISL with max bytes as 20

    >>> import pysisl
    >>> pysisl.dumps({"abc": 2, "def": 3}, max_length=20)
    ['{abc: !int "2"}', '{def: !int "3"}']

### Joining multiple SISL files to form a single Python object
If a SISL file has been split in the way described above, pySISL supports joining the split files into a single Python object. When a list of SISL strings is passed to pySISL.loads(), this joining is done by default. A single Python dictionary is returned. Joining is done by merging nesting structures of arbitrary depth, while maintaining order.

    >>> import pysisl
    >>> pysisl.loads(['{abc: !list {_0: !str "I", _1: !list {_0: !str "am"}}}', 
                      '{abc: !list {_1: !list {_1: !str "a"}, _2: !str "list"}}'])

    {"abc": ['I', ['am', 'a'], 'list']}

    >>> pysisl.loads(['{abc: !list {_0: !str "I", _1: !list {_0: !str "am"}}}',
                      '{abc: !list {_2: !list {_0: !str "a"}, _3: !str "list"}}'])

    {"abc": ['I', ['am'], ['a'], 'list']}

### Semantic Verification with a Schema
The [jsonschema](https://pypi.org/project/jsonschema/) library is used to optionally verify the parsed SISL data structure. See [JSON Schema](https://json-schema.org/) for details on the json schema syntax. For example

#### Successful Parsing

    >>> import pysisl
    >>> my_schema = {
            "properties": {
                "name": {
                    "type": "string"
                },
                "flag": {
                    "type": "boolean" 
                },
                "count": {
                    "type": "number"
                }
            }
        }
    >>> decode_example = '{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'
    >>> pysisl.loads(decode_example, my_schema)
    {'name': 'helpful_name', 'flag': False, 'count': 3}

#### Schema Verification Fails

    >>> import pysisl
    >>> my_schema = {
            "properties": {
                "name": {
                    "type": "string"
                },
                "flag": {
                    "type": "boolean" 
                },
                "count": {
                    "type": "string"
                }
            }
        }
    >>> decode_example = '{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'
    >>> pysisl.loads(decode_example, my_schema)
    Traceback (most recent call last):
        File "/home/vagrant/pysisl/pysisl/sisl_decoder.py", line 31, in _verify_schema_if_required
            json_validator(flattened_sisl, schema=schema, format_checker=FormatChecker())
        File "/home/vagrant/pysisl/venv/lib64/python3.6/site-packages/jsonschema/validators.py", line 934, in validate
    raise error
            jsonschema.exceptions.ValidationError: 3 is not of type 'string'
    
    Failed validating 'type' in schema['properties']['count']:
            {'type': 'string'}


#### Conversion table

    | Python | SISL |
    | ------ | ---- |
    | dict   | obj  |
    | list   | list |
    | str    | str  |
    | int    | int  |
    | float  | float|
    | bool   | bool |
    | None   | null |


## Background
The [NCSC Safely Importing Data Pattern](https://www.ncsc.gov.uk/guidance/pattern-safely-importing-data), an architecture pattern describes a safe mechanism for handling structured data from an external untrusted source. We use a Transform - Verify approach taking our source data, transforming to an intermediate format, inspecting the intermediate format and then transforming back to the original format. SISL was designed to be a simple and easily inspectable intermediate format for just such an approach.

Oakdoor<sup>TM</sup> products enable one- or two-way data transfers between segregated networks, letting organisations safely run services, such as file transfer, protocol exchanges, secure internet browsing and systems management. This is done using a combination of hardware enforced verification and software.

pySISL can form part of the transformation engine sub-system that enables cross-network communication that is compatible with the NCSC Safely importing data pattern. The pySISL encoder can be used to convert complex Python dictionaries into valid SISL that is compatible with the diodes and the decoder will convert the SISL back into the same dictionaries without loss of data.


## License
MIT licence

## SISL Specification
For reference, this is ABNF for SISL.    

    sislfile        = grouping *255wsp
    grouping        = "{" ( (*255wsp collection *255wsp ) / *255wsp ) "}"
    collection      = element *("," *255wsp element)
    element         = name ":" 1*255wsp "!" type 1*255wsp value 
    name            = ( "_" / ALPHA ) *( "_" / "-" / "." / ALPHA / DIGIT )
    type            = ( "_" / ALPHA ) *254( "_" / "-" / "." / ALPHA / DIGIT )
    value           = ( DQUOTE *( printable / escape) DQUOTE ) / grouping
    escape          = "\" ( lcr / lct / lcn / DQUOTE / "\" / (lcx 2HEXDIG) / (lcu 4HEXDIG) / (ucu 8HEXDIG) )
    wsp             = SP / HTAB / CR / LF
    printable       = %x20-21 / %x23-5B / %x5D-7E             ; Printable chars apart from '"' or '\'
    
    lcr             = %x72                                    ; lower case r
    lct             = %x74                                    ; lower case t
    lcn             = %x6E                                    ; lower case n
    lcx             = %x78                                    ; lower case x
    lcu             = %x75                                    ; lower case u
    ucu             = %x55                                    ; upper case u
    
    ; Core rules
    ALPHA           = %x41-5A / %x61-7A                       ; A-Z / a-z
    DIGIT           = %x30-39                                 ; 0-9
    DQUOTE          = %x22                                    ; " (double-quote)
    SP              = %x20                                    ; space
    HTAB            = %x09                                    ; horizontal tab
    CR              = %x0D                                    ; carriage return
    LF              = %x0A                                    ; line feed

## Getting Help
If you need help using the pySISL module, please contact Oakdoor<sup>TM</sup> support at oakdoor.support@paconsulting.com. 

## Contributing to pySISL
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

If you notice a bug or would like to make an update to pySISL, please open an issue or raise a pull request.  



