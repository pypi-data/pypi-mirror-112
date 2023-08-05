Managing Images
===============

For ``cbm-shell`` to be able to access the contents of an image it
must be associated with a drive number. That is done by attaching the
image:

.. code-block:: text

    (cbm) attach mydisk.d64 
    Attached mydisk.d64 to 0

Up to ten images may be attached at any one time.

To prevent modifications to an image it may be attached read-only

.. code-block:: text

    (cbm) attach --read-only mydisk.d64 

When an image is no longer required it may be detached:

.. code-block:: text

    (cbm) detach 0
    Detached D64Image(mydisk.d64)

The list of currently attached images can be displayed using the
``images`` command:

.. code-block:: text

    (cbm) images
        0  RW  D64Image(mydisk.d64)


Creating New Images
-------------------

New disk images should be created using the ``d64-format`` console
script that is included in the ``d64`` module.

A new tape image can be created by attaching a non-existent file.


Subdirectories
--------------

Images from 1581 drives (.d81) may contain nested filesystems called
subdirectories. These may be attached after the parent image has been
attached by using the drive number and entry name:

.. code-block:: text

    (cbm) attach 0:SUBDIR
    Attached ImagePath(0:b'SUBDIR') to 1

The subdirectory can then be addressed in the same way as an image,
including attaching any nested subdirectories.
