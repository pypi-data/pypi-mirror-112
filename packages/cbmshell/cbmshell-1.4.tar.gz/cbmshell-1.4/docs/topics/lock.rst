==============================
Protecting Files From Deletion
==============================

DOS supports a flag to prevent deleting a file with the SCRATCH
command but does not provide a mechanism to set it.

A file in a disk image can be protected using the ``lock`` command:

.. code-block:: text

    (cbm) lock 0:IMPORTANT
    Locking ImagePath(0:b'IMPORTANT')

Similarly the protection can be cleared with the ``unlock`` command:

.. code-block:: text

    (cbm) unlock 0:IMPORTANT
    Unlocking ImagePath(0:b'IMPORTANT')

.. warning::
    Locking a file does not prevent it from being deleted by
    ``cbmshell``.
