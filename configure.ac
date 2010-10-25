dnl                                                -*- Autoconf -*-
dnl  Process this file with autoconf to produce a configure script.

dnl AC_PREREQ(2.59)
AC_INIT(cmip5-cmor-tables, 1.2.1, doutriaux1@llnl.gov)

GIT_TAG=`./get_git_version.sh`

AC_CANONICAL_TARGET

TABLES_VERSION=${PACKAGE_VERSION}" (commit: ${GIT_TAG})"

AC_PREFIX_DEFAULT([/usr/local])
AC_CONFIG_FILES([Makefile])

AC_OUTPUT

AC_MSG_NOTICE([CMIP5 CMOR Table version: ${TABLES_VERSION} installation path configured to: ${prefix}/share/cmor])
