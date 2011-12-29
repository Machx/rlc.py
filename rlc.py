#!/usr/bin/python

#############################################################
# rlc.py
# a Clone of wc -l in Python aimed at counting lines of code
# in C, Objective-C, C++ and header files
# Copyright (c) 11/12/2008 Colin Wheeler
#
# Changes by Vincent Esche (03|02|09):
# 1. Added count of actual code lines of code per file and total to log output
#    (ignoring c-style "/*...*/" & "//" comments and syntactically empty lines)
# 2. Added support for file exclusion via blacklist (regex patterns)
# 3. Added file count to log output
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Thanks to Dan Weeks and Mark Hughes for help in simplifying the code
#############################################################

import re
import os
import sys

# for customizations scroll to very bottom of code

def linecount(filename):
	total_lines = len(open(filename).readlines())
	
	file_content = open(filename).read()
	code_content = file_content
	
	#remove c-style "//" single-line comments
	code_content = re.sub("//[^\n\r]+", "", code_content)
	#remove c-style "/**/" multi-line comments
	code_content = re.sub("[\s\n\r]*/*/\*(.|\r\n)*?\*/[\s\n\r]*", "\n", code_content)
	#remove empty lines
	code_content = re.sub("[\n\t\s]*(?=\n)", "", code_content)
	code_lines = len(re.findall("[\n\r]+", code_content))
	
	print "%s" % (filename[len(os.getcwd()):len(filename) + 1])
	print "\tTotal Lines: %6d" % (total_lines)
	print "\t Code Lines: %6d" % (code_lines)
	
	return (total_lines, code_lines)

def main():
	global extensions, ignore_patterns
	grand_total = 0
	code_total = 0
	files_total = 0
	path = os.getcwd()
	
	for root, dirs, files in os.walk(path, topdown=True):
		for filename in files:
			if os.path.splitext(filename)[-1] in extensions:
				valid_file = True
				for ignore in ignore_patterns:
					if re.search(ignore, os.path.join(root, filename)) != None:
						valid_file = False
						break
				if valid_file:
					file_results = linecount(os.path.join(root, filename))
					grand_total += file_results[0]
					code_total  += file_results[1]
					files_total += 1
	print "Grand Total Lines: %6d" % grand_total
	print " Total Code Lines: %6d" % code_total
	print " Total Code Files: %6d" % files_total

if __name__ == "__main__":
	extensions = ['.c', '.pch', '.m', '.h', '.mm', '.cpp', '.java']
	ignore_patterns = ['/build/']
	main()