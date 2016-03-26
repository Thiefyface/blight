from ctypes import *
from ctypes.util import find_library
from os.path import isfile
from os import access
from os import X_OK

'''
#include <sys/ptrace.h>
 
long ptrace (enum __ptrace_request request,
             pid_t pid,
             void *addr,
             void *data);
'''

MAX_PID = 32768
libc = CDLL(find_library('c'))
PTRACE = libc.ptrace

#Lifted straight from GDB source
def WIFEXITED(w): return (((w)&0377) == 0)
def WIFSIGNALED(w):  return (((w)&0377) != 0177 and ((w)&~0377) == 0) 
def WIFSTOPPED(w):  return (((w)&0377) == 0177)

#Executable file check
def exec_test(f): return (isfile(f) and access(f,X_OK))

#COLORS!!!
ATTN = '\033[96m'
PURP = '\033[95m'
GOOD = '\033[92m'
WARN = '\033[93m'
BAD = '\033[91m'
CLEAR = '\00'

#constants

PTRACE_TRACEME = 0
PTRACE_PEEKTEXT = 1
PTRACE_PEEKDATA = 2
PTRACE_PEEKUSR = 3
PTRACE_POKETEXT = 4
PTRACE_POKEDATA = 5
PTRACE_POKEUSR = 6
PTRACE_CONT = 7
PTRACE_KILL = 8
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_SYSCALL = 24

EFLAGS = [ 
       "CF", None, "PF", None, #0-3
       "AF", None, "ZF", "SF", #4-7
       "TF", "IF", "DF", "OF", #8-11
    ]
