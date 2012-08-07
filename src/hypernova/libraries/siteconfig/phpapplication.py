#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# PHP application management (via Phing)
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.siteconfig import SiteConfigBase, SiteProvisionerBase

class SiteConfig(SiteConfigBase):
    """
    Generic PHP application configuration (via Phing).

    This object represents the configuration passed to the Phing build system
    maintained by TDM Open Source Software Services.

    For a list and detailed description of all of the properties available for
    customisation within this tool, see the following wiki page. Take note of
    which options are valid for which targets, since many are tied to specific
    operations:

        http://dev.ossservices.com/projects/oss-build-system/wiki
    """

    # HyperNova name -> OSS build system name mapping
    __mapping = {
        # Generic paths
        "build_dir":   "dir.abs.build",
        "data_dir":    "dir.abs.data",
        "project_dir": "dir.abs.project",
        "web_url":     "web.url",

        # Generic DB properties
        "db_host":     "db.host",
        "db_name":     "db.name",
        "db_type":     "db.type",
        "db_username": "db.user.name",
        "db_password": "db.user.password",

        # Migration-specific properties
        "db_migration_dir": "db.migrate.dir",
        "db_migration_ver": "db.migrate.target",

        # Package-specific properties
        "package_dat": "package.dat",
        "package_db":  "package.db",
        "package_src": "package.src",
    }

    # Property definition format.
    __templ_property_def = "%s=%s\n"

    # Absolute path to the build system directory.
    #
    # dir.abs.build
    build_dir = ""

    # Absolute path to the data directory.
    #
    # dir.abs.data
    data_dir = ""

    # Absolute project directory.
    #
    # dir.abs.project
    project_dir = ""

    # Database host.
    #
    # db.host
    db_host = ""

    # Database name.
    #
    # db.name
    db_name = ""

    # Database type.
    #
    # db.type
    db_type = ""

    # Database username.
    #
    # db.username
    db_username = ""

    # Database password.
    #
    # db.password
    db_password = ""

    # Absolute path to database migration directory.
    #
    # db.migrate.dir
    db_migration_dir = ""

    # DB migration target version.
    #
    # db.migrate.target
    db_migration_ver = ""

    # Archive to package the data directory in.
    #
    # package.dat
    package_dat = ""

    # Singular compressed file to package the database in.
    #
    # package.db
    package_db = ""

    # Archive or package to store the project source code in.
    package_src = ""

    # Complete URL to the application (without trailing /).
    #
    # web.url
    web_url = ""

    def __str__(self):
        prop_file = ""
        for hn, oss in self.__mapping:
            prop_file += self.__templ_property_def %(oss, getattr(self, hn))
        return prop_file


class SiteProvisioner(SiteProvisionerBase):
    """
    Generic PHP application provisioner.
    """

    module_name = 'phpapplication'

    source_url = None

    def __init__(self, *args):
        super().__init__(*args)
