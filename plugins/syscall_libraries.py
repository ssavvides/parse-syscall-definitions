"""
<Program Name>
  syscall_definition.py

<Started>
  July 2013

<Author>
  Savvas Savvides <ssavvide@purdue.edu>

<Purpose>
  The program asks for a pickle file containing a set of system call 
  definitions. Then the program examines a set of python libraries and checks
  whether these libraries contain functions corresponding to these system calls.

  An order of the libraries can be optionally set. If the order is not set, then
  each library will be examined individually for whether it contains these
  system calls. This means that a system call can appear in more than one
  library. If the order is set, then the libraries will be examined in that
  order, and each system call will appear only once, in the library first met.

"""

import os
import sys
import pickle
import socket

import ctypes
import ctypes.util

import syscall_definition

libc_name = ctypes.util.find_library('c')
libc = ctypes.CDLL(libc_name)


class SyscallLibrary:
  """
  This class is used to hold the names of the system calls contained within a
  library. Each object contains the name of the library, a pointer to the 
  library and a list of the contained system calls.
  """

  def __init__(self, n, m):
    self.name = n
    self.module = m
    self.syscalls_contained = []

  
  def __repr__(self):
    title = "Functions in " + self.name + "(" + \
            str(len(self.syscalls_contained)) + ")"
    
    title_line = "-" * len(title)

    list_of_names = ""
    for syscall_name in self.syscalls_contained:
      list_of_names += syscall_name + "\n"

    return title + "\n" + title_line + "\n" + list_of_names



def syscalls_per_library(libraries, syscall_definitions, order=None):
  """
  <Purpose>
    Given a set of libraries and a set of system calls, examine which system
    call is contained in which library.

  <Arguments>
    libraries:
      A list of SyscallLibrary objects to examine whether they contain system 
      call function.
    syscall_definitions:
      The set of system calls to examine.
    order:
      An optional list of library names that specifies the order in which to
      examine the libraries, and hence each system call name appears only once,
      in the first library it is met.

  <Exceptions>
    None
  
  <Side Effects>
    None

  <Returns>
    not_in_libraries:
      A list of the system calls not found in any of the examined libraries.
  """
  
  # remove libraries not contained in the order.
  if order:
    index = 0
    while index < len(libraries):
      if libraries[index].name not in order:
        libraries.pop(index)
      else:
        index += 1

  # a list to hold all system calls not contained in any of the examined
  # libraries.
  not_in_libraries = []
  
  for sd in syscall_definitions:
    contained = False
    if order:
      # if a library order was given, examine libraries in that order and
      # include each system call only once, in the first library found.
      lib = None
      for libname in order:
        for l in libraries:
          if l.name == libname:
            lib = l
            break

        if lib == None:
          raise Exception("Library " + libname + " not found.")

        if(getattr(lib.module, sd.name, False)):
          lib.syscalls_contained.append(sd.name)
          contained = True
          break

    else:
      for lib in libraries:
        if(getattr(lib.module, sd.name, False)):
          lib.syscalls_contained.append(sd.name)
          contained = True
      
    if not contained:
      not_in_libraries.append(sd.name)

  return not_in_libraries



def main():
  # need exactly one argument which is the pickle file from which to get the
  # syscall definitions.
  if len(sys.argv) != 2:
    raise Exception("Please give the name of the pickle file from which to " + 
                    "read syscall definitions.")

  # get the syscall definitions from the pickle file
  pickle_file = open(sys.argv[1], 'rb')
  syscall_definitions = pickle.load(pickle_file)
  
  sock_obj = socket.socket()

  # the libraries we want to examine for whether they contain a function
  # corresponding to a system call.
  libraries = [
    SyscallLibrary("os", os), 
    SyscallLibrary("sys", sys), 
    SyscallLibrary("libc", libc), 
    SyscallLibrary("socket", socket), 
    SyscallLibrary("sock_obj", sock_obj)
  ]
  
  # the order in which the libraries will be examined for whether they contain a 
  # system call function.
  # order = None
  order = ["libc", "os", "socket", "sock_obj", "sys"]
  
  syscalls_not_in_libraries = syscalls_per_library(libraries, syscall_definitions, order)

  # print the system calls per library.
  for lib in sorted(libraries, key=lambda x: len(x.syscalls_contained), reverse=True):
    print(lib)
    print()
    print()

  # print the system calls not identified in any of the examined libraries.
  print("Syscalls not in any of the examined libraries (" + 
        str(len(syscalls_not_in_libraries)) + "):")
  print("----------------------------------------------------")
  for syscall_name in syscalls_not_in_libraries:
    print(syscall_name)



if __name__ == '__main__':
  main()