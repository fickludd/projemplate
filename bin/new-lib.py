#!/usr/bin/python

import os
import subprocess

NAME = "New-Lib"
VERSION = "0.0.1"

print
print NAME, VERSION
print "="*(len(NAME) + len(VERSION) + 1)
print


# //////////////////	User input	//////////////////
# ====================================================

ok = False
while not ok:
	pUnixName 	= raw_input("unix name: ")
	pCamelName 	= raw_input("camel case name: ")
	pgroup 		= raw_input("project group: ")
	pversion 	= "0.0.1-SNAPSHOT"
	okv 		= raw_input("ok (y/n)? ")
	ok = (okv == "y" or ok == "Y" or ok == "k")


# //////////////////	Project dir	//////////////////
# ====================================================

baseDir = os.getcwd()
pDir = ""


# //////////////////	Maven	//////////////////
# ================================================

pom = open("pom.xml", 'w')
pom.write("""<project 
		xmlns="http://maven.apache.org/POM/4.0.0" 
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>%s</groupId>
  <artifactId>%s</artifactId>
  <version>%s</version>
  <packaging>jar</packaging>

  <!--
  <name>Maven Quick Start Archetype</name>
  <url>http://maven.apache.org</url>
  -->

  <properties>
	<scala.version>2.10.1</scala.version>
  </properties>

  <scm>
	<developerConnection>scm:git:https://github.com/fickludd/%s</developerConnection>
  </scm>

	<repositories>
		<repository>
			<id>scala-tools.org</id>
			<name>Scala-tools Maven2 Repository</name>
			<url>http://scala-tools.org/repo-releases</url>
		</repository>
	</repositories>
  
	<pluginRepositories>
		<pluginRepository>
			<id>scala-tools.org</id>
			<name>Scala-tools Maven2 Repository</name>
			<url>http://scala-tools.org/repo-releases</url>
		</pluginRepository>
	</pluginRepositories>
  
	<dependencies>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.8.2</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.scala-lang</groupId>
			<artifactId>scala-library</artifactId>
			<version>${scala.version}</version>
		</dependency>
	</dependencies>

	<distributionManagement>
	    <repository>
			<id>local</id>
			<name>localReporsitory</name>
			<url>file:///Users/johanteleman/.m2/repository</url>
	    </repository>
	</distributionManagement>

	<build>
		<sourceDirectory>src/main/scala</sourceDirectory>
		<testSourceDirectory>src/test/scala</testSourceDirectory>

		<plugins>
			
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-release-plugin</artifactId>
				<version>2.4.1</version>
			</plugin>

			<plugin>
				<groupId>org.scala-tools</groupId>
				<artifactId>maven-scala-plugin</artifactId>
				<executions>
					<execution>
						<goals>
							<goal>compile</goal>
							<goal>testCompile</goal>
						</goals>
					</execution>
				</executions>
				<configuration>
					<scalaVersion>${scala.version}</scalaVersion>
					<jvmArgs>
						<jvmArg>-Xms64m</jvmArg>
						<jvmArg>-Xmx1024m</jvmArg>
					</jvmArgs>
				</configuration>
			</plugin>

			<plugin>
				<artifactId>maven-surefire-plugin</artifactId>
				<version>2.9</version>
				<configuration>
					<includes>
						<include>**/*Test.*</include>
					</includes>
					<excludes>
						<exclude>**/*IntegrationTest.*</exclude>
						<exclude>**/*IT.*</exclude>
					</excludes>
					<!--<debugForkedProcess>true</debugForkedProcess>  -->
				</configuration>
			</plugin>
	  
			<plugin>
				<artifactId>maven-failsafe-plugin</artifactId>
				<version>2.6</version>
				<configuration>
					<includes>
						<include>**/*IntegrationTest.*</include>
						<include>**/*IT.*</include>
					</includes>
					<workingDirectory>target/test-classes</workingDirectory>
				</configuration>
				<executions>
				  <execution>
						<goals>
							<goal>integration-test</goal>
							<goal>verify</goal>
						</goals>
					</execution>
				</executions>
			</plugin>

		</plugins>
	</build>
</project>""" % (
	pgroup,
	pCamelName,
	pversion,
	pUnixName
	))
pom.close()


# //////////////////	Create directory structure	//////////////////
# ====================================================================

os.mkdir("src")
os.mkdir("src/main")
os.mkdir("src/main/scala")
os.mkdir("src/test")
os.mkdir("src/test/scala")

pkgs = pgroup.split(".")
pDir = ""
for pkg in pkgs:
	pDir = "%s/%s" % (pDir, pkg) 
	os.mkdir("src/main/scala%s" % pDir)
	os.mkdir("src/test/scala%s" % pDir)



# //////////////////	Main scala source file	//////////////////
# ================================================================

mainSrc = open("src/main/scala%s/%s.scala" % (pDir, pCamelName), "w")
mainSrc.write("""/*
 * %s
 *	Copyright (C) 2014 Johan Teleman
 */
package %s

class %s {

}
""" % (pCamelName, pgroup, pCamelName))
mainSrc.close()



# //////////////////	Git 	//////////////////
# ================================================

gitignore = open("./.gitignore", "w")
gitignore.write("""# ignore all bin directories
# matches "bin" in any subfolder
bin/

# ignore all target directories
target/

# ignore all files ending with ~
*~ """)
gitignore.close()

subprocess.call(["git", "add", "src", "pom.xml"])
subprocess.call(["git", "commit", "-m", "'Initial commit'"])
subprocess.call(["git", "push", "origin", "master"])

