#!/usr/bin/python

import os
import subprocess
import sys
import shutil
from xml.dom import minidom, Node

NAME = "Release"
VERSION = "0.0.1"

print
print NAME, VERSION
print "="*(len(NAME) + len(VERSION) + 1)
print

shutil.copyfile("pom.xml", "pom.xml.BAK")
doc = minidom.parse("pom.xml")
root = doc.documentElement

def byPath(p, start=root):
	tags = p.split(".")
#	print "tags: ", tags
	elem = start
	for tag in tags:
		elems = elem.getElementsByTagName(tag)
		if len(elems) == 0:
			print "oooops!"
		else:
			elem = elems[0]
	return elem

def getByPath(p, start=root):
	elem = byPath(p, start)
	return "".join([child.nodeValue for child in elem.childNodes])

def setByPath(p, str, start=root):
	elem = byPath(p, start)
	elem.childNodes = [doc.createTextNode(str)]

def realChilds(node):
	es = []
	for c in node.childNodes:
		if c.nodeType == Node.ELEMENT_NODE:
			es.append(c)
	return es

def restore():
	subprocess.call(["git", "tag", "-d", newVersion])
	shutil.move("pom.xml.BAK", "pom.xml")

def call_restore(ls):
	ret = subprocess.call(ls)
	if ret != 0:
		print "Failed calling '%s'" % (" ".join(ls))
		restore()
		sys.exit(1)

devCon 	= getByPath("scm.developerConnection")
artId 	= getByPath("artifactId")
version = getByPath("version")

print "artifact ID:", artId
print "version:", version 

##############################################

hasSnapshotDeps = False
deps = byPath("dependencies")
for child in realChilds(deps):
	depVer = getByPath("version", child)
	if depVer.find("SNAPSHOT") >= 0:
		print " %s:%s:%s is a SNAPSHOT" % (getByPath("groupId", child), getByPath("artifactId", child), depVer)
		hasSnapshotDeps = True

if hasSnapshotDeps:
	print "Project has snapshot dependencies, exiting."
	sys.exit(1)

##############################################

p1 = subprocess.Popen(["git", "status"], stdout=subprocess.PIPE)
ret, err = p1.communicate()
if ret.find("Changes to be commited:") >= 0:
	print "There are uncommited changes..."
	print ret
	print " ... exiting ..."
	sys.exit(1)

##############################################

newVersion = raw_input("new version (%s): " % version[:-9])
if newVersion == "":
	newVersion = version[:-9]

print "new version is", newVersion

setByPath("version", newVersion)

##############################################

gitTag = raw_input("git tag (%s): " % newVersion)
if gitTag == "":
	gitTag = newVersion

print "git tag is", gitTag

##############################################

pom = open("pom.xml", "w")
root.writexml(pom)
pom.close()

##############################################

call_restore(["mvn", "test"])

# TODO: check mvn test is successful

##############################################

call_restore(["git", "add", "pom.xml", ".gitignore"])
call_restore(["git", "commit", "-m", '"version %s"'%gitTag])
call_restore(["git", "tag", gitTag])
#call_restore(["git", "push", "origin", "master"])

##############################################

call_restore(["mvn", "install"])

##############################################

s = newVersion.split(".")
minor = int(s[-1])
print "MINOR::: %d" % minor 
nextSnapshotDefault = ".".join( s[:-1] + [str(minor+1)] ) + "-SNAPSHOT"

nextSnapshot = raw_input("next snapshot (%s): " % nextSnapshotDefault)
if nextSnapshot == "":
	nextSnapshot = nextSnapshotDefault

print "next snapshot is", nextSnapshot

setByPath("version", nextSnapshot)

##############################################

pom = open("pom.xml", "w")
root.writexml(pom)
pom.close()

##############################################

call_restore(["git", "add", "pom.xml"])
call_restore(["git", "commit", "-m", nextSnapshot])

##############################################

os.remove("pom.xml.BAK")
