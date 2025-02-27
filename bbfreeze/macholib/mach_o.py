"""
Other than changing the load commands in such a way that they do not
contain the load command itself, this is largely a by-hand conversion
of the C headers.  Hopefully everything in here should be at least as
obvious as the C headers, and you should be using the C headers as a real
reference because the documentation didn't come along for the ride.

Doing much of anything with the symbol tables or segments is really
not covered at this point.

See /usr/include/mach-o and friends.
"""
import time

from macholib.ptypes import *

CPU_TYPE_NAMES = {
    -1:     'ANY',
    1:      'VAX',
    6:      'MC680x0',
    7:      'i386',
    8:      'MIPS',
    10:     'MC98000',
    11:     'HPPA',
    12:     'ARM',
    13:     'MC88000',
    14:     'SPARC',
    15:     'i860',
    16:     'Alpha',
    18:     'PowerPC',
}

_MH_EXECUTE_SYM = "__mh_execute_header"
MH_EXECUTE_SYM = "_mh_execute_header"
_MH_BUNDLE_SYM = "__mh_bundle_header"
MH_BUNDLE_SYM = "_mh_bundle_header"
_MH_DYLIB_SYM = "__mh_dylib_header"
MH_DYLIB_SYM = "_mh_dylib_header"
_MH_DYLINKER_SYM = "__mh_dylinker_header"
MH_DYLINKER_SYM = "_mh_dylinker_header"

(
    MH_OBJECT, MH_EXECUTE, MH_FVMLIB, MH_CORE, MH_PRELOAD, MH_DYLIB,
    MH_DYLINKER, MH_BUNDLE, MH_DYLIB_STUB,
) = range(0x1, 0xa)

(
    MH_NOUNDEFS, MH_INCRLINK, MH_DYLDLINK, MH_BINDATLOAD, MH_PREBOUND,
    MH_SPLIT_SEGS, MH_LAZY_INIT, MH_TWOLEVEL, MH_FORCE_FLAT, MH_NOMULTIDEFS,
    MH_NOFIXPREBINDING
) = map((1).__lshift__, range(11))

MH_MAGIC = 0xfeedfaceL
MH_CIGAM = 0xcefaedfeL
MH_MAGIC_64 = 0xfeedfacfL
MH_CIGAM_64 = 0xcffaedfeL

integer_t = p_int
cpu_type_t = integer_t
cpu_subtype_t = integer_t

MH_FILETYPE_NAMES = {
    MH_OBJECT:      'relocatable object',
    MH_EXECUTE:     'demand paged executable',
    MH_FVMLIB:      'fixed vm shared library',
    MH_CORE:        'core',
    MH_PRELOAD:     'preloaded executable',
    MH_DYLIB:       'dynamically bound shared library',
    MH_DYLINKER:    'dynamic link editor',
    MH_BUNDLE:      'dynamically bound bundle',
    MH_DYLIB_STUB:  'shared library stub for static linking',
}

MH_FILETYPE_SHORTNAMES = {
    MH_OBJECT:      'object',
    MH_EXECUTE:     'execute',
    MH_FVMLIB:      'fvmlib',
    MH_CORE:        'core',
    MH_PRELOAD:     'preload',
    MH_DYLIB:       'dylib',
    MH_DYLINKER:    'dylinker',
    MH_BUNDLE:      'bundle',
    MH_DYLIB_STUB:  'dylib_stub',
}

MH_FLAGS_NAMES = {
    MH_NOUNDEFS:    'no undefined references',
    MH_INCRLINK:    'output of an incremental link',
    MH_DYLDLINK:    'input for the dynamic linker',
    MH_BINDATLOAD:  'undefined references bound dynamically when loaded',
    MH_PREBOUND:    'dynamic undefined references prebound',
    MH_SPLIT_SEGS:  'split read-only and read-write segments',
    MH_LAZY_INIT:   '(obsolete)',
    MH_TWOLEVEL:    'using two-level name space bindings',
    MH_FORCE_FLAT:  'forcing all imagges to use flat name space bindings',
    MH_NOMULTIDEFS: 'umbrella guarantees no multiple definitions',
    MH_NOFIXPREBINDING: 'do not notify prebinding agent about this executable',
}

class mach_version_helper(Structure):
    _fields_ = (
        ('major', p_ushort),
        ('minor', p_ubyte),
        ('rev', p_ubyte),
    )
    def __str__(self):
        return '%s.%s.%s' % (self.major, self.minor, self.rev)

class mach_timestamp_helper(p_ulong):
    def __str__(self):
        return time.ctime(self)

def read_struct(f, s, **kw):
    return s.from_fileobj(f, **kw)

class mach_header(Structure):
    _fields_ = (
        ('magic', p_ulong),
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('filetype', p_ulong),
        ('ncmds', p_ulong),
        ('sizeofcmds', p_ulong),
        ('flags', p_ulong),
    )
    def _describe(self):
        bit = 1L
        flags = self.flags
        dflags = []
        while flags and bit < (1<<32L):
            if flags & bit:
                dflags.append(MH_FLAGS_NAMES.get(bit, str(bit)))
                flags = flags ^ bit
            bit <<= 1L
        return (
            ('magic', '0x%08X' % self.magic),
            ('cputype', CPU_TYPE_NAMES.get(self.cputype, self.cputype)),
            ('cpusubtype', self.cpusubtype),
            ('filetype', MH_FILETYPE_NAMES.get(self.filetype, self.filetype)),
            ('ncmds', self.ncmds),
            ('sizeofcmds', self.sizeofcmds),
            ('flags', dflags),
        )

class mach_header_64(mach_header):
    _fields_ = mach_header._fields_ + (('reserved', p_ulong),)

class load_command(Structure):
    _fields_ = (
        ('cmd', p_ulong),
        ('cmdsize', p_ulong),
    )

LC_REQ_DYLD = 0x80000000L

(
    LC_SEGMENT, LC_SYMTAB, LC_SYMSEG, LC_THREAD, LC_UNIXTHREAD, LC_LOADFVMLIB,
    LC_IDFVMLIB, LC_IDENT, LC_FVMFILE, LC_PREPAGE, LC_DYSYMTAB, LC_LOAD_DYLIB,
    LC_ID_DYLIB, LC_LOAD_DYLINKER, LC_ID_DYLINKER, LC_PREBOUND_DYLIB,
    LC_ROUTINES, LC_SUB_FRAMEWORK, LC_SUB_UMBRELLA, LC_SUB_CLIENT,
    LC_SUB_LIBRARY, LC_TWOLEVEL_HINTS, LC_PREBIND_CKSUM
) = range(0x1, 0x18)

LC_LOAD_WEAK_DYLIB = LC_REQ_DYLD | 0x18

LC_SEGMENT_64 = 0x19
LC_ROUTINES_64 = 0x1a
LC_UUID = 0x1b
LC_RPATH = (0x1c | LC_REQ_DYLD)
LC_CODE_SIGNATURE = 0x1d
LC_CODE_SEGMENT_SPLIT_INFO = 0x1e
LC_REEXPORT_DYLIB = 0x1f | LC_REQ_DYLD

# this is really a union.. but whatever
class lc_str(p_ulong):
    pass

p_str16 = pypackable('p_str16', str, '16s')

vm_prot_t = p_int
class segment_command(Structure):
    _fields_ = (
        ('segname', p_str16),
        ('vmaddr', p_ulong),
        ('vmsize', p_ulong),
        ('fileoff', p_ulong),
        ('filesize', p_ulong),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', p_ulong), # read the section structures ?
        ('flags', p_ulong),
    )

class segment_command_64(Structure):
    _fields_ = (
        ('segname', p_str16),
        ('vmaddr', p_ulonglong),
        ('vmsize', p_ulonglong),
        ('fileoff', p_ulonglong),
        ('filesize', p_ulonglong),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', p_ulong), # read the section structures ?
        ('flags', p_ulong),
    )

SG_HIGHVM = 0x1
SG_FVMLIB = 0x2
SG_NORELOC = 0x4

class section(Structure):
    _fields_ = (
        ('sectname', p_str16),
        ('segname', p_str16),
        ('addr', p_ulong),
        ('size', p_ulong),
        ('offset', p_ulong),
        ('align', p_ulong),
        ('reloff', p_ulong),
        ('nreloc', p_ulong),
        ('flags', p_ulong),
        ('reserved1', p_ulong),
        ('reserved2', p_ulong),
    )

class section_64(Structure):
    _fields_ = (
        ('sectname', p_str16),
        ('segname', p_str16),
        ('addr', p_ulonglong),
        ('size', p_ulonglong),
        ('offset', p_ulong),
        ('align', p_ulong),
        ('reloff', p_ulong),
        ('nreloc', p_ulong),
        ('flags', p_ulong),
        ('reserved1', p_ulong),
        ('reserved2', p_ulong),
        ('reserved3', p_ulong),
    )

SECTION_TYPE = 0xffL
SECTION_ATTRIBUTES = 0xffffff00L
S_REGULAR = 0x0
S_ZEROFILL = 0x1
S_CSTRING_LITERALS = 0x2
S_4BYTE_LITERALS = 0x3
S_8BYTE_LITERALS = 0x4
S_LITERAL_POINTERS = 0x5
S_NON_LAZY_SYMBOL_POINTERS = 0x6
S_LAZY_SYMBOL_POINTERS = 0x7
S_SYMBOL_STUBS = 0x8
S_MOD_INIT_FUNC_POINTERS = 0x9
S_MOD_TERM_FUNC_POINTERS = 0xa
S_COALESCED = 0xb

SECTION_ATTRIBUTES_USR = 0xff000000L
S_ATTR_PURE_INSTRUCTIONS = 0x80000000L
S_ATTR_NO_TOC = 0x40000000L
S_ATTR_STRIP_STATIC_SYMS = 0x20000000L
SECTION_ATTRIBUTES_SYS = 0x00ffff00L
S_ATTR_SOME_INSTRUCTIONS = 0x00000400L
S_ATTR_EXT_RELOC = 0x00000200L
S_ATTR_LOC_RELOC = 0x00000100L


SEG_PAGEZERO =    "__PAGEZERO"
SEG_TEXT =    "__TEXT"
SECT_TEXT =   "__text"
SECT_FVMLIB_INIT0 = "__fvmlib_init0"
SECT_FVMLIB_INIT1 = "__fvmlib_init1"
SEG_DATA =    "__DATA"
SECT_DATA =   "__data"
SECT_BSS =    "__bss"
SECT_COMMON = "__common"
SEG_OBJC =    "__OBJC"
SECT_OBJC_SYMBOLS = "__symbol_table"
SECT_OBJC_MODULES = "__module_info"
SECT_OBJC_STRINGS = "__selector_strs"
SECT_OBJC_REFS = "__selector_refs"
SEG_ICON =     "__ICON"
SECT_ICON_HEADER = "__header"
SECT_ICON_TIFF =   "__tiff"
SEG_LINKEDIT =    "__LINKEDIT"
SEG_UNIXSTACK =   "__UNIXSTACK"

#
#  I really should remove all these _command classes because they
#  are no different.  I decided to keep the load commands separate,
#  so classes like fvmlib and fvmlib_command are equivalent.
#

class fvmlib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('minor_version', mach_version_helper),
        ('header_addr', p_ulong),
    )

class fvmlib_command(Structure):
    _fields_ = fvmlib._fields_

class dylib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('timestamp', mach_timestamp_helper),
        ('current_version', mach_version_helper),
        ('compatibility_version', mach_version_helper),
    )

# merged dylib structure
class dylib_command(Structure):
    _fields_ = dylib._fields_

class sub_framework_command(Structure):
    _fields_ = (
        ('umbrella', lc_str),
    )

class sub_client_command(Structure):
    _fields_ = (
        ('client', lc_str),
    )

class sub_umbrella_command(Structure):
    _fields_ = (
        ('sub_umbrella', lc_str),
    )

class sub_library_command(Structure):
    _fields_ = (
        ('sub_library', lc_str),
    )

class prebound_dylib_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('nmodules', p_ulong),
        ('linked_modules', p_ulong),
    )

class dylinker_command(Structure):
    _fields_ = (
        ('name', lc_str),
    )

class thread_command(Structure):
    _fields_ = (
    )

class routines_command(Structure):
    _fields_ = (
        ('init_address', p_ulong),
        ('init_module', p_ulong),
        ('reserved1', p_ulong),
        ('reserved2', p_ulong),
        ('reserved3', p_ulong),
        ('reserved4', p_ulong),
        ('reserved5', p_ulong),
        ('reserved6', p_ulong),
    )

class routines_command_64(Structure):
    _fields_ = (
        ('init_address', p_ulonglong),
        ('init_module', p_ulonglong),
        ('reserved1', p_ulonglong),
        ('reserved2', p_ulonglong),
        ('reserved3', p_ulonglong),
        ('reserved4', p_ulonglong),
        ('reserved5', p_ulonglong),
        ('reserved6', p_ulonglong),
    )

class symtab_command(Structure):
    _fields_ = (
        ('symoff', p_ulong),
        ('nsyms', p_ulong),
        ('stroff', p_ulong),
        ('strsize', p_ulong),
    )

class dysymtab_command(Structure):
    _fields_ = (
        ('ilocalsym', p_ulong),
        ('nlocalsym', p_ulong),
        ('iextdefsym', p_ulong),
        ('nextdefsym', p_ulong),
        ('iundefsym', p_ulong),
        ('nundefsym', p_ulong),
        ('tocoff', p_ulong),
        ('ntoc', p_ulong),
        ('modtaboff', p_ulong),
        ('nmodtab', p_ulong),
        ('extrefsymoff', p_ulong),
        ('nextrefsyms', p_ulong),
        ('indirectsymoff', p_ulong),
        ('nindirectsyms', p_ulong),
        ('extreloff', p_ulong),
        ('nextrel', p_ulong),
        ('locreloff', p_ulong),
        ('nlocrel', p_ulong),
    )

INDIRECT_SYMBOL_LOCAL = 0x80000000L
INDIRECT_SYMBOL_ABS = 0x40000000L

class dylib_table_of_contents(Structure):
    _fields_ = (
        ('symbol_index', p_ulong),
        ('module_index', p_ulong),
    )

class dylib_module(Structure):
    _fields_ = (
        ('module_name', p_ulong),
        ('iextdefsym', p_ulong),
        ('nextdefsym', p_ulong),
        ('irefsym', p_ulong),
        ('nrefsym', p_ulong),
        ('ilocalsym', p_ulong),
        ('nlocalsym', p_ulong),
        ('iextrel', p_ulong),
        ('nextrel', p_ulong),
        ('iinit_iterm', p_ulong),
        ('ninit_nterm', p_ulong),
        ('objc_module_info_addr', p_ulong),
        ('objc_module_info_size', p_ulong),
    )

class dylib_module_64(Structure):
    _fields_ = (
        ('module_name', p_ulong),
        ('iextdefsym', p_ulong),
        ('nextdefsym', p_ulong),
        ('irefsym', p_ulong),
        ('nrefsym', p_ulong),
        ('ilocalsym', p_ulong),
        ('nlocalsym', p_ulong),
        ('iextrel', p_ulong),
        ('nextrel', p_ulong),
        ('iinit_iterm', p_ulong),
        ('ninit_nterm', p_ulong),
        ('objc_module_info_size', p_ulong),
        ('objc_module_info_addr', p_ulonglong),
    )

class dylib_reference(Structure):
    _fields_ = (
        # XXX - ick, fix
        ('isym_flags', p_ulong),
        #('isym', p_ubyte * 3),
        #('flags', p_ubyte),
    )

class twolevel_hints_command(Structure):
    _fields_ = (
        ('offset', p_ulong),
        ('nhints', p_ulong),
    )

class twolevel_hint(Structure):
    _fields_ = (
      # XXX - ick, fix
      ('isub_image_itoc', p_ulong),
      #('isub_image', p_ubyte),
      #('itoc', p_ubyte * 3),
  )

class prebind_cksum_command(Structure):
    _fields_ = (
        ('cksum', p_ulong),
    )

class symseg_command(Structure):
    _fields_ = (
        ('offset', p_ulong),
        ('size', p_ulong),
    )

class ident_command(Structure):
    _fields_ = (
    )

class fvmfile_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('header_addr', p_ulong),
    )

class uuid_command (Structure):
    _fields_ = (
        ('uuid', p_str16),
    )

class rpath_command (Structure):
    _fields_ = (
        ('path', lc_str),
    )

class linkedit_data_command (Structure):
    _fields_ = (
        ('dataoff',   p_ulong),
        ('datassize', p_ulong),
    )


LC_REGISTRY = {
    LC_SEGMENT:         segment_command,
    LC_IDFVMLIB:        fvmlib_command,
    LC_LOADFVMLIB:      fvmlib_command,
    LC_ID_DYLIB:        dylib_command,
    LC_LOAD_DYLIB:      dylib_command,
    LC_LOAD_WEAK_DYLIB: dylib_command,
    LC_SUB_FRAMEWORK:   sub_framework_command,
    LC_SUB_CLIENT:      sub_client_command,
    LC_SUB_UMBRELLA:    sub_umbrella_command,
    LC_SUB_LIBRARY:     sub_library_command,
    LC_PREBOUND_DYLIB:  prebound_dylib_command,
    LC_ID_DYLINKER:     dylinker_command,
    LC_LOAD_DYLINKER:   dylinker_command,
    LC_THREAD:          thread_command,
    LC_UNIXTHREAD:      thread_command,
    LC_ROUTINES:        routines_command,
    LC_SYMTAB:          symtab_command,
    LC_DYSYMTAB:        dysymtab_command,
    LC_TWOLEVEL_HINTS:  twolevel_hints_command,
    LC_PREBIND_CKSUM:   prebind_cksum_command,
    LC_SYMSEG:          symseg_command,
    LC_IDENT:           ident_command,
    LC_FVMFILE:         fvmfile_command,
    LC_SEGMENT_64:      segment_command_64,
    LC_ROUTINES_64:     routines_command_64,
    LC_UUID:            uuid_command,
    LC_RPATH:           rpath_command,
    LC_CODE_SIGNATURE:  linkedit_data_command,
    LC_CODE_SEGMENT_SPLIT_INFO:  linkedit_data_command,
    LC_REEXPORT_DYLIB:  dylib_command,
}

class nlist(Structure):
    _fields_ = (
        ('n_un', p_long),
        ('n_type', p_ubyte),
        ('n_sect', p_ubyte),
        ('n_desc', p_short),
        ('n_value', p_ulong),
    )

N_STAB = 0xe0
N_PEXT = 0x10
N_TYPE = 0x0e
N_EXT = 0x01

N_UNDF = 0x0
N_ABS = 0x2
N_SECT = 0xe
N_PBUD = 0xc
N_INDR = 0xa

NO_SECT = 0
MAX_SECT = 255

REFERENCE_TYPE = 0xf
REFERENCE_FLAG_UNDEFINED_NON_LAZY = 0
REFERENCE_FLAG_UNDEFINED_LAZY = 1
REFERENCE_FLAG_DEFINED = 2
REFERENCE_FLAG_PRIVATE_DEFINED = 3
REFERENCE_FLAG_PRIVATE_UNDEFINED_NON_LAZY = 4
REFERENCE_FLAG_PRIVATE_UNDEFINED_LAZY = 5

REFERENCED_DYNAMICALLY = 0x0010

def GET_LIBRARY_ORDINAL(n_desc):
    return (((n_desc) >> 8) & 0xff)

def SET_LIBRARY_ORDINAL(n_desc, ordinal):
    return (((n_desc) & 0x00ff) | (((ordinal & 0xff) << 8)))

SELF_LIBRARY_ORDINAL = 0x0
MAX_LIBRARY_ORDINAL = 0xfd
DYNAMIC_LOOKUP_ORDINAL = 0xfe
EXECUTABLE_ORDINAL = 0xff

N_DESC_DISCARDED = 0x0020
N_WEAK_REF = 0x0040
N_WEAK_DEF = 0x0080

# /usr/include/mach-o/fat.h
FAT_MAGIC = 0xcafebabeL
class fat_header(Structure):
    _fields_ = (
        ('magic', p_ulong),
        ('nfat_arch', p_ulong),
    )

class fat_arch(Structure):
    _fields_ = (
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('offset', p_ulong),
        ('size', p_ulong),
        ('align', p_ulong),
    )
