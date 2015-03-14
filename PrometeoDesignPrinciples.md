# Introduction #

This page describes the design principles used in the Prometeo ERP development process.


# Details #

## Repository conventions ##

The Prometeo ERP project uses GIT as its reference versioning system. The structure of the repository follow the model described in this page:

http://nvie.com/posts/a-successful-git-branching-model

Basically there are two remote branches (hosted by Google Code):

  * _origin/master_
  * _origin/develop_

The _origin/master_ branch contains the last stable release (if any), while the _origin/develop_ contains the current development code.

The new code is always pushed to the _origin/develop_. New big features are coded in feature-specific (local) branches and merged to the remote _origin/develop_ branch.

As convention, we named all feature-specific (local) branches adding a **feature-** prefix to the name of the branch (i.e: _feature-improved-crm_, _feature-new-ui_, etc.)

## Business model ##

_**NOTE:** This part is fully a TODO, it doesn't reflect the current Prometeo ERP architecture._

Prometeo ERP is based on a unified business model inspired by the _ERP5_'s one:

  * http://www.erp5.org/UnifiedBusinessModel
  * http://en.wikibooks.org/wiki/ERP5_Handbook/Getting_Started#Five_classes_-_introduction

All the Prometeo ERP business applications are built using one or more of these **six** concepts:

  1. **Node**
  1. **Resource**
  1. **Item**
  1. **Path**
  1. **Movement**
  1. **State**