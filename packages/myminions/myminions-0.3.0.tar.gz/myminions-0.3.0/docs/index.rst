.. isisysvic3daccess documentation master file, created by
   sphinx-quickstart on Fri Sep 25 10:54:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============================
Documentation of myminions's
============================

*- by David Scheliga*

**My minions** is a loose collection of frequently used methods doing basic
bidding's.

.. image:: ../myminions_icon.png
   :height: 192px
   :width: 192px
   :alt: 3 minions
   :align: center

Indices and tables
==================

* :ref:`genindex`

Installation
============

Either install the current release from pip ...

.. code-block:: shell

   pip install myminions

... or the latest *dev*elopment state of the gitlab repository.

.. code-block:: shell

   $ pip install git+https://gitlab.com/david.scheliga/myminions.git@dev --upgrade

Module content
==============

.. py:currentmodule:: myminions

Helper for docopt
-----------------

You find a great example making a cli like git at the `docopt git example`_. This
example splits the commands into separate files. It can also be emulated by
using the :func:`myminions.docopt_parsable` within a single file.

.. _docopt git example: https://github.com/docopt/docopt/tree/master/examples/git

.. autofunction:: myminions.docopt_parsable

.. code-block:: python

   @docopt_parsable
   def command_plus(argv):
       """
       USAGE:
           mymodule (p|plus) [-d] [<args>..]

       Does something positive.

       OPTIONS:
           -d, --deep     Go deep.
       """
       pass
       # do something here


   @docopt_parsable
   def command_plus(argv):
       """
       USAGE:
           mymodule (m|minus) [-r] [<args>..]

       Does something negative.

       OPTIONS:
           -r, --repeat     Repeat it.
       """
       pass
       # do something here


   def main(argv):
       """
       USAGE:
           mymodule [-h|--help] [--version] <command> [<args>...]

       The most commonly use of mymodule commands are:
           p, plus

       See '`mymodule` help <command>' for more information on a specific command.

       """
       try:
           args = docopt(
               main.__doc__,
               argv=argv,
               version="mymodule version " + __version__,
               options_first=True,
           )
       except DocoptExit:
           exit(main.__doc__)

       plus_commands = ["p", "plus"]

       argv = [args["<command>"]] + args["<args>"]
       command = args["<command>"]
       if command in plus_commands:
           do_plus(argv)
       elif command in minus_commands:
           do_minus(argv)
       else:
           exit("'{}' is not a mymodule command. See 'mymodule help'.".format(command))


   if __name__ == "__main__":
       import sys

       arguments_via_pipe = []

       standard_in_pipe_was_not_empty = not sys.stdin.isatty()
       if standard_in_pipe_was_not_empty:
           input_stream = sys.stdin
           assert isinstance(
               input_stream, io.TextIOWrapper
           ), "The stream input was not a text file."
           arguments_via_pipe = [arg for arg in input_stream.read().split("\n")]

       commandline_arguments_and_pipe_content = sys.argv[1:] + arguments_via_pipe

       main(commandline_arguments_and_pipe_content)


For getting the piped arguments.

.. autofunction:: myminions.get_piped_command_line_arguments

Usage of *get_piped_command_line_arguments*:

.. code-block:: python

   if __main__ == "__main__":
       import sys
       sys_argv_and_pipe_content = get_piped_command_line_arguments(sys.argv[1:])
       main(sys_argv_and_pipe_content)


Helper for doctest
------------------

I prefer doctests. To make path related doctests happen both on Linux and Windows
these methods comes in handy.

.. autofunction:: myminions.repr_posix_path

.. autofunction:: myminions.strip_for_doctest


Removing something
------------------

.. autofunction:: myminions.remove_path_or_tree


Saving stuff on Linux and on Windows
------------------------------------
On one occasion changing, editing a text file in between Linux and Windows broke
the parsing with `json` and `yaml`. Originated from the module `dicthandling`
:func:`try_deconding_potential_text_content` is moved to `myminions`.

.. autofunction:: myminions.try_decoding_potential_text_content

.. autofunction:: myminions.load_yaml_file_content

.. autofunction:: myminions.update_yaml_file_content
