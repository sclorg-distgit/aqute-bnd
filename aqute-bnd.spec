%global pkg_name aqute-bnd
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           %{?scl_prefix}%{pkg_name}
Version:        0.0.363
Release:        11.12%{?dist}
Summary:        BND Tool
License:        ASL 2.0
URL:            http://www.aQute.biz/Code/Bnd

# NOTE : sources for 0.0.363 are no longer available
# The following links would work for 0.0.370-0.0.401 version range, but
# we need to stay by 0.0.363 to minimize problems during the 1.43.0 introduction
Source0:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.jar
Source1:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.pom
Source2:        aqute-service.tar.gz

Patch0:         0001-Port-to-Ant-1.9.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}ant


%description
The bnd tool helps you create and diagnose OSGi R4 bundles.
The key functions are:
- Show the manifest and JAR contents of a bundle
- Wrap a JAR so that it becomes a bundle
- Create a Bundle from a specification and a class path
- Verify the validity of the manifest entries
The tool is capable of acting as:
- Command line tool
- File format
- Directives
- Use of macros

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -c -n %{pkg_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%patch0 -p1

mkdir -p target/site/apidocs/
mkdir -p target/classes/
mkdir -p src/main/
mv OSGI-OPT/src src/main/java
pushd src/main/java
tar xfs %{SOURCE2}
popd
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ComponentDef.java
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ServiceComponent.java

# get rid of eclipse plugins which are not usable anyway and complicate
# things
rm -rf src/main/java/aQute/bnd/annotation/Test.java \
       src/main/java/aQute/bnd/{classpath,jareditor,junit,launch,plugin} \
       aQute/bnd/classpath/messages.properties

# remove bundled stuff
for f in $(find aQute/ -type f -name "*.class"); do
    rm -f $f
done

# Convert CR+LF to LF
sed -i "s|\r||g" LICENSE
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
export LANG=en_US.utf8
export OPT_JAR_LIST=:
export CLASSPATH=$(build-classpath ant)

/usr/bin/javac -d target/classes -target 1.5 -source 1.5 $(find src/main/java -type f -name "*.java")
/usr/bin/javadoc -d target/site/apidocs -sourcepath src/main/java aQute.lib.header aQute.lib.osgi aQute.lib.qtokens aQute.lib.filter
cp -p LICENSE maven-dependencies.txt plugin.xml pom.xml target/classes
for f in $(find aQute/ -type f -not -name "*.class"); do
    cp -p $f target/classes/$f
done
pushd target/classes
/usr/bin/jar cmf ../../META-INF/MANIFEST.MF ../%{pkg_name}-%{version}.jar *
popd
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
# jars
install -Dpm 644 target/%{pkg_name}-%{version}.jar %{buildroot}%{_javadir}/%{pkg_name}.jar

# pom
install -Dm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 0.0.363-11.12
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0.0.363-11.11
- Mass rebuild 2015-01-13

* Thu Jan 08 2015 Michal Srb <msrb@redhat.com> - 0.0.363-11.10
- Workaround issue with alternatives on RHEL6

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 0.0.363-11.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0.0.363-11.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-11.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.0.363-11
- Mass rebuild 2013-12-27

* Thu Sep 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-10
- Add patch for compatibility with Ant 1.9

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.363-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.363-6
- Get rid of unusable eclipse plugins to simplify dependencies

* Fri Mar 02 2012 Jaromir Capik <jcapik@redhat.com> - 0.0.363-5
- Fixing build failures on f16 and later

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.363-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-3
- Resurrection of bundled non-class files

* Thu Sep 22 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-2
- Bundled classes removed
- jpackage-utils dependency added to the javadoc subpackage

* Wed Sep 21 2011 Jaromir Capik <jcapik@redhat.com> - 0.0.363-1
- Initial version (cloned from aqute-bndlib 0.0.363)
