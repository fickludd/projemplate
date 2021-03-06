#!/usr/bin/python

import os
import subprocess

NAME = "New-App"
VERSION = "0.0.1"

print
print NAME, VERSION
print "="*(len(NAME) + len(VERSION) + 1)
print

def askOk(str = "ok?"):
	while True:
		okv = raw_input("%s (y/n): " % str)
		if okv == "y" or okv == "Y" or okv == "k":
			return True
		elif okv == "n" or okv == "N":
			return False


# //////////////////	User input	//////////////////
# ==================================================

ok = False
while not ok:
	pUnixName 	= raw_input("unix name: ")
	pCamelName 	= raw_input("camel case name: ")
	pgroup 		= raw_input("project group: ")
	pversion 	= "0.0.1-SNAPSHOT"
	useSlick	= askOk("use Slick database?")
	useGUI		= askOk("want swing GUI?")
	ok = askOk()


# //////////////////	Project dir	//////////////////
# ==================================================

pDir = "."


# //////////////////	Maven	//////////////////
# ============================================

pom = open("pom.xml", 'w')
pom.write("""<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
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
		<mainClass>%s.%s</mainClass>
		<selfContained.jar>${basedir}/target/${build.finalName}-jar-with-dependencies.jar</selfContained.jar>
	</properties>

	<scm>
		<developerConnection>scm:git:file://localhost/path_to_repository</developerConnection>
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
		</dependency>""" % (
	pgroup,
	pCamelName,
	pversion,
	pgroup,
	pCamelName
	))

if useSlick:
	pom.write("""
		<dependency>
			<groupId>com.typesafe.slick</groupId>
			<artifactId>slick_2.10</artifactId>
			<version>1.0.1</version>
		</dependency>""")

if useGUI:
	pom.write("""
		<dependency>
			<groupId>org.scala-lang</groupId>
			<artifactId>scala-swing</artifactId>
			<version>${scala.version}</version>
		</dependency>
		<dependency>
			<groupId>se.strawbrary</groupId>
			<artifactId>SwingApplication</artifactId>
			<version>0.0.3</version>
		</dependency>""")
else:
	pom.write("""
		<dependency>
			<groupId>se.strawbrary</groupId>
			<artifactId>Application</artifactId>
			<version>1.0.8</version>
		</dependency>""")

pom.write("""
	</dependencies>

	<build>
		<sourceDirectory>src/main/scala</sourceDirectory>
		<testSourceDirectory>src/test/scala</testSourceDirectory>

		<resources>
			<resource>
			<directory>src/main/resources</directory>
			<filtering>true</filtering>
			</resource>
		</resources>

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
				<artifactId>maven-assembly-plugin</artifactId>
				<configuration>
					<descriptorRefs>
						<descriptorRef>jar-with-dependencies</descriptorRef>
					</descriptorRefs>
					<archive>
						<manifest>
							<mainClass>${mainClass}</mainClass>
						</manifest>
					</archive>
				</configuration>
				<executions>
					<execution>
						<id>make-assembly</id> <!-- this is used for inheritance merges -->
						<phase>package</phase> <!-- bind to the packaging phase -->
						<goals>
							<goal>single</goal>
						</goals>
					</execution>
				</executions>
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

			<!-- plugin>
				<artifactId>maven-antrun-plugin</artifactId>
				<version>1.6</version>
				<executions>
					<execution>
						<id>deploy to public</id>
						<phase>verify</phase>
						<configuration>
							<target>
								<copy file="${selfContained.jar}"
									tofile="${publicDeploy.jar}"
									overwrite="true"/>
								<chmod file="${publicDeploy.jar}" perm="755"/>
								<echo message="changed '${publicDeploy.jar}' permissions to 755"/>
							</target>
						</configuration>
						<goals>
							<goal>run</goal>
						</goals>
					</execution>
				
					<execution>
						<id>install shortcut script</id>
						<phase>install</phase>
						<configuration>
							<target>
								<echo message="creating shortcut script '${script.file}'"/>
								<echo file="${script.file}">#!/bin/bash 
java -jar ${selfContained.jar} "$@"
								</echo>
								<chmod file="${script.file}" perm="755"/>
								<echo message="changed '${script.file}' permissions to 755"/>
							</target>
						</configuration>
						<goals>
							<goal>run</goal>
						</goals>
					</execution>
				</executions>
			</plugin -->
		</plugins>
	</build>
</project>""")
pom.close()


# //////////////////	Create directory structure	//////////////////
# ==================================================================

os.mkdir("src")
os.mkdir("src/main")
os.mkdir("src/main/scala")
os.mkdir("src/main/resources")
os.mkdir("src/test")
os.mkdir("src/test/scala")

pkgs = pgroup.split(".")
pDir = ""
for pkg in pkgs:
	pDir = "%s/%s" % (pDir, pkg) 
	os.mkdir("src/main/scala%s" % pDir)
	os.mkdir("src/test/scala%s" % pDir)



# //////////////////	Main scala source file	//////////////////
# ==============================================================

mainSrc = open("src/main/scala%s/%s.scala" % (pDir, pCamelName), "w")
mainSrc.write("""/*
 * %s
 *	Copyright (C) 2014 Johan Teleman
 */
package %s

import java.util.Properties
""" % (pCamelName, pgroup))

if useGUI:
	mainSrc.write("""
import swing._
import swing.event._
import se.strawbrary.swing.SwingApplication

object %s extends SwingApplication {

	val properties = new Properties
	properties.load(this.getClass.getResourceAsStream("/pom.properties"))

	override def main(args:Array[String]):Unit = {
		
		super.main(args)
	}

	def top = new MainFrame {
		title = properties.getProperty("pom.name") + " " + properties.getProperty("pom.version")
		contents = new BoxPanel {
			contents += new Label("Hello, world! said "+
							properties.getProperty("pom.name")+" "+
							properties.getProperty("pom.version"))
		}
	}	
}
""" % (pCamelName))

else:
	mainSrc.write("""
import se.strawbrary.Application

object %s extends Application {

	val properties = new Properties
	properties.load(this.getClass.getResourceAsStream("/pom.properties"))

	def main(args:Array[String]):Unit = {
		println("Hello, world! said "+
							properties.getProperty("pom.name")+" "+
							properties.getProperty("pom.version"))
	}
}
""" % (pCamelName))
mainSrc.close()



# //////////////////	Properties file	//////////////////
# ======================================================

props = open("src/main/resources/pom.properties", "w")
props.write("pom.name=${pom.name}\npom.version=${pom.version}\n")
props.close()



# //////////////////	Git 	//////////////////
# ============================================

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
