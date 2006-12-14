# TODO: webapps
Summary:	Web-based tool written in PHP aimed at managing proFTPd server
Summary(pl):	Napisany w PHP system do zarz±dzania serwerem proFTPd poprzez interfejs WWW i MySQL
Name:		proftpd_admin
Version:	0.9
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/proftpd-adm/%{name}_v%{version}.tar.gz
# Source0-md5:	413ee31b000301c5623c5c9a08d8ecfe
Source1:	%{name}.conf
URL:		http://proftpd-adm.sourceforge.net/
Requires:	php-mysql
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_proftpd_admin_dir	%{_datadir}/%{name}

%description
Web-based tool written in PHP and MySQL aimed at managing proFTPd
server.

%description -l pl
Napisany w PHP system do zarz±dzania serwerem proFTPd poprzez
interfejs WWW i MySQL.

%prep
%setup -q -n %{name}_v%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_proftpd_admin_dir}/{jscript,misc/{database_structure,howto_install,sample_config,user_script}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd

install *.php *.xml $RPM_BUILD_ROOT%{_proftpd_admin_dir}
install COPYING VERSION $RPM_BUILD_ROOT%{_proftpd_admin_dir}
install jscript/*.js $RPM_BUILD_ROOT%{_proftpd_admin_dir}/jscript
install misc/database_structure/*.sql $RPM_BUILD_ROOT%{_proftpd_admin_dir}/misc/database_structure
install misc/howto_install/*.html $RPM_BUILD_ROOT%{_proftpd_admin_dir}/misc/howto_install
install misc/sample_config/*.conf $RPM_BUILD_ROOT%{_proftpd_admin_dir}/misc/sample_config
install misc/user_script/*.sh $RPM_BUILD_ROOT%{_proftpd_admin_dir}/misc/user_script

cp -rf style $RPM_BUILD_ROOT%{_proftpd_admin_dir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc INSTALL TODO misc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
%dir %{_proftpd_admin_dir}
%{_proftpd_admin_dir}/jscript
%{_proftpd_admin_dir}/misc
%{_proftpd_admin_dir}/style
%{_proftpd_admin_dir}/COPYING
%{_proftpd_admin_dir}/VERSION
%{_proftpd_admin_dir}/*.php
%{_proftpd_admin_dir}/*.xml
