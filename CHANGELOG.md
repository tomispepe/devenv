1.0.0-beta19
===============

* Added wrappers for magento, vhosts.sh and vcd to run inside default vagrant guest
* Fixed error reporting of vhosts.sh when it fails

1.0.0-beta18
===============

* Added list of available sites to the index file available at dev-web - resolves #17
* Added assertion for local /etc/hosts entry in vhosts.sh - resolves #36
* Added root CA signing certificate to Shared System Certificate trust list - resolves #58
* Refactored vhosts.sh. Highlights are as follows:
    * requires root privileges to run (will self-escalate if necessary)
    * removed the --reset flag and added --reset-config / --reset-certs
    * no longer cleans up after old sites without performing a reset
    * removed (now) unnecessary LSB code masking
    * generated configuration files are no longer shared via mount
* Moved bin scripts for use on guest into /usr/local/bin on guest
* Changed m2setup.sh to require --hostname flag when run
* Fixed for finalized ability to provision a vm completely offline - resolves #11
* Refactored provisioners to be single-file per role shell scripts
* Varnish is now running when the machine is provisioned with support for a .varnish.vcl file in site root (PR #59)

1.0.0-beta17
===============

* Fixed bug with sttdy input expectations in m2setup.sh
* Fixed incorrect use of shell redirection in bootstrap.sh
* Fixed issue with improper grep filter regex files (blank line matches anything)
* Fixed verbosity issue in rpm installation script
* Fixed version check in m2setup.sh to be compatible with PHP 7.0.x

1.0.0-beta16
===============

* Added FQDN to hosts file for each defined node (PR #57)
* Changed pre-configured value of php's max_input_vars setting (PR #56)

1.0.0-beta15
===============

* Updated method of rpm installation to:
    * elimnate perpetual failure after a failed offline provisioning
    * allow cached rpm definition files to update as needed
* Updated default hostname used by m2setup.sh to m2.demo
* Added --verbose and --urlpath options to m2setup.sh
* Changed installed composer version to 1.0.0-alpha11 due to continued instability issues on latest snapshot
* Updated n98-magerun installer to setup n98-magerun2 as mr2 in addition to existing version of tool
* Misc updates to support davidalger/cloud project
* Correct README info on m2.dev to match implementation

1.0.0-beta14
===============

* Added composer.json for using this as a library (vagrant-cloud support)
* Added install of varnish to web role in a (currently) inactive state
* Added support for Xdebug reports to link to PhpStorm file:line URLs
* Added support to m2setup.sh for generating / inputing administrator details for installs
* Added support to m2setup.sh for installing from enterprise meta-packages
* Added verbose flag to the bootstrap.sh script for use in calls to bootstrap_sh method (vagrant-cloud support)
* Added wget to rpm init routine; digital ocean images don't have it pre-installed (vagrant-cloud support)
* Added Zend OPCache to installed extension list
* Fixed AllowOverride directive failing to apply to DocumentRoot
* Moved npm setup to node role for global support of npm usage (vagrant-cloud support)
* Removed unused sites_dir env var from default list of constants passed through to bootstrap_sh

1.0.0-beta13
===============

* Added change-timeout.sh script for quickly increasing timeouts (issue #45, PR #49)
* Added PHP 7.0 support via a new alternate web70 vagrant machine
* Added support for SSL on web role (issue #34, PR #50)
* Updated m2setup.sh to use SSL on frontend and backend by default
* Changed xdebug.var_display_max_depth to default value of 3 (PR #48)

1.0.0-beta12
===============

* Added magento CLI tool shortcut to custom bin dir
* Added vagrant/bin to PATH for easy use of custom tooling
* Changed default session lifetime in php config (issue #47)
* Fixed bug where vhosts.sh failed restart httpd when run within virtual machine
* Fixed issue with sample data install with RC and develop trunk
* Removed temporary fix for issue with sample data running from pub doc root
* Renamed m2site.sh to m2setup.sh
* Updated m2setup.sh to support install from meta-packages
* Updated mreports alias to sort reports by count

1.0.0-beta11
===============

* Added compatibility with non-bash shells (kudos @colnpanic)
* Added copyright/license info to source files
* Added flag to specify branch on m2 install
* Documented resolution for most common issue causing mysqld start failure (issue #43)
* Fixed exit bug in m2dev.sh when run with invalid arguments
* Updated nginx sites config to allow any TLD
* Updated session storage workaround documentation
* Updated with quiter rpm mirror host resolution failure / retry messages on provisioning

1.0.0-beta10
===============

* Added documentation for virtual host configuration
* Added provisioner for grunt-cli on web role (issue #33)
* Added provisioner for man on node role
* Added provisioner for npm on web role (issue #33)
* Added quick-reference for virtual machines to README
* Added support for color ls output
* Added support to m2site.sh for installing sample data (see m2site.sh --help for details)
* Added support to m2site.sh for using alternate hostname (see m2site.sh --help for details)
* Fixed typo in nginx config
* Fixed warning in php provisioner
* Removed git status from shell prompt in virtual machine to improve prompt performance
* Removed use of symlinks for var directories in m2site.sh (issue #39)
* Updated version of Nginx for HTTP 1.1 transfer encoding support in proxy_pass (issue #37)

1.0.0-beta9
===============

* Added --reset flag to vhosts.sh (issue #35)
* Added some new git log aliases
* Added support for .demo and .local TLD in nginx configuration
* Fixed timezone used in virtual machines (issue #32)
* Updated mounts to consume fewer provisioners for binds and support future use of NFS4
* Updated PS1 to use __git_ps1 for status information

1.0.0-beta8
===============

* Added togglehidden alias to allow quickly flipping the visibility of hidden files in the Finder
* Fixed issue caused by alias.sh executing before git was installed in vm
* Implemented bootstrap.log file to record bootstrap.sh output and removed most -q flags from scripts
* Quieted vagrant output when bootstrap.sh runs
* Updated service calls to relay status messages to user and filter stderr output lines
* Updated virtual box machine directory via auto configuration

1.0.0-beta7
===============

* Introduced install.sh tool for CL machine setup
* Updated install.sh tool to support updating existing components

1.0.0-beta6
===============

* Added creation of /sites link to install.sh
* Added perl dependency to host for vhosts.sh script
* Added php56 to host general tooling installation
* Added vhosts.sh provisioner to always run on load
* Configured .my.cnf file setup to be automatic
* Configured /etc/hosts entries to be automatic
* Moved m2.dev setup into non-provisioning script
* Silenced output of service calls during provisioning

1.0.0-beta5
===============

* Fixed bug in order of setup in install.sh
* Fixed incorrect change reporting in install.sh

1.0.0-beta4
===============

* Added composer token instructions to setup info (issue #29)
* Updated install.sh script to bring env to complete working state
* Updated README

1.0.0-beta3
===============

* Added pre-configured machines for running alternate versions of PHP and MySql
* Moved vagrant home to /server/.vagrant and remove cwd relative dotfile path (issue #31)
* Updated PS1 and NFS exports in readme to be independent of where /server points

1.0.0-beta2
===============

* Added php-bcmath dependency needed for Magento 2 EE (issue #30)
* Fixed glitch in m2.dev where composer would hang waiting for user input (issue #29)
* Fixed issue occurring in odd case where vagrant sub-called itself
* Fixed issue with PS1 running under sh
* Misc framework updates
* Updated environment constants used in configuration
* Updated NFS exports setup on host machine to be automatic (issue #28)

1.0.0-beta1
===============

* Added auto mkdir calls for source path when mounting a bind file-system (issue #22)
* Added binds for walking bash history
* Added setup instructions to the README
* Added SoapClient dependency to php provisioner (issue #21)
* Added support for mysqld configuration extras (PR #19)
* Changed db privileges to use hostname of host vs hardcoded address
* Fixed broken package names in install tools
* Fixed bug causing vagrant failure when run from /server/vagrant
* Fixed bug failing all provisioners when using Virtual Box (PR #20)
* Fixed invalid presence check for vagrant command in vhosts.sh
* Fixed regression caused by relative links introduced in 1.0.0-beta0
* Removed php-code-fixer dependency
* Removed port forwards in favor of connecting directly to virtual machine
* Resolved issue with package installation order
* Updated ignore rules to properly ignore additional OS X special dirs
* Updated nginx proxy read timeout (issue #26, PR #27)

1.0.0-beta0
===============

* Added bind for /sites and /server/sites shortcuts for direct host -> guest path mapping (issue #1)
* Added execution of etc/profile.d/*.sh scripts on host machine (issue #10)
* Added provisioner for bash-completion package on node role (issue #3)
* Added provisioner to install n98-magerun on web role (issue #2)
* Adjusted NFS mounts for better stability
* Fixed issues with m2.dev provisioner failing and taking too long to run (issue #18)
* Fixed m2 setup on halt/destroy/up sequence
* Fixed Xdebug remote configuration
* Updated base box image to use new bento images
* Updated node provisioning order to have db node start first
* Updated persistent yum cache mount to bind to top-level cache location on guest (issue #8)
* Updated vhosts.sh to run on guest or host and auto-run during provisioning (issue #4)

1.0.0-alpha0
===============

* First tagged release used for alpha testing purposes
