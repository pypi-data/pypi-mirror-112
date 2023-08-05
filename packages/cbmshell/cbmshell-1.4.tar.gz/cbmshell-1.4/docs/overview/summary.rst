.. _pypi: https://pypi.org/

Install the Python ``cbmshell`` package from pypi_ using:

.. code-block:: shell

    $ pip install cbmshell

Start an interactive session by running:

.. code-block:: shell

    $ cbm-shell
    (cbm)

Commands entered following the ``(cbm)`` prompt will be immediately
executed. To see a list of supported commands use ``help``:

.. code-block:: text

    (cbm) help
  
    Documented commands (use 'help -v' for verbose/'help <topic>' for details):
    ===========================================================================
    alias   delete     file     list   quit          shell      unlock
    attach  detach     help     lock   run_pyscript  shortcuts
    cat     directory  history  macro  run_script    token_set
    copy    edit       images   mkdir  set           unlist

Disk images are made available by attaching them to a drive number:

.. code-block:: text

    (cbm) attach mydisk.d64 
    Attached mydisk.d64 to 0

Many commands can work with either a file on the local filesystem:

.. code-block:: text

    (cbm) list test.prg

or a file inside an image:

.. code-block:: text

    (cbm) list 0:PRINT

or a combination of both:

.. code-block:: text

    (cbm) copy 0:TEST test.prg
