__doc__ = '''Tool Set for Networking Geeks
-------------------------------------------------------------------
JSet, IPv4, IPv6, addressing, Validation,
Default, Container, Numeric, STR, IO, LST, DIC, LOG, DB, IP,
DifferenceDict, DictMethods
-------------------------------------------------------------------
 Juniper      various juniper config operations
 IPv4         IPV4 Object, and its operations
 IPv6         IPV4 Object, and its operations
 addressing   dynamic allocation of IPv4/IPv6 Objects
 Validation   Validate subnet
 Default      default implementations of docstring
 Container    default identical dunder methods implementations
 Numeric      To be implemented later
 STR          String Operations static methods 
 IO           Input/Output of text files Operations static methods 
 LST          List Operations static methods 
 DIC          Dictionary Operations static methods 
 DifferenceDict Differences between dictionaries
 DictMethods  Common Dictionary Methods
 LOG          Logging Operations static methods 
 DB           Database Operations static methods 
 IP           IP Addressing Operations static methods 
 ... and many more
-------------------------------------------------------------------
'''

__all__ = [
	# .juniper
	'Juniper',
	# Jset
	'JSet',
	# .addressing
	'IPv4', 'IPv6', 'addressing', 'Validation', 'get_summaries', 'isSubset',
	'binsubnet', 'bin2dec', 'bin2decmask', 'to_dec_mask', 'bin_mask',
	# .gpl
	'Default', 'Container', 'Numeric', 'DifferenceDict', 
	'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP', 'XL_READ', 'XL_WRITE', 
	'DictMethods', 'Multi_Execution',
	# .convertdict
	'ConvDict',
	]

__version__ = "0.0.9"

from .juniper import Juniper
from .jset import JSet

from .addressing import (
	IPv4, IPv6, addressing, Validation, get_summaries, isSubset,
	binsubnet, bin2dec, bin2decmask, to_dec_mask, bin_mask,
	)

from .gpl import (Default, Container, Numeric, 
	DifferenceDict, DictMethods, DIC,
	STR, IO, LST, LOG, DB, IP, XL_READ, XL_WRITE, 
	Multi_Execution,
	)

from .convertdict import ConvDict