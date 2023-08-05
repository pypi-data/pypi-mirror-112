======================================
External Commands & Output Redirection
======================================

Commands can be run without leaving ``cbm-shell`` by using the ``!``
shortcut:

.. code-block:: text

    (cbm) !uptime
     11:47:39 up  4:43,  4 users,  load average: 0.78, 0.92, 1.30

The output from internal commands can be redirected to a file in the
local filesystem:

.. code-block:: text

    (cbm) directory >out

The output may also be piped to an external command:

.. code-block:: text

    (cbm) list 0:PRINT | grep OPEN
    11 OPEN4,4,SA
    15 OPEN2,8,2,F$+",S,R"

To pipe the raw contents of a file use the ``cat`` command:

.. code-block:: text

    (cbm) cat 0:FNKEY | dxa
            .word $0c00
            * = $0c00
    
    lc00    sei
            lda $0314
            sta $0337
            lda $0315
            sta $0338
