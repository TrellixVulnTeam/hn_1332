#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# WordPress site management
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import re
from hypernova.libraries.siteconfig import SiteConfigBase, SiteProvisionerBase
from os.path import join

class SiteConfig(SiteConfigBase):
    """
    WordPress site configuration.

    This file represents a standard wp-config.php file. Its __str__() method
    converts into such.

    When making changes to this file, be sure to carefully examine the
    appropriate documentation before hand to ensure you fully understand the
    effects of your changes! This is usually a good place to start research:

        http://codex.wordpress.org/Editing_wp-config.php
    """

    # Support DB character sets; UTF-8 only for now
    DB_CHARSETS = [
        'utf8'
    ]

    # Database credentials
    db_host        = ''
    db_username    = ''
    db_password    = ''
    db_name        = ''
    db_prefix      = ''
    db_charset     = ''
    db_auto_repair = False

    # Hash key/salt values
    #
    # I doubt anybody fully understands what all of these control, but they
    # should all be random for security reasons.
    key_auth         = ''
    key_secure_auth  = ''
    key_logged_in    = ''
    key_nonce        = ''
    salt_auth        = ''
    salt_secure_auth = ''
    salt_logged_in   = ''
    salt_nonce       = ''

    # Site location details
    site_url      = ''
    site_home     = ''

    # Authentication/session options
    cookie_domain       = ''
    cookie_path         = ''
    site_cookie_path    = ''
    admin_cookie_path   = ''
    plugin_cookie_path  = ''

    # Content directory location
    content_dir = ''
    content_url = ''

    # Content (stylesheets, JavaScript, etc) editing
    content_enable_modifications = True

    # Explosive options that should never, ever, ever (in your wildest dreams)
    # be changed
    template_path   = ''
    stylesheet_path = ''

    # Plugin directory location
    #
    # The plugin_url value has to be set in two places for some older plugins.
    # We set PLUGINDIR *and* WP_PLUGIN_DIR to ensure no ill effects.
    plugin_dir = ''
    plugin_url = ''

    # Post/page revision control
    #
    # To limit the number of revisions that can be stored, you can change the
    # value of revisions_max_stored to any integer value above zero. Setting it
    # to true implies infinity. A value of false completely disables revisions.
    # To disable compacting ("trash emptying"), set
    # revisions_compact to zero.
    revisions_autosave_interval = 160 # (seconds)
    revisions_max_stored        = False
    revisions_compact           = 30 # (days)

    # Multi-site installation?
    #
    # This is best left false (the default) for most installations.
    is_multisite = False

    # Debugging configuration
    #
    # The server option, when true, displays error messages and warnings
    # generated by WordPress and its plugins. The client option does the same,
    # but for the client side code (JavaScript).
    debug_server         = False
    debug_server_display = False
    debug_server_log     = False
    debug_db             = False
    debug_client         = False

    # Optimisations
    concatenate_admin_js = True
    cache                = True
    cron_enable          = True
    cron_alternate       = False

    # Integration options
    #
    # Setting these values to None will cause them to be omitted, forcing the
    # defaults.
    integration_user_table     = False
    integration_usermeta_table = False

    # Internationalisation/localisation
    lang     = ''
    lang_dir = ''

    # Filesystem permission options
    chmod_dir  = 0o755
    chmod_file = 0o777

    # Upgrade configuration
    #
    # We should research effectively disabling this for specified sites, so as
    # to prevent upgrades breaking things before plugins have been updated. For
    # now, these options are best left set to false.
    #
    # When working with larger sites, the upgrade_global_db_tables functionality
    # should *definitely* be disabled to prevent breaking production sites. A
    # better approach than applying these major, potentially slow, upgrades via
    # PHP would be to perform the upgrade manually through MySQL's batch
    # processing, then redeploy the site's files and upgraded database when
    # complete.
    upgrade_method           = 'ftpsockets'
    upgrade_global_db_tables = True
    ftp_host                 = ''
    ftp_ssl                  = False
    ftp_base                 = ''
    ftp_content_dir          = ''
    ftp_plugin_dir           = ''
    ftp_key_pub              = ''
    ftp_key_priv             = ''
    ftp_username             = ''
    ftp_password             = ''

    __templ_option = "define('%s', %s);"
    __file_pre = """<?php
/*
 * Generated by HyperNova (hypernova.libraries.siteconfig.wordpress)
 *
 * This file was automatically generated and any modifications made to it will
 * likely be overwritten by automated maintenance. For assistance, contact our
 * support department.
 */
"""
    __file_post = """
if (defined('TABLE_PREFIX'))
    $table_prefix = TABLE_PREFIX;
"""

    __mapping = {
        'db_host':        'DB_HOST',
        'db_username':    'DB_USER',
        'db_password':    'DB_PASSWORD',
        'db_name':        'DB_NAME',
        'db_prefix':      'DB_PREFIX',
        'db_charset':     'DB_CHARSET',
        'db_auto_repair': 'WP_ALLOW_REPAIR',

        'key_auth':         'AUTH_KEY',
        'key_secure_auth':  'SECURE_AUTH_KEY',
        'key_logged_in':    'LOGGED_IN_KEY',
        'key_nonce':        'NONCE_KEY',
        'salt_auth':        'AUTH_SALT',
        'salt_secure_auth': 'SECURE_AUTH_SALT',
        'salt_logged_in':   'LOGGED_IN_SALT',
        'salt_nonce':       'NONCE_SALT',

        'site_url':  'WP_SITEURL',
        'site_home': 'WP_HOME',

        'cookie_domain':      'COOKIE_DOMAIN',
        'cookie_path':        'COOKIEPATH',
        'site_cookie_path':   'SITECOOKIEPATH',
        'admin_cookie_path':  'ADMIN_COOKIE_PATH',
        'plugin_cookie_path': 'PLUGINS_COOKIE_PATH',

        'content_dir': 'WP_CONTENT_DIR',
        'content_url': 'WP_CONTENT_URL',

        'content_enable_modifications': 'DISALLOW_FILE_MODS',

        'template_path':   'TEMPLATEPATH',
        'stylesheet_path': 'STYLESHEETPATH',

        'plugin_dir': 'WP_PLUGIN_DIR',
        'plugin_url': 'WP_PLUGIN_URL',

        'revisions_autosave_interval': 'AUTOSAVE_INTERVAL',
        'revisions_max_stored':        'WP_POST_REVISIONS',
        'revisions_compact':           'EMPTY_TRASH_DAYS',

        'debug_server':         'WP_DEBUG',
        'debug_server_display': 'WP_DEBUG_DISPLAY',
        'debug_server_log':     'WP_DEBUG_LOG',
        'debug_db':             'SAVEQUERIES',
        'debug_client':         'SCRIPT_DEBUG',

        'concatenate_admin_js': 'CONCATENATE_SCRIPTS',
        'cache':                'WP_CACHE',
        'cron_enable':          'DISABLE_WP_CRON',
        'cron_alternate':       'ALTERNATE_WP_CRON',

        'integration_user_table':     'CUSTOM_USER_TABLE',
        'integration_usermeta_table': 'CUSTOM_USER_META_TABLE',

        'lang':     'WP_LANG',
        'lang_dir': 'WP_LANG_DIR',

        'chmod_dir':  'FS_CHMOD_DIR',
        'chmod_file': 'FS_CHMOD_FILE',

        'upgrade_method':           'FS_METHOD',
        'upgrade_global_db_tables': 'DO_NOT_UPGRADE_GLOBAL_TABLES',
        'ftp_host':                 'FTP_HOST',
        'ftp_ssl':                  'FTP_SSL',
        'ftp_base':                 'FTP_BASE',
        'ftp_content_dir':          'FTP_CONTENT_DIR',
        'ftp_plugin_dir':           'FTP_PLUGIN_DIR',
        'ftp_key_pub':              'FTP_PUBKEY',
        'ftp_key_priv':             'FTP_PRIVKEY',
        'ftp_username':             'FTP_USER',
        'ftp_password':             'FTP_PASS',
    }

    # Booleans that actually make sense
    __bools = [
        'db_auto_repair',
        'debug_server',
        'debug_server_display',
        'debug_server_log',
        'debug_db',
        'debug_client',
        'concatenate_admin_js',
        'cache',
        'cron_alternative',
    ]

    # Booleans that start with disable/don't
    __reverse_bools = [
        'content_enable_modifications',
        'cron_enable',
        'upgrade_global_db_tables',
    ]

    __ints = [

    ]

    def __php_boolean(self, value):
        """
        Format a Python boolean into a PHP one.
        """

        if value:
            return 'true'

        return 'false'

    def __php_str(self, value):
        """
        Format a Python string as a PHP one.
        """

        return '\'' + re.sub(r'[\\\']', r'\\\\\'', value) + '\''

    def __init__(self):
        """
        Initialise defaults.
        """

    def __str__(self):
        """
        Return a string representation.

        Assemble a configuration file from the options defined within the
        object.
        """

        options = []
        for abstract, actual in self.__mapping.items():
            value = getattr(self, abstract)

            if abstract in self.__bools:
                value = self.__php_boolean(value)
            elif abstract in self.__reverse_bools:
                value = self.__php_boolean(not value)
            else:
                value = self.__php_str(str(value))

            options.append(self.__templ_option %(actual, value))

        return "\n".join([
            self.__file_pre,
            "\n".join(options),
            self.__file_post,
        ])

class SiteProvisioner(SiteProvisionerBase):
    """
    """

    module_name = 'wordpress'

    __source_url        = 'http://wordpress.org/wordpress-%s.tar.gz'
    __latest_source_url = 'http://wordpress.org/latest.tar.gz'

    source_url = None

    def __init__(self, *args):
        """
        Initialise the provisioner.

        If version is None (the default), the provisioner will fall back on
        using the latest available release of the application.
        """

        super().__init__(*args)

        try:
            self.source_url = self.__source_url %(self.parameters[1])
        except IndexError:
            self.source_url = self.__latest_source_url

    def _provision(self):

        # Download
        print('downloading')
        tarball = self.download_url(self.source_url, suffix='.tar.gz')

        # Extract
        print('extracting')
        source = self.extract_gzipped_tarball(tarball)

        # Create database
        print('creating db')
        db = self.create_mysql_database()

        # Install the files
        print('installing files')
        target = join(self.config['web']['base_dir'], self.parameters[0])
        self.move_tree(join(source, 'wordpress'), target)

        # Write web server configuration and reload daemon
        print('configuring http server')
        vhost = self.add_vhost()
        vhost.listen = 80
        vhost.server_names = [self.parameters[0]]
        vhost.indexes = ['index.php', 'index.html', 'index.htm']
        vhost.includes.append('enable_php')
        self.create_vhost(vhost)

        # Write application configuration
        print('configuring application')
        config = SiteConfig()
        with open(join(target, 'wp-config.php'), 'w') as f:
            f.write(str(config))

        # Migrate database
        print('migrating db')
