#
#  Copyright (C) 2013-2022 Cisco Systems, Inc. and/or its affiliates. All rights reserved.
#  Copyright (C) 2007-2013 Sourcefire, Inc.
#  Copyright (C) 2003-2007 Tomasz Kojm <tkojm@clamav.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

if HAVE_MILTER

sbin_PROGRAMS = clamav-milter

clamav_milter_SOURCES = \
    whitelist.c \
    whitelist.h \
    connpool.c \
    connpool.h \
    netcode.c \
    netcode.h \
    clamfi.c \
    clamfi.h \
    clamav-milter.c
man_MANS = $(top_builddir)/docs/man/clamav-milter.8
AM_CFLAGS=@WERR_CFLAGS_MILTER@

endif

LIBS = $(top_builddir)/libclamav/libclamav.la $(top_builddir)/shared/libshared.la @CLAMAV_MILTER_LIBS@ @THREAD_LIBS@
AM_CPPFLAGS = -I$(top_srcdir)/clamd -I$(top_srcdir)/libclamav -I$(top_builddir)/libclamav -I$(top_srcdir)/libclamunrar_iface -I$(top_srcdir)/shared -I$(top_srcdir) @SSL_CPPFLAGS@ @JSON_CPPFLAGS@ @PCRE_CPPFLAGS@
CLEANFILES=*.gcda *.gcno
