%define uscver 2.1_3
Summary:	Code Generation Library
Summary(pl):	Biblioteka do generowania kodu
Name:		cglib
Version:	2.1.3
Release:	2
Epoch:		0
License:	Apache Software License 2
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/cglib/%{name}-src-%{uscver}.jar
# Source0-md5:	17747df2f9e6ad660962c629282c0fca
Source1:	%{name}-missing-words.txt
Patch0:		%{name}-2.1.3-build_xml.patch
Patch1:		%{name}-ExamplePreProcessor.patch
URL:		http://cglib.sourceforge.net/
BuildRequires:	asm >= 1.5.3
BuildRequires:	asm2
BuildRequires:	aspectwerkz >= 1.0
BuildRequires:	ant >= 1.6
BuildRequires:	jarjar
BuildRequires:	junit
Requires:	asm >= 1.5.3
Requires:	aspectwerkz >= 1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cglib is a powerful, high performance and quality Code Generation
Library. It is used to extend Java classes and implement interfaces
at runtime.

%description -l pl
cglib to potê¿na, o wysokiej wydajno¶ci i jako¶ci biblioteka
generowania kodu. Jest u¿ywana do rozszerzania klas Javy i
implementowania interfejsów w trakcie dzia³ania programu.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -T -c -n %{name}
unzip -q %{SOURCE0}
# remove all binary libs
for f in $(find . -name "*.jar"); do mv $f $f.no; done
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
build-jar-repository -s -p lib \
ant \
asm/asm-attrs \
asm/asm \
asm2/asm2 \
asm/asm-util \
aspectwerkz-core \
jarjar \
junit \

ant test javadoc jar

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
%{_javadocdir}/*
