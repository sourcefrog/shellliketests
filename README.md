Shell-like tests
================

Licence: GNU GPL v2+
Home page: https://github.com/sourcefrog/shelliketests
Maintainer: Martin Pool <mbp@sourcefrog.net>

`shellliketests` allows users to write tests in a syntax very close to a
shell session, using a restricted and limited set of commands that should
be enough to mimic most of the behaviours.

Features and benefits:

* Provides a concise way to run commands and check output.

* Commands can either be really run as subprocesses, or selectively
  intercepted and run in-process (eg by calling something like the `main`
  routine of a Python program).  Running in process may be substantially
  faster and can allow more precise control of the test environment.

* Abstracts cross-platform differences: for example `rm` can be used
  across Windows and Unix.

Shell-like tests don't cover every kind of test you should write, but they
do make one class of tests easier.

A script is a set of commands, each command is composed of:

* one mandatory command line,
* one optional set of input lines to feed the command,
* one optional set of output expected lines,
* one optional set of error expected lines.

Input, output and error lines can be specified in any order.

Except for the expected output, all lines start with a special
string (based on their origin when used under a Unix shell):

* '$ ' for the command,
* '<' for input,
* nothing for output,
* '2>' for errors,

Comments can be added anywhere, they start with '#' and end with
the line.

The execution stops as soon as an expected output or an expected error is not
matched.

If output occurs and no output is expected, the execution stops and the
test fails.  If unexpected output occurs on the standard error, then
execution stops and the test fails.

If an error occurs and no expected error is specified, the execution stops.

An error is defined by a returned status different from zero, not by the
presence of text on the error stream.

The matching is done on a full string comparison basis unless `...` is used, in
which case expected output/errors can be less precise.

Examples:

The following will succeeds only if 'bzr add' outputs 'adding file':

    $ bzr add file
    >adding file

If you want the command to succeed for any output, just use:

    $ bzr add file
    ...
    2>...

or use the `--quiet` option:

    $ bzr add -q file

The following will stop with an error:

    $ bzr not-a-command

If you want it to succeed, use:

    $ bzr not-a-command
    2> bzr: ERROR: unknown command "not-a-command"

You can use ellipsis (...) to replace any piece of text you don't want to be
matched exactly:

    $ bzr branch not-a-branch
    2>bzr: ERROR: Not a branch...not-a-branch/".

This can be used to ignore entire lines too:

    $ cat
    <first line
    <second line
    <third line
    # And here we explain that surprising fourth line
    <fourth line
    <last line
    >first line
    >...
    >last line

You can check the content of a file with cat:

    $ cat <file
    >expected content

You can also check the existence of a file with cat, the following will fail if
the file doesn't exist:

    $ cat file

The actual use of ScriptRunner within a TestCase looks something like
this:

    from bzrlib.tests import script

    def test_unshelve_keep(self):
        # some setup here
        script.run_script(self, '''
            $ bzr add -q file
            $ bzr shelve -q --all -m Foo
            $ bzr shelve --list
            1: Foo
            $ bzr unshelve -q --keep
            $ bzr shelve --list
            1: Foo
            $ cat file
            contents of file
            ''')

You can also test commands that read user interaction:

    def test_confirm_action(self):
        """You can write tests that demonstrate user confirmation"""
        commands.builtin_command_registry.register(cmd_test_confirm)
        self.addCleanup(commands.builtin_command_registry.remove, 'test-confirm')
        self.run_script("""
            $ bzr test-confirm
            2>Really do it? [y/n]: 
            <yes
            yes
            """)

To avoid having to specify `...` for all commands whose output is
irrelevant, the `run_script()` method may be passed the keyword argument
`null_output_matches_anything=True`.  For example:

    def test_ignoring_null_output(self):
        self.run_script("""
            $ bzr init
            $ bzr ci -m 'first revision' --unchanged
            $ bzr log --line
            1: ...
            """, null_output_matches_anything=True)

Authors
-------

This code is based on the `bzrlib.tests.script` module in
[Bazaar](http://bazaar.canonical.com/), developed by Canonical Ltd and
written by:

* Vincent Ladieul
* Martin Pool
* Robert Collins
* John Arbash Meinel
* Martin gz
