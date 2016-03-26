from ctypes import *


class user_regs_struct(Structure):
	_fields_ = [

		("ebx",	c_ulong),	
		("ecx",	c_ulong),	
		("edx",	c_ulong),	
		("esi",	c_ulong),	
		("edi",	c_ulong),	
		("ebp",	c_ulong),	
		("eax",	c_ulong),	
		("xds",	c_ulong),	
		("xes",	c_ulong),	
		("xfs",	c_ulong),	
		("xgs",	c_ulong),	
		("orig_eax", c_ulong),	
		("eip",	c_ulong),	
		("xcs",	c_ulong),	
		("eflags",	c_ulong),	
		("esp",	c_ulong),	
		("xss",	c_ulong),	
	]
