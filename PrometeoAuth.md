# Introduction #

This page describes the authentication system used in Prometeo ERP.


# Details #

Authentication management in Prometeo ERP is based on four models:

  * **User**
  * **Group**
  * **Permission**
  * **ObjectPermission**

The first three models are the Django's default ones, so you can read more info about these at:

https://docs.djangoproject.com/en/dev/topics/auth/

The important addition to the Prometeo ERP's authentication system is the last model, called **ObjectPermission**.

This new model allows you to associate row-level permissions to one or more users/groups.

# Object Permissions #

An **ObjectPermission** instance contains two fields:

  * A reference to a default **Permission** instance.
  * An **ID** used to reference an instance of the model related to the **Permission**.