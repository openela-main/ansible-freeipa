# Turn off automatic python byte compilation because these are Ansible
# roles and the files are transferred to the node and compiled there with
# the python version used in the node
%define __brp_python_bytecompile %{nil}

%global python %{__python3}

Summary: Roles and playbooks to deploy FreeIPA servers, replicas and clients
Name: ansible-freeipa
Version: 1.9.2
Release: 3%{?dist}
URL: https://github.com/freeipa/ansible-freeipa
License: GPLv3+
Source: https://github.com/freeipa/ansible-freeipa/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1: ansible-freeipa-1.9.2-paclient-Fix-allow_repair-with-removed-krb5.conf-an_RHBZ#2189235.patch
Patch2: ansible-freeipa-1.9.2-ipaclient-Defer-creating-the-final-krb5.conf-on-clients_RHBZ#2189238.patch
Patch3: ansible-freeipa-1.9.2-ipaclient-Defer-krb5-configuration-fix_RHBZ#2189238.patch
Patch4: ansible-freeipa-1.9.2-Fix-typo-in-ipapwpolicy.py_RHBZ#2218187.patch
BuildArch: noarch

%description
Ansible roles to install and uninstall FreeIPA servers, replicas and clients,
roles for backups and SmartCard configuration, modules for management and also
playbooks for all roles and modules.

Note: The Ansible playbooks and roles require a configured Ansible environment
where the Ansible nodes are reachable and are properly set up to have an IP
address and a working package manager.

Features

- Server, replica and client deployment
- Cluster deployments: Server, replicas and clients in one playbook
- One-time-password (OTP) support for client installation
- Repair mode for clients
- Backup and restore, also to and from controller
- Smartcard setup for servers and clients
- Modules for automembership rule management
- Modules for automount key management
- Modules for automount location management
- Modules for automount map management
- Modules for config management
- Modules for delegation management
- Modules for dns config management
- Modules for dns forwarder management
- Modules for dns record management
- Modules for dns zone management
- Modules for group management
- Modules for hbacrule management
- Modules for hbacsvc management
- Modules for hbacsvcgroup management
- Modules for host management
- Modules for hostgroup management
- Modules for idrange management
- Modules for location management
- Modules for netgroup management
- Modules for permission management
- Modules for privilege management
- Modules for pwpolicy management
- Modules for role management
- Modules for self service management
- Modules for server management
- Modules for service management
- Modules for service delegation rule management
- Modules for service delegation target management
- Modules for sudocmd management
- Modules for sudocmdgroup management
- Modules for sudorule management
- Modules for topology management
- Modules for trust management
- Modules for user management
- Modules for vault management

Supported FreeIPA Versions

FreeIPA versions 4.6 and up are supported by all roles.

The client role supports versions 4.4 and up, the server role is working with
versions 4.5 and up, the replica role is currently only working with versions
4.6 and up.

Supported Distributions

- RHEL/CentOS 7.4+
- Fedora 26+
- Ubuntu
- Debian 10+ (ipaclient only, no server or replica!)

Requirements

  Controller
  - Ansible version: 2.8+ (ansible-freeipa is an Ansible Collection)

  Node
  - Supported FreeIPA version (see above)
  - Supported distribution (needed for package installation only, see above)

Limitations

External signed CA is now supported. But the currently needed two step process
is an issue for the processing in a simple playbook.
Work is planned to have a new method to handle CSR for external signed CAs in
a separate step before starting the server installation.


%package tests
Summary: ansible-freeipa tests
Requires: %{name} = %{version}-%{release}

%description tests
ansible-freeipa tests.

Please have a look at %{_datadir}/ansible-freeipa/requirements-tests.txt
to get the needed requrements to run the tests.


%prep
%setup -q
# Do not create backup files with patches
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Fix python modules and module utils:
# - Remove shebang
# - Remove execute flag
for i in roles/ipa*/library/*.py roles/ipa*/module_utils/*.py plugins/*/*.py;
do
    sed -i '1{/\/usr\/bin\/python*/d;}' $i
    chmod a-x $i
done

for i in utils/*.py utils/new_module utils/changelog utils/ansible-doc-test;
do
    sed -i '{s@/usr/bin/python*@%{python}@}' $i
done


%build

%install
install -m 755 -d %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaserver %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaserver/README.md README-server.md
cp -rp roles/ipareplica %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipareplica/README.md README-replica.md
cp -rp roles/ipaclient %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipaclient/README.md README-client.md
cp -rp roles/ipabackup %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipabackup/README.md README-backup.md
cp -rp roles/ipasmartcard_server %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipasmartcard_server/README.md README-smartcard_server.md
cp -rp roles/ipasmartcard_client %{buildroot}%{_datadir}/ansible/roles/
cp -rp roles/ipasmartcard_client/README.md README-smartcard_client.md
install -m 755 -d %{buildroot}%{_datadir}/ansible/plugins/
cp -rp plugins/* %{buildroot}%{_datadir}/ansible/plugins/

install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa
cp requirements*.txt %{buildroot}%{_datadir}/ansible-freeipa/
cp -rp utils %{buildroot}%{_datadir}/ansible-freeipa/
install -m 755 -d %{buildroot}%{_datadir}/ansible-freeipa/tests
cp -rp tests %{buildroot}%{_datadir}/ansible-freeipa/

%files
%license COPYING
%{_datadir}/ansible/roles/ipaserver
%{_datadir}/ansible/roles/ipareplica
%{_datadir}/ansible/roles/ipaclient
%{_datadir}/ansible/roles/ipabackup
%{_datadir}/ansible/roles/ipasmartcard_server
%{_datadir}/ansible/roles/ipasmartcard_client
%{_datadir}/ansible/plugins/doc_fragments
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/modules
%doc README*.md
%doc playbooks
%{_datadir}/ansible-freeipa/requirements.txt
%{_datadir}/ansible-freeipa/requirements-dev.txt
%{_datadir}/ansible-freeipa/utils

%files tests
%{_datadir}/ansible-freeipa/tests
%{_datadir}/ansible-freeipa/requirements-tests.txt

%changelog
* Wed Jul  5 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-3
- Fix maxsequence handling in ipapwpolicy module
  Resolves: RHBZ#2218187

* Mon Apr 24 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-2
- ipaclient: Fix allow_repair with removed krb5.conf and DNS lookup
  Resolves: RHBZ#2189235
- ipaclient: Defer creating the final krb5.conf on clients
  Resolves: RHBZ#2189238

* Tue Jan 31 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-1
- Update to version 1.9.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.2
  Resolves: RHBZ#2125591
- ipabackup: Use ipabackup_item again in copy_backup_to_server
  Resolves: RHBZ#2165951

* Mon Jan 30 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.1-1
- Update to version 1.9.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.1
  Resolves: RHBZ#2125591
- pwpolicy: Allow clearing policy values
  Resolves: RHBZ#2150332
- Use netgroup_find instead of netgroup_show to workaround IPA bug
  Resolves: RHBZ#2144724

* Wed Dec  7 2022 Thomas Woerner <twoerner@redhat.com> - 1.9.0-1
- Update to version 1.9.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.0
  Related: RHBZ#2125591
- pwpolicy: Add support for password check and grace limit
  Resolves: RHBZ#2015288
- ipaconfig: Do not allow enable_sid set to False
  Resolves: RHBZ#2127447
- ipaclient: No kinit on controller for deployment using OTP
  Resolves: RHBZ#2127885
- ipaclient: Configure DNS resolver
  Resolves: RHBZ#2127894
- New netgroup management module
  Resolves: RHBZ#2127908
- sudorule: Add support for 'hostmask' parameter
  Resolves: RHBZ#2127912
- ipaconfig: Fix fail_json calls
  Resolves: RHBZ#2128460
- ipaconfig: Do not require enable_sid for add_sids or netbios_name
  Resolves: RHBZ#2134530
- ipaserver: Add missing idstart check
  Resolves: RHBZ#2132729

* Mon Sep 12 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.4-1
- Update to version 1.8.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.4
  Resolves: RHBZ#2125591
- 'ansible-doc' -l lists most idm modules as 'UNDOCUMENTED'
  Resolves: RHBZ#2121362
- ansible-freeipa Replica Install Setup DNS fails
  Resolves: RHBZ#2120415
- ipaconfig does not support SID and netbios attributes
  Resolves: RHBZ#2069174

* Tue Aug 16 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.3-1
- Update to version 1.8.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.3
  Related: RHBZ#2080321
- Fixes replica deployment issue for domains without SID support.
  Related: RHBZ#2110491

* Thu Jul 28 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.2-1
- Update to version 1.8.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.2
  Related: RHBZ#2080321
- SIDs are always generated for server and replica deployments
  Resolves: RHBZ#2110491
- Random Serial Numbers are not enabled by default any more
  Resolves: RHBZ#2110526
- Fixes comparison of bool values in IPA 4.9.10+ for ipadnsconfig
  Resolves: RHBZ#2110539

* Thu Jul  7 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.1-1
- Update to version 1.8.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.1
  Related: RHBZ#2080321
- ipa server deploys failing with latest IPA compose
  Resolves: RHBZ#2103928
- ipaserver_external_cert_files failes to copy with ansible 2.13
  Resolves: RHBZ#2104842

* Fri Jun 24 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.0-1
- idrange: Fix usage of dom_name when idrange doesn't exist.
  Resolves: RHBZ#2086993
- smartcard roles for ansible-freeipa
  Resolves: RHBZ#2076554

* Fri Apr 29 2022 Thomas Woerner <twoerner@redhat.com> - 1.7.0-1
- Update to version 1.7.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.7.0
  Resolves: RHBZ#2080321
- New idrange management module.
  Resolves: RHBZ#1921545
- Not able to update empty descriptions in automount maps.a
  Resolves: RHBZ#2048552
- New servicedelegationrule management module.
  Resolves: RHBZ#2069170
- New servicedelegationtarget management module.
  Resolves: RHBZ#2069172
- Add support for managing idoverrideusers in ipagroup.
  Resolves: RHBZ#2069173

* Thu Jan 27 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.3-1
- Update to version 1.6.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.3
  Related: RHBZ#2010621

* Wed Jan 26 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.2-1
- Update to version 1.6.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.2
  Related: RHBZ#2010621

* Fri Jan 21 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.1-1
- Update to version 1.6.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.0
  Related: RHBZ#2010621
- Add module to manage automount maps
  Resolves: RHBZ#2040462
- Add module to manage automount keys
  Resolves: RHBZ#2040464
- Client deploy failing with ipaadmin keytab and OTP due to latest ansible
  version
  Resolves: RHBZ#2041753

* Wed Dec 29 2021 Thomas Woerner <twoerner@redhat.com> - 1.5.3-1
- Update to version 1.5.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.0
  Related: RHBZ#2010621
- automember set default group/hostgroup is missing from the automember module
  Resolves: RHBZ#1999912
- automember remove default group/hostgroup is missing from the automember
  module
  Resolves: RHBZ#1999913
- automember rebuild is missing from the automember module
  Resolves: RHBZ#1999915
- automember remove orphans group/hostgroup is missing from the automember
  module
  Resolves: RHBZ#1999916
- Not able to update existing automember rule description
  Resolves: RHBZ#2021393

* Tue Oct  5 2021 Thomas Woerner <twoerner@redhat.com> - 0.4.0-1
- Update to version 0.4.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.4.0
  Resolves: RHBZ#2010621
- Add ability to run modules remotely
  Resolves: RHBZ#1918025
- New management module ipaautomountlocation
  Resolves: RHBZ#2010639

* Tue Jul 13 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.8-1
- Update to version 0.3.8
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.8
  Related: RHBZ#1959875
- automember: Verify condition keys
  Related: RHBZ#1976926

* Tue Jul 13 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.7-1
- Update to version 0.3.7
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.7
  Related: RHBZ#1959875
- automember: Fix action to be automember or member, not service
  Resolves: RRBZ#1976923
- automember: Fix result["failed"] issues with conditions
  Resolves: RRBZ#1976926

* Wed Jun  9 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-3
- Apply fix for ipabackup: Use module to get IPA_BACKUP_DIR from ipaplatform
  Related: RRBZ#1969847

* Wed Jun  9 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-2
- ipabackup: Use module to get IPA_BACKUP_DIR from ipaplatform
  Resolves: RRBZ#1969847

* Mon Jun  7 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-1
- Update to version 0.3.6
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.6
  Resolves: RHBZ#1959875
- ansible-freeipa-tests not in the compose
  Resolves: RHBZ#1936869
- Remove unsupported parameter for (ipapermission) module: perm_rights from
  permission-present.yml
  Resolves: RHBZ#1921654
- Sample playbook included for selfservice module is incorrect
  Resolves: RHBZ#1922060
- ipa-client-install failing with error code 7(keytab: /usr/sbin/ipa-rmkeytab
  returned 7)
  Resolves: RHBZ#1935123
- New management module ipaserver
  Resolves: RHBZ#1966493
- New management module ipaautomember
  Resolves: RHBZ#1966496

* Mon Jan 18 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.2-1
- Update to version 0.3.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.2
  Related: RHBZ#1891826
- Not able to add additional privileges with existing privilege in role module
  Resolves: RHBZ#1893678
- Required error message while adding non-existing members in role handling
  Resolves: RHBZ#1893679
- Not able to add new members with existing members role handling
  Resolves: RHBZ#1893684
- service members are removed while updating other members in role handling
  Resolves: RHBZ#1893685
- after changing the vault type from standard to symmetric, Salt is missing
  Resolves: RHBZ#1880367
- After changing the vault type from symmetric to asymmetric, Salt is present
  in the asymmetric vault
  Resolves: RHBZ#1880377
- After changing the vault type from asymmetric to the standard vault, the
  Public key is present in the standard vault
  Resolves: RHBZ#1880378
- Not able to replace public-key-file to the public-key in asymmetric vault
  type
  Resolves: RHBZ#1880862
- ipauser module does not seem to support --check flag to ansible-playbook
  Resolves: RHBZ#1893675
- Not able to add additional attributes with existing attributes in permission
  handling
  Resolves: RHBZ#1893687
- Privilege variable is removed from permission handling
  Resolves: RHBZ#1893688

* Wed Dec  2 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.1-1
- Update to version 0.3.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.1
  Related: RHBZ#1891826
- ipabackup: Fix undefined vars for conditions in shell tasks without else
  Related: RHBZ#1894494

* Tue Dec  1 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-2
- Ship ipabackup role for backup and restore
  Related: RHBZ#1894494

* Thu Nov 26 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-1
- Update to version 0.3.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.0
  With tests sub package
  Resolves: RHBZ#1891826
- Support for firewalld zone in ipaserver and ipareplica roles 
  Resolves: RHBZ#1894488
- ipagroup: Add support for the IPA CLI option `posix`
  Resolves: RHBZ#1894493
- New ipabackup role for backup and restore
  Resolves: RHBZ#1894494
- New management module ipadelegation
  Resolves: RHBZ#1894496
- New management module ipalocation
  Resolves: RHBZ#1894497
- New management module ipaprivilege
  Resolves: RHBZ#1894498
- New management module ipapermission
  Resolves: RHBZ#1894499
- New management module iparole
  Resolves: RHBZ#1894500
- New management module ipaselfservice
  Resolves: RHBZ#1894501
- New management module ipatrust
  Resolves: RHBZ#1894502
- Fixed log of vault data return when retrieving to a file
  Resolves: RHBZ#1875378
- ipadnszone: Fix modification o SOA serial with other attributes
  Resolves: RHBZ#1876896
- Fix symmetric vault password change when using password_files
  Resolves: RHBZ#1879004
- ipadnsrecord: fix record modification behavior
  Resolves: RHBZ#1880409
  Resolves: RHBZ#1881452
- ipadnsrecord: fix record update when multiple records exist
  Resolves: RHBZ#1881436

* Tue Aug 18 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-6
- Allow to manage multiple dnszone entries
  Resolves: RHBZ#1845058
- Fixed error msgs on FreeIPABaseModule subclasses
  Resolves: RHBZ#1845051
- Fix `allow_create_keytab_host` in service module
  Resolves: RHBZ#1868020
- Modified return value for ipavault module
  Resolves: RHBZ#1867909
- Add support for option `name_from_ip` in ipadnszone module
  Resolves: RHBZ#1845056
- Fixe password behavior on Vault module
  Resolves: RHBZ#1839200

* Tue Jul 14 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-5
- ipareplica: Fix failure while deploying KRA
  Resolves: RHBZ#1855299

* Thu Jul 02 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-4
- ipa[server,replica]: Fix pkcs12 info regressions introduced with CA-less
  Resolves: RHBZ#1853284

* Wed Jul 01 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-3
- action_plugins/ipaclient_get_otp: Discovered python needed in task_vars
  Resolves: RHBZ#1852714

* Mon Jun 29 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-2
- Fixes service disable when service has no certificates attached
  Resolves: RHBZ#1836294
- Add suppport for changing password of symmetric vaults
  Resolves: RHBZ#1839197
- Fix forwardzone issues
  Resolves: RHBZ#1843826
  Resolves: RHBZ#1843828
  Resolves: RHBZ#1843829
  Resolves: RHBZ#1843830
  Resolves: RHBZ#1843831
- ipa[host]group: Fix membermanager unknow user issue
  Resolves: RHBZ#1848426
- ipa[user,host]: Fail on duplucate names in the users and hosts lists
  Resolves: RHBZ#1822683

* Mon Jun 15 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-1
- Update to version 0.1.12 bug fix only release
  Related: RHBZ#1818768

* Thu Jun 11 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.11-1
- Update to version 0.1.11
  Related: RHBZ#1818768

* Mon Apr 27 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.10-1
- Update to version 0.1.10:
  - ipaclient: Not delete keytab when ipaclient_on_master is true
  - New module to manage dns forwarder zones in ipa
  - Enhancements of sudorule module tests
  - Gracefully handle RuntimeError raised during parameter validation in
    fail_jso
  - ipareplica_prepare: Fix module DOCUMENTATION
  - ipa[server,replica,client]: setup_logging wrapper for
    standard_logging_setup
  - Created FreeIPABaseModule class to facilitate creation of new modules
  - New IPADNSZone module
  - Add admin password to the ipadnsconfig module tests
  - Added alias module arguments in dnszone module
  - Fixed a bug in AnsibleFreeIPAParams
  - utils/build-galaxy-release: Do not add release tag to version for galaxy
  - ipaserver docs: Calm down module linter
  - galaxy.yml: Add system tag
  - ipareplica_setup_kra: Remove unused ccache parameter
  - ipareplica_setup_krb: krb is assigned to but never used
  - utils/galaxy: Make galaxy scripts more generic
  - galaxyfy-playbook.py: Fixed script name
  Related: RHBZ#1818768

* Thu Feb 20 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.8-3
- ipahost: Do not fail on missing DNS or zone when no IP address given
  Resolves: RHBZ#1804838

* Fri Feb 14 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.8-2
- Updated RPM description for ansible-freeipa 0.1.8
  Related: RHBZ#1748986
- ipahost: Fix choices of auth_ind parameter, allow to reset parameter
  Resolves: RHBZ#1783992
- ipauser: Allow reset of userauthtype, do not depend on first,last for mod
  Resolves: RHBZ#1784474
- ipahost: Enhanced failure msg for member params used without member action
  Resolves: RHBZ#1783948
- Add missing attributes to ipasudorule
  Resolves: RHBZ#1788168
  Resolves: RHBZ#1788035
  Resolves: RHBZ#1788024
- ipapwpolicy: Use global_policy if name is not set
  Resolves: RHBZ#1797532
- ipahbacrule: Fix handing of members with action hbacrule
  Resolves: RHBZ#1787996
- ansible_freeipa_module: Fix comparison of bool parameters in compare_args_isa
  Resolves: RHBZ#1784514
- ipahost: Add support for several IP addresses and also to change them
  Resolves: RHBZ#1783979
  Resolves: RHBZ#1783976
- ipahost: Fail on action member for new hosts, fix dnsrecord_add reverse flag
  Resolves: RHBZ#1803026

* Sat Dec 14 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.8-1
- Update to version 0.1.8 (bug fix release)
  - roles/ipaclient/README.md: Add information about ipaclient_otp
  - Install and enable firewalld if it is configured for ipaserver and
    ipareplica roles
  - ipaserver_test: Do not use zone_overlap_check for domain name validation
  - Allow execution of API commands that do not require a name
  - Update README-host: Drop options from allow_*keytab parameters docs
  - ipauser: Extend email addresses with default email domain if no domain is
    given
    Resolves: RHBZ#1747413
  Related: RHBZ#1748986

* Mon Dec  2 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.7-1
- Update to version 0.1.7
  - Add debian support for ipaclient
  - Added support for predefining client OTP using ipaclient_otp
  - ipatopologysegment: Store suffix for commands in command list
  - ipatopologysegment: Fail for missing entry with reinitialized
  - Utils scripts: ansible-ipa-[server,replica,client]-install
  - ipaserver_test,ipareplica_prepare: Do not return _pkcs12_file settings
  - ansible_freeipa_module: Add support for GSSAPI
  - ansible_ipa_client: Drop import of configure_nsswitch_database
  - New host management module
  - New hostgroup management module
  - ipagroup: Remove unused member_[present,absent] states
  - external-ca tests: Fix typo in inventory files
  - tests/external-signed-ca tests: Fix external-ca.sh to use proper serials
  - ipagroup: Rework to use same mechanisms as ipahostgroup module
  - ansible_freeipa_module: api_command should not have extra try clause
  - ansible_freeipa_module: compare_args_ipa needs to compare lists orderless
  - ansible_freeipa_module: New function api_check_param
  - ansible_freeipa_module: New functions module_params_get and _afm_convert
  - ansible_freeipa_module: Add missing to_text import for _afm_convert
  - ansible_freeipa_module: Convert tuple to list in compare_args_ipa
  - ansible_freeipa_module: New function api_get_realm
  - ipauser: User module extension
  - New sudocmd management module
  - New sudocmdgroup management module
  - ansible_freeipa_module: Convert int to string in compare_args_ipa
  - New pwpolicy management module
  - New hbacsvc (HBAC Service) management module
  - New hbacsvcgroup (HBAC Service Group) management module
  - ipagroup: Properly support IPA versions 4.6 and RHEL-7
  - ipagroup: Fix changed flag, new test cases
  - ipauser: Add info about version limitation of passwordexpiration
  - New hbacrule (HBAC Rule) management module
  - ipahostgroup: Fix changed flag, support IPA 4.6 on RHEL-7, new test cases
  - New sudorule (Sudo Rule) management module
  - ipauser: Support 'sn' alias of 'last' for surname
  - Update galaxy.yml: Update description, drop empty dependencies
  - Update ipauser.py: Fix typo in users.name description
  - ipaclient: Fix misspelled sssd options
  - ipauser: Return generated random password
  - ipahost: Return generated random password
  - Added context configuration to api_connect
  - ansible_freeipa_module: Better support for KRB5CCNAME environment variable
  - ipa[server,replica,client]: Add support for CentOS-8
  - ipahost: Extension to be able handle several hosts and all settings
  - Flake8 fixes
  - Documentation updates
  - Cleanup
  Resolves: RHBZ#1748986

* Fri Sep  6 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-4
- ansible_ipa_client: Drop import of configure_nsswitch_database
  (RHBZ#1748905)

* Wed Jul 31 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-3
- ipatopologysegment: Store suffix for commands in command list (RHBZ#1733547)
- ipatopologysegment: Fail for missing entry with reinitialized (RHBZ#1733559)

* Tue Jul 23 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-2
- Drop dirserv_cert_files key from utils/gen_module_docs.py for covscan

* Tue Jul 23 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-1
- update to version 0.1.6
  - Lots of documentation updates in READMEs and modules
  - library/ipaclient_get_otp: Enable force mode for host_add call (fixes #74)
  - Flake8 and pylint reated fixes
  - Fixed wrong path to CheckedIPAddress class in ipareplica_test
  - Remove unused ipaserver/library/ipaserver.py
  - No not use wildcard imports for modules
  - ipareplica: Add support for pki_config_override
  - ipareplica: Initialize dns.ip_addresses and dns.reverse_zones for dns setup
  - ipareplica_prepare: Properly initialize pin and cert_name variables
  - ipareplica: Fail with proper error messages
  - ipaserver: Properly set settings related to pkcs12 files
  - ipaclient: RawConfigParser is not always provided by six.moves.configparser
  - ipaclient_setup_nss: paths.GETENT is not available before
    freeipa-4.6.90.pre1
  - ipaserver_test: Initialize value from options.zonemgr
  - ipareplica_setup_custodia: create_replica only available in newer releases
  - ipaclient: Fix typo in dnsok assignment for ipaclient_setup_nss
  - ipa[server,replica]: Set _packages_adtrust for Ubuntu
  - New build script for galaxy release
  - New utils script to update module docs
- Changes from ansible-freeipa-0.1.5
  - Support for IPA 4.8.0
  - New user management module
  - New group management module
  - ipaserver: Support external signed CA
  - RHEL-8 specific vars files to be able to install needed modules
    automatically
  - ipareplica: Fixes for certmonger and kra setup
  - New tests folder
  - OTP related updates to README files

* Thu Jul  4 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.4-2
- ansible_ipa_client: Always set options.unattended (RHBZ#1726645)
- ipaserver_prepare: Properly report error, do show trace back (RHBZ#1726668)
- ipa[server,replica,client]: RHEL-8 specific vars files (RHBZ#1727095)
- ipatopology modules: Use ipaadmin_ prefix for principal and password
  (RHBZ#1727101)

* Mon Jun 17 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.4-1
- update to version 0.1.4
  - ipatopologysegment: Use commands, not command

* Mon Jun 17 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.3-1
- update to version 0.1.3
  - ipaclient_test: Fix Python2 decode use with Python3
  - Fixed: #86 (AttributeError: 'str' object has no attribute 'decode')
  - ipaclient_get_otp: Remove ansible_python_interpreter handling
  - ipaclient: Use omit (None) for password, keytab, no string length checks
  - ipaclient_join: Support to use ipaadmin_keytab without ipaclient_use_otp
  - ipaclient: Report error message if ipaclient_get_otp failed
  - Fixes #17 Improve how tasks manage package installation
  - ipareplica: The dm password is not needed for ipareplica_master_password
  - ipareplica: Use ipareplica_server if set
  - ipatopologysegment: Allow domain+ca suffix, new state: checked
  - Documentation updates
  - Cleanups

* Tue Jun 11 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.2-3
- bump release for functional test

* Tue Jun 11 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.2-2
- bump release for functional test

* Fri Jun  7 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.2-1
- update to version 0.1.2
  - Now a new Ansible Collection
  - Fix gssapi requirement for OTP: It is only needed if keytab is used with
    OTP now.
  - Fix wrong ansible argument types
  - Do not fail on textwrap for replica deployments with CA
  - Ansible lint and galaxy fixes
  - Disable automatic removal of replication agreements in uninstall
  - Enable freeipa-trust service if adtrust is enabled
  - Add support for hidden replica
  - New topology managament modules
  - Add support for pki_config_override
  - Fix host name setup in server deployment
  - Fix errors when ipaservers variable is not set
  - Fix ipaclient install role length typo
  - Cleanups
  
* Mon May  6 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.1-1
- Initial package
