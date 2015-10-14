parse-syscall-definitions
=========================
Parse the definitions of all system calls from their man pages.

First read the manual page for syscalls (man 2 syscalls) and parse the names
of all system calls available in the system. Then for each system call read
its man page and get its definition.

Tested Under:
-------------
Ubuntu Linux and Gentoo Linux


The SyscallManual module
============================
Parses the definition of a system call into a SyscallDefinition object.

Read the man page of a system call and extract its definition. If a definition
with the exact system call name is not found then pick one with a similar name
if such a definition exists. If there are multiple definitions for the same
system call then choose the one with the most arguments.

Examples:

man 2 chown32 gives the same page as man chown so for chown32 definition is:
  int chown(const char *path, uid_t owner, gid_t group)

from open man page:
  int open(const char *pathname, int flags);
  int open(const char *pathname, int flags, mode_t mode); <-- pick this one



The SyscallDefinition Class
---------------------------
<Purpose>
  A SyscallDefinition is made up of the system call name and its definition 
  parsed from its man page.

  The name of the system call and the definition name are not necessarily the
  same, but most of the times are. For example the name of the system call can
  be 'chown32' and the name of its definition 'chown'.

<Attributes>
  name:
    The name of the system call
  
  type:
    The type of the definition. Can be one of NO_MAN_ENTRY, NOT_FOUND, 
    UNIMPLEMENTED, FOUND
  
  definition:
    Holds the definition object if the type is FOUND. Otherwise definition is 
    set to None.


The Definition Class
--------------------
<Purpose>
  A Definition object is made up of three parts. The definition return type,
  the definition name and the definition parameters.
<Attributes>
  ret_type:
    The return type of the syscall definition.

  name:
    The name of the definition. This is not always the same as the syscall 
    name.

  parameters:
    A list of Parameter objects each describing a parameter of the definition.



The Parameter Class
-------------------
<Purpose>
  This object is used to describe a parameter of system call definitions.

<Attributes>
  self.type
  self.name
  self.ellipsis
  self.enum
  self.array
  self.const
  self.union
  self.struct
  self.pointer
  self.unsigned
  self.function
  self.const_pointer

The passed parameter_string is made up from the parameter type and a
parameter name. We need both the type and the name along with some other
derived information, to fully describe the parameter. 

Example:
Full definition: int open(const char *pathname, int flags);
Example parameter string: const char *pathname

In this example the name of the parameter is pathname and the type of the
parameter is char. The type should be further described as const and
pointer.
