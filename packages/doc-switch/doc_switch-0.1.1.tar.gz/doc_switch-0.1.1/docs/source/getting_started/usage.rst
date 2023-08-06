=====
Usage
=====

Switching Documentation Formats
-------------------------------

To switch documentation formats, just use the following command:

.. code-block:: bash

    $ ds <input> --output=[output] --input-format=sphinx --output-format=google

In this command, ``<input>`` is the input file name and ``[output]`` is the
output file name. If ``[output]`` is not specified, it defaults to
``<input>-<format>.py``. In other words, if you pass a file called ``foo.py``
as the input file and let the ``--output-format`` option be ``google``, it will
output a file named ``foo-google.py``.

The option ``--input-format`` is optional, and if not passed, DocSwitch will
make a guess as to which format it is. For example, the following function:

.. code-block:: py

    def function(number):
        """Returns ``number`` + ``42``

        :param number int: The number used to process
        :returns: The resulting number
        :rtype: int
        """

        return number + 42

Will result in DocSwitch guessing the format to be ``sphinx``. It is
recommended to always include the input format, in case DocSwitch guesses
wrong and the file becomes disastrous.
