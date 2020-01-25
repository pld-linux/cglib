%define uscver 2.1_3
Summary:	Code Generation Library
Summary(pl.UTF-8):	Biblioteka do generowania kodu
Name:		cglib
Version:	2.1.3
Release:	2
Epoch:		0
License:	Apache Software License 2
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/cglib/%{name}-src-%{uscver}.jar
# Source0-md5:	17747df2f9e6ad660962c629282c0fca
Source1:	%{name}-missing-words.txt
Patch0:		%{name}-build_xml.patch
Patch1:		%{name}-ExamplePreProcessor.patch
URL:		http://cglib.sourceforge.net/
BuildRequires:	ant >= 1.6
BuildRequires:	asm >= 1.5.3
BuildRequires:	asm2
BuildRequires:	aspectwerkz >= 1.0
#BuildRequires:	jarjar
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	asm >= 1.5.3
Requires:	aspectwerkz >= 1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cglib is a powerful, high performance and quality Code Generation
Library. It is used to extend Java classes and implement interfaces at
runtime.

%description -l pl.UTF-8
cglib to potężna, o wysokiej wydajności i jakości biblioteka
generowania kodu. Jest używana do rozszerzania klas Javy i
implementowania interfejsów w trakcie działania programu.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -qc
find -name '*.jar' | xargs rm -vf

( cat << EO_JP
grant codeBase "file:/-"{
  permission java.security.AllPermission;
};
EO_JP
) > java.policy
# add missing test input file
cp %{SOURCE1} src/test/net/sf/cglib/util/words.txt

%patch0
%patch1

%build
build-jar-repository -s -p lib ant asm-attrs asm asm2 asm-util junit

#aspectwerkz-core \
#jarjar \

%ant test javadoc jar

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{uscver}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p dist/%{name}-nodep-%{uscver}.jar \
	$RPM_BUILD_ROOT%{_javadir}/%{name}-nodep-%{version}.jar

cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rmdir docs/api
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
