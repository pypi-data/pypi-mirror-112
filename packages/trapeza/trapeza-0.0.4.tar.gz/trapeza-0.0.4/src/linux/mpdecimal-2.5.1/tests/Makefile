

SRCDIR = ../libmpdec

ENABLE_SHARED = yes

LIBSTATIC = libmpdec.a
LIBSHARED = libmpdec.so.2.5.1
LINK_STATIC = 
LINK_DYNAMIC = 
LINK_SHLIBS = -lmpdec

CC = gcc
AR = ar

MPD_GNU99 = 

CONFIGURE_CFLAGS = -Wall -Wextra -Wno-unknown-pragmas -std=c99 -pedantic -DNDEBUG -O2 
MPD_CFLAGS = $(strip $(filter-out $(CFLAGS),$(CONFIGURE_CFLAGS)) $(CFLAGS) $(MPD_GNU99))

LINK_LIBSTATIC = $(strip $(LINK_STATIC) $(SRCDIR)/$(LIBSTATIC) $(LINK_DYNAMIC))
LINK_LIBSHARED = $(strip $(LINK_SHLIBS))

ifeq ($(ENABLE_SHARED), yes)
default: runtest runtest_shared
else
default: runtest
endif


# Objects.
test.o:\
Makefile test.c $(SRCDIR)/mpdecimal.h test.h
	$(CC) -I$(SRCDIR) $(MPD_CFLAGS) -c test.c

runtest.o:\
Makefile runtest.c $(SRCDIR)/mpdecimal.h test.h vctest.h
	$(CC) -I$(SRCDIR) $(MPD_CFLAGS) -c runtest.c

# Short test.
runtest:\
Makefile runtest.o test.o $(SRCDIR)/$(LIBSTATIC)
	$(CC) -I$(SRCDIR) $(MPD_CFLAGS) -o runtest runtest.o test.o $(LINK_LIBSTATIC) -lm

runtest_shared:\
Makefile runtest.o test.o $(SRCDIR)/$(LIBSHARED)
	$(CC) -I$(SRCDIR) $(MPD_CFLAGS) -o runtest_shared runtest.o test.o -L$(SRCDIR) $(LINK_LIBSHARED) -lm


FORCE:

clean: FORCE
	rm -f *.o *.gch *.gcda *.gcno *.gcov *.dyn *.dpi *.lock
	rm -f runtest runtest_shared

distclean: FORCE
	$(MAKE) clean
	rm -rf Makefile dectest.zip testdata


