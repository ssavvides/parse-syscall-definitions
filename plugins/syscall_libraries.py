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



def syscalls_per_library(libraries, syscall_definitions):
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

  <Exceptions>
    None
  
  <Side Effects>
    None

  <Returns>
    not_in_libraries:
      A list of the system calls not found in any of the examined libraries.
  """
  
  # a list to hold all system calls not contained in any of the examined
  # libraries.
  not_in_libraries = []

  for sd in syscall_definitions:
    contained = False
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

  syscalls_not_in_libraries = syscalls_per_library(libraries, syscall_definitions)

  for lib in libraries:
    print(lib)
    print()
    print()

  print("Syscalls not in any of the examined libraries (" + 
        str(len(syscalls_not_in_libraries)) + "):")
  print("----------------------------------------------------")
  for syscall_name in syscalls_not_in_libraries:
    print(syscall_name)



if __name__ == '__main__':
  main()