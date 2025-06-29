# Dynamic Doc SH

A dynamic documentation generator for shell scripts using inline tags, inspired by Swagger's approach to API documentation.

## Overview

When writing shell scripts, documenting them properly can be tedious and often gets overlooked. Dynamic Doc SH solves this problem by allowing you to embed documentation tags directly in your shell scripts, then automatically generating clean, readable Markdown documentation.

Similar to how Swagger generates API documentation from code annotations, this tool parses special tags in your shell scripts and creates comprehensive documentation that stays in sync with your code.

## Features

 - 🏷️ Tag-based Documentation: Use simple tags to mark functions, variables, and script sections
 - 📝 Automatic Markdown Generation: Generates clean .md files from your tagged shell scripts
 - 🔄 Dynamic Updates: Documentation stays current with your code changes
 - 🎯 Multiple Tag Types: Support for different documentation elements
 - 📋 Template Generation: Creates consistent documentation structure

## How It Works

Add Tags: Place documentation tags directly above the code elements you want to document
Run Generator: Execute the script to parse your shell files
Get Documentation: Clean Markdown documentation is generated/updated automatically

