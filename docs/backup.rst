Backup and Restoration
======================

Always take precautions. Backup your data as you'll never know when you'll need to restore it.

Backup
------

It is strongly advised that you backup your agents to protect you in the event of catastrophe.

The following directories need to be saved periodically.

#. The ``PATTOO_CONFIGDIR`` directory which contains your configuration
#. The ``daemon_directory`` location defined in your configuration. This area stores important authentication information.
#. The ``pattoo`` directory which contains your source code.

We'll discuss data restoration next.

Restoration
-----------

It's important to follow these steps in this order when restoring ``pattoo`` after a disaster.

#. FIRST make sure all the ``pattoo`` agents are stopped.
#. SECOND restore the contents of the ``daemon_directory`` location defined in your configuration. This area stores important authentication information.
#. Restore the ``PATTOO_CONFIGDIR`` directory which contains your configuration
#. Restore the ``pattoo`` directory which contains your source code.

You should now be able to restart your agents without issue.
