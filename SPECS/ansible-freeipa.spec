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
Patch1: ansible-freeipa-1.9.2-paclient-Fix-allow_repair-with-removed-krb5.conf-an_RHBZ#2189229.patch
Patch2: ansible-freeipa-1.9.2-ipaclient-Defer-creating-the-final-krb5.conf-on-clients_RHBZ#2189232.patch
Patch3: ansible-freeipa-1.9.2-ipaclient-Defer-krb5-configuration-fix_RHBZ#2189232.patch
Patch4: ansible-freeipa-1.9.2-Fix-typo-in-ipapwpolicy.py_RHBZ#2218186.patch
BuildArch: noarch
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
Requires: ansible-core
%endif

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
  Resolves: RHBZ#2218186

* Mon Apr 24 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-2
- ipaclient: Fix allow_repair with removed krb5.conf and DNS lookup
  Resolves: RHBZ#2189229
- ipaclient: Defer creating the final krb5.conf on clients
  Resolves: RHBZ#2189232

* Tue Jan 31 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.2-1
- Update to version 1.9.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.2
  Resolves: RHBZ#2125592
- ipabackup: Use ipabackup_item again in copy_backup_to_server
  Resolves: RHBZ#2165953

* Mon Jan 30 2023 Thomas Woerner <twoerner@redhat.com> - 1.9.1-1
- Update to version 1.9.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.1
  Resolves: RHBZ#2125592
- pwpolicy: Allow clearing policy values
  Resolves: RHBZ#2150334
- Use netgroup_find instead of netgroup_show to workaround IPA bug
  Resolves: RHBZ#2144725

* Wed Dec  7 2022 Thomas Woerner <twoerner@redhat.com> - 1.9.0-1
- Update to version 1.9.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.9.0
  Related: RHBZ#2125592
- pwpolicy: Add support for password check and grace limit
  Resolves: RHBZ#2127911
- ipaconfig: Do not allow enable_sid set to False
  Resolves: RHBZ#2127446
- ipaclient: No kinit on controller for deployment using OTP
  Resolves: RHBZ#2127887
- ipaclient: Configure DNS resolver
  Resolves: RHBZ#2127895
- New netgroup management module
  Resolves: RHBZ#2127910
- sudorule: Add support for 'hostmask' parameter
  Resolves: RHBZ#2127913
- ipaconfig: Fix fail_json calls
  Resolves: RHBZ#2134375
- ipaconfig: Do not require enable_sid for add_sids or netbios_name
  Resolves: RHBZ#2134505
- ipaserver: Add missing idstart check
  Resolves: RHBZ#2132731

* Mon Sep 12 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.4-1
- Update to version 1.8.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.4
  Resolves: RHBZ#2125592
- 'ansible-doc' -l lists most idm modules as 'UNDOCUMENTED'
  Resolves: RHBZ#2125603
- ansible-freeipa Replica Install Setup DNS fails
  Resolves: RHBZ#2125616
- ipaconfig does not support SID and netbios attributes
  Resolves: RHBZ#2069184

* Tue Aug 16 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.3-1
- Update to version 1.8.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.3
  Related: RHBZ#2080322
- Fixes replica deployment issue for domains without SID support.
  Related: RHBZ#2110478

* Thu Jul 28 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.2-1
- Update to version 1.8.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.2
  Related: RHBZ#2080322
- SIDs are always generated for server and replica deployments
  Resolves: RHBZ#2110478
- Random Serial Numbers are not enabled by default any more
  Resolves: RHBZ#2110523
- Fixes comparison of bool values in IPA 4.9.10+ for ipadnsconfig
  Resolves: RHBZ#2110538

* Thu Jul  7 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.1-1
- Update to version 1.8.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.8.1
  Related: RHBZ#2080322
- ipa server deploys failing with latest IPA compose
  Resolves: RHBZ#2103924
- ipaserver_external_cert_files failes to copy with ansible 2.13
  Resolves: RHBZ#2104142

* Fri Jun 24 2022 Thomas Woerner <twoerner@redhat.com> - 1.8.0-1
- idrange: Fix usage of dom_name when idrange doesn't exist.
  Resolves: RHBZ#2086994
- smartcard roles for ansible-freeipa
  Resolves: RHBZ#2076567

* Fri Apr 29 2022 Thomas Woerner <twoerner@redhat.com> - 1.7.0-1
- Update to version 1.7.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.7.0
  Resolves: RHBZ#2080322
- New idrange management module.
  Resolves: RHBZ#2069188
- Not able to update empty descriptions in automount maps.a
  Resolves: RHBZ#2050179
- New servicedelegationrule management module.
  Resolves: RHBZ#2069179
- New servicedelegationtarget management module.
  Resolves: RHBZ#2069180
- Add support for managing idoverrideusers in ipagroup.
  Resolves: RHBZ#2069183

* Thu Jan 27 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.3-1
- Update to version 1.6.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.3
  Related: RHBZ#2010622

* Wed Jan 26 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.2-1
- Update to version 1.6.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.2
  Related: RHBZ#2010622

* Fri Jan 21 2022 Thomas Woerner <twoerner@redhat.com> - 1.6.1-1
- Update to version 1.6.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.6.0
  Related: RHBZ#2010622
- Add module to manage automount maps
  Resolves: RHBZ#2040701
- Add module to manage automount keys
  Resolves: RHBZ#2040702

* Wed Dec 29 2021 Thomas Woerner <twoerner@redhat.com> - 1.5.3-1
- Update to version 1.5.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.2
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v1.5.0
  Related: RHBZ#2010622
- automember set default group/hostgroup is missing from the automember module
  Resolves: RHBZ#2021947
- automember remove default group/hostgroup is missing from the automember
  module
  Resolves: RHBZ#2021952
- automember rebuild is missing from the automember module
  Resolves: RHBZ#2021954
- automember remove orphans group/hostgroup is missing from the automember
  module
  Resolves: RHBZ#2021955
- Not able to update existing automember rule description
  Resolves: RHBZ#1976922

* Tue Oct  5 2021 Thomas Woerner <twoerner@redhat.com> - 0.4.0-1
- Update to version 0.4.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.4.0
  Resolves: RHBZ#2010622
- Add ability to run modules remotely
  Resolves: RHBZ#2010633
- New management module ipaautomountlocation
  Resolves: RHBZ#2010643

* Mon Aug 16 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.8-3
- Add requirement for ansible-core
  Resolves: RHBZ#1993857
- Remove python3, pip and ansible installation from sanity test
  Related: RHBZ#1993857
- Replace json_query in tests/user/test_users_absent.yml
  Resolves: RHBZ#1992997

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.3.8-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jul 15 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.8-1
- Update to version 0.3.7 and 0.3.8
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.7
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.8
  Related: RHBZ#1972178
- automember: Verify condition keys
  Resolves: RHBZ#1981713
- automember: Fix result["failed"] issues with conditions
  Resolves: RHBZ#1981713
- automember: Fix action to be automember or member, not service
  Resolves: RHBZ#1981711

* Thu Jun 17 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-3
- Apply fix for ipabackup: Use module to get IPA_BACKUP_DIR from ipaplatform
  Resolves: RRBZ#1973173

* Mon Jun  7 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.6-1
- Update to version 0.3.6
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.6
  Resolves: RHBZ#1972178
- ansible-freeipa-tests not in the compose
  Resolves: RHBZ#1940014
- Remove unsupported parameter for (ipapermission) module: perm_rights from
  permission-present.yml
  Resolves: RHBZ#1973167
- Sample playbook included for selfservice module is incorrect
  Resolves: RHBZ#1973166
- ipa-client-install failing with error code 7(keytab: /usr/sbin/ipa-rmkeytab
  returned 7)
  Resolves: RHBZ#1973169
- New management module ipaserver
  Resolves: RHBZ#1973171
- New management module ipaautomember
  Resolves: RHBZ#1973172

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 0.3.5-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Mar  3 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.5-1
- Update to version 0.3.5
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.5

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Thomas Woerner <twoerner@redhat.com> - 0.3.4-1
- Update to version 0.3.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.4
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.3
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.2

* Wed Dec  2 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.1-1
- Update to version 0.3.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.1
- ipabackup: Fix undefined vars for conditions in shell tasks without else

* Tue Dec  1 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-2
- Ship ipabackup role for backup and restore

* Thu Nov 26 2020 Thomas Woerner <twoerner@redhat.com> - 0.3.0-1
- Update to version 0.3.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.3.0

* Fri Oct 09 2020 Thomas Woerner <twoerner@redhat.com> - 0.2.1-1
- Update to version 0.2.1
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.2.1
- Update to version 0.2.0
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.2.0
- New tests sub package providing upstream tests
- Utils in /usr/share/ansible-freeipa/utils

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.12-1
- Update to version 0.1.12 bug fix only release

* Thu Jun 11 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.11-1
- Update to version 0.1.11
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.11

* Mon Apr 27 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.10-1
- Update to version 0.1.10 with fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.10

* Mon Mar 16 2020 Thomas Woerner <twoerner@redhat.com> - 0.1.9-1
- Update to version 0.1.8 with lots of fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.8-1
- Update to version 0.1.8 with lots of fixes and additional modules
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.8
  https://github.com/freeipa/ansible-freeipa/releases/tag/v0.1.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.6-1
- Update to version 0.1.6
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

* Tue Jul  9 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.5-2
- Update README-user.md: Fixed examples, new example
- ipauser example playbooks: Fixed actions, new example

* Tue Jul  9 2019 Thomas Woerner <twoerner@redhat.com> - 0.1.5-1
- Update to version 0.1.5
  - Support for IPA 4.8.0
  - New user management module
  - New group management module
  - ipaserver: Support external signed CA
  - RHEL-8 specific vars files to be able to install needed modules
    automatically
  - ipareplica: Fixes for certmonger and kra setup
  - New tests folder
  - OTP related updates to README files
- Updates of version 0.1.4
  - ipatopologysegment: Use commands, not command
- Updates of version 0.1.3
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
- Update of version 0.1.2
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
