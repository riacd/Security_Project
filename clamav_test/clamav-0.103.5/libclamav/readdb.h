/*
 *  Copyright (C) 2013-2022 Cisco Systems, Inc. and/or its affiliates. All rights reserved.
 *  Copyright (C) 2007-2013 Sourcefire, Inc.
 *  Copyright (C) 2002-2007 Tomasz Kojm <tkojm@clamav.net>
 *
 *  Authors: Tomasz Kojm
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License version 2 as
 *  published by the Free Software Foundation.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
 */

#ifndef __READDB_H
#define __READDB_H

#if HAVE_CONFIG_H
#include "clamav-config.h"
#endif

#include "clamav.h"
#include "str.h"
#include "cvd.h"

#define MAX_LDB_SUBSIGS 64

struct cli_matcher;

/* NOTE: We don't include .info in CLI_DBEXT because they are only used for
 * one specific purpose - verifying the contents of database container files.
 * This list is geared towards file extensions of files that users can provide
 * to ClamAV directly. */
#ifdef HAVE_YARA
#define CLI_DBEXT(ext)                   \
    (                                    \
        cli_strbcasestr(ext, ".db") ||   \
        cli_strbcasestr(ext, ".hdb") ||  \
        cli_strbcasestr(ext, ".hdu") ||  \
        cli_strbcasestr(ext, ".fp") ||   \
        cli_strbcasestr(ext, ".mdb") ||  \
        cli_strbcasestr(ext, ".mdu") ||  \
        cli_strbcasestr(ext, ".hsb") ||  \
        cli_strbcasestr(ext, ".hsu") ||  \
        cli_strbcasestr(ext, ".sfp") ||  \
        cli_strbcasestr(ext, ".msb") ||  \
        cli_strbcasestr(ext, ".msu") ||  \
        cli_strbcasestr(ext, ".ndb") ||  \
        cli_strbcasestr(ext, ".ndu") ||  \
        cli_strbcasestr(ext, ".ldb") ||  \
        cli_strbcasestr(ext, ".ldu") ||  \
        cli_strbcasestr(ext, ".sdb") ||  \
        cli_strbcasestr(ext, ".zmd") ||  \
        cli_strbcasestr(ext, ".rmd") ||  \
        cli_strbcasestr(ext, ".pdb") ||  \
        cli_strbcasestr(ext, ".tdb") ||  \
        cli_strbcasestr(ext, ".gdb") ||  \
        cli_strbcasestr(ext, ".wdb") ||  \
        cli_strbcasestr(ext, ".cbc") ||  \
        cli_strbcasestr(ext, ".ftm") ||  \
        cli_strbcasestr(ext, ".cfg") ||  \
        cli_strbcasestr(ext, ".cvd") ||  \
        cli_strbcasestr(ext, ".cld") ||  \
        cli_strbcasestr(ext, ".cud") ||  \
        cli_strbcasestr(ext, ".cdb") ||  \
        cli_strbcasestr(ext, ".cat") ||  \
        cli_strbcasestr(ext, ".crb") ||  \
        cli_strbcasestr(ext, ".idb") ||  \
        cli_strbcasestr(ext, ".ioc") ||  \
        cli_strbcasestr(ext, ".yar") ||  \
        cli_strbcasestr(ext, ".yara") || \
        cli_strbcasestr(ext, ".pwdb") || \
        cli_strbcasestr(ext, ".ign") ||  \
        cli_strbcasestr(ext, ".ign2") || \
        cli_strbcasestr(ext, ".imp"))
#else
 //Injected :new tdb options
#define CLI_DBEXT(ext)                   \
    (                                    \
        cli_strbcasestr(ext, ".tdb") ||  \
        cli_strbcasestr(ext, ".db") ||   \
        cli_strbcasestr(ext, ".hdb") ||  \
        cli_strbcasestr(ext, ".hdu") ||  \
        cli_strbcasestr(ext, ".fp") ||   \
        cli_strbcasestr(ext, ".mdb") ||  \
        cli_strbcasestr(ext, ".mdu") ||  \
        cli_strbcasestr(ext, ".hsb") ||  \
        cli_strbcasestr(ext, ".hsu") ||  \
        cli_strbcasestr(ext, ".sfp") ||  \
        cli_strbcasestr(ext, ".msb") ||  \
        cli_strbcasestr(ext, ".msu") ||  \
        cli_strbcasestr(ext, ".ndb") ||  \
        cli_strbcasestr(ext, ".ndu") ||  \
        cli_strbcasestr(ext, ".ldb") ||  \
        cli_strbcasestr(ext, ".ldu") ||  \
        cli_strbcasestr(ext, ".sdb") ||  \
        cli_strbcasestr(ext, ".zmd") ||  \
        cli_strbcasestr(ext, ".rmd") ||  \
        cli_strbcasestr(ext, ".pdb") ||  \
        cli_strbcasestr(ext, ".gdb") ||  \
        cli_strbcasestr(ext, ".wdb") ||  \
        cli_strbcasestr(ext, ".cbc") ||  \
        cli_strbcasestr(ext, ".ftm") ||  \
        cli_strbcasestr(ext, ".cfg") ||  \
        cli_strbcasestr(ext, ".cvd") ||  \
        cli_strbcasestr(ext, ".cld") ||  \
        cli_strbcasestr(ext, ".cud") ||  \
        cli_strbcasestr(ext, ".cdb") ||  \
        cli_strbcasestr(ext, ".cat") ||  \
        cli_strbcasestr(ext, ".crb") ||  \
        cli_strbcasestr(ext, ".idb") ||  \
        cli_strbcasestr(ext, ".ioc") ||  \
        cli_strbcasestr(ext, ".pwdb") || \
        cli_strbcasestr(ext, ".ign") ||  \
        cli_strbcasestr(ext, ".ign2") || \
        cli_strbcasestr(ext, ".imp"))
#endif

char *cli_virname(const char *virname, unsigned int official);

cl_error_t cli_sigopts_handler(struct cli_matcher *root, const char *virname, const char *hexsig, uint8_t sigopts, uint16_t rtype, uint16_t type, const char *offset, uint8_t target, const uint32_t *lsigid, unsigned int options);

cl_error_t cli_parse_add(struct cli_matcher *root, const char *virname, const char *hexsig, uint8_t sigopts, uint16_t rtype, uint16_t type, const char *offset, uint8_t target, const uint32_t *lsigid, unsigned int options);

cl_error_t cli_load(const char *filename, struct cl_engine *engine, unsigned int *signo, unsigned int options, struct cli_dbio *dbio);

char *cli_dbgets(char *buff, unsigned int size, FILE *fs, struct cli_dbio *dbio);

cl_error_t cli_initroots(struct cl_engine *engine, unsigned int options);

#ifdef HAVE_YARA
cl_error_t cli_yara_init(struct cl_engine *engine);

void cli_yara_free(struct cl_engine *engine);
#endif

#endif
