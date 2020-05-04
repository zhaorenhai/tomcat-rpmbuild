%define __jar_repack %{nil}
%define tomcat_group tomcat
%define tomcat_user tomcat
%define tomcat_home /usr/share/tomcat
%define tomcat_var_home /var/tomcat/
%define tomcat_conf_home %{_sysconfdir}/tomcat
%define tomcat_log_home /var/log/tomcat
%define systemd_dir /usr/lib/systemd/system/
%define tomcat_version 9.0.34
%define tomcat_release 1

Name: tomcat
Version: %{tomcat_version} 
Release: %{tomcat_release}
Summary: Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API 
License: Apache License 2.0 
URL: http://tomcat.apache.org
BuildArch: noarch
Group: Networking/Daemons
Source0: apache-tomcat-%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.sysconfig
Source3: %{name}.logrotate
Conflicts: tomcat, tomcat7, tomcat8, tomcat9, tomcat10

%description 
The Apache Tomcat® software is an open source implementation of the Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket technologies. The Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket specifications are developed under the Java Community Process.
The Apache Tomcat software is developed in an open and participatory environment and released under the Apache License version 2. The Apache Tomcat project is intended to be a collaboration of the best-of-breed developers from around the world. We invite you to participate in this open development project.
Apache Tomcat software powers numerous large-scale, mission-critical web applications across a diverse range of industries and organizations.
Apache Tomcat, Tomcat, Apache, the Apache feather, and the Apache Tomcat project logo are trademarks of the Apache Software Foundation.

%prep
%setup -q -n apache-tomcat-%{version}

%build
 
%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

rm -f %{buildroot}/%{tomcat_home}/bin/*.bat

install -d -m 755 %{buildroot}/%{tomcat_var_home}
mv %{buildroot}/%{tomcat_home}/webapps %{buildroot}/%{tomcat_var_home}/
mv %{buildroot}/%{tomcat_home}/temp %{buildroot}/%{tomcat_var_home}/
mv %{buildroot}/%{tomcat_home}/work %{buildroot}/%{tomcat_var_home}/
cd %{buildroot}/%{tomcat_home}/
chmod 755 %{buildroot}/%{tomcat_var_home}/webapps
chmod 775 %{buildroot}/%{tomcat_var_home}/temp
chmod 775 %{buildroot}/%{tomcat_var_home}/work
ln -s %{tomcat_var_home}/webapps webapps
ln -s %{tomcat_var_home}/temp temp
ln -s %{tomcat_var_home}/work work
cd -

rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/%{tomcat_log_home}/
cd %{buildroot}/%{tomcat_home}/
ln -s %{tomcat_log_home} logs
cd -

install -d -m 755 %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{tomcat_home}/conf %{buildroot}/%{tomcat_conf_home}
cd %{buildroot}/%{tomcat_home}/
ln -s %{tomcat_conf_home} conf
cd -

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

# sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -g 91 -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd -u 91 --comment "Apache Tomcat" --shell /sbin/nologin -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group},0770)
%{tomcat_log_home}/
%defattr(-,root,root)
%{tomcat_home}
%{systemd_dir}/%{name}.service
%{_sysconfdir}/logrotate.d/%{name} 
%defattr(-,root,%{tomcat_group})
%{tomcat_var_home}
%exclude %{tomcat_home}/webapps/manager
%exclude %{tomcat_home}/webapps/host-manager
%exclude %{tomcat_var_home}/webapps/manager
%exclude %{tomcat_var_home}/webapps/host-manager
%exclude %{tomcat_home}/webapps/ROOT
%exclude %{tomcat_var_home}/webapps/ROOT
%exclude %{tomcat_home}/webapps/examples
%exclude %{tomcat_var_home}/webapps/examples
%exclude %{tomcat_home}/webapps/docs
%exclude %{tomcat_var_home}/webapps/docs
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{tomcat_conf_home}/*

%post
/bin/systemctl daemon-reload

%package manager
Summary:    Admin Webapps for Apache Tomcat
Version:    %{tomcat_version}
BuildArch:  noarch
Release:    %{tomcat_release}
License:    Apache License 2.0 
Group:      Networking/Daemons
Requires:   tomcat >= %{tomcat_version}-%{tomcat_release}

%description manager 
This package contains the manager and host-manager webapps used to
assist in the deploying and configuration of Tomcat. 

%files manager 
%{tomcat_var_home}/webapps/manager
%{tomcat_var_home}/webapps/host-manager

%package root-page 
Summary:    Root Page for Apache Tomcat
Version:    %{tomcat_version}
BuildArch:  noarch
Release:    %{tomcat_release}
License:    Apache License 2.0
Group:      Networking/Daemons
Requires:   tomcat >= %{tomcat_version}-%{tomcat_release}

%description root-page 
This package contains the default root page webapps used to
assist in the deploying and configuration of Tomcat.

%files root-page
%{tomcat_var_home}/webapps/ROOT

%package docs 
Summary:    Docs for Apache Tomcat
Version:    %{tomcat_version}
BuildArch:  noarch
Release:    %{tomcat_release}
License:    Apache License 2.0
Group:      Networking/Daemons
Requires:   tomcat >= %{tomcat_version}-%{tomcat_release}

%description docs 
This package contains docs of Tomcat.

%files docs 
%{tomcat_var_home}/webapps/docs

%package examples 
Summary:    Examples for Apache Tomcat
Version:    %{tomcat_version}
BuildArch:  noarch
Release:    %{tomcat_release}
License:    Apache License 2.0
Group:      Networking/Daemons
Requires:   tomcat >= %{tomcat_version}-%{tomcat_release}

%description examples 
This package contains the examples of Tomcat.

%files examples 
%{tomcat_var_home}/webapps/examples
