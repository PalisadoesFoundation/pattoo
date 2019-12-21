How To Contribute
=================

Below is the workflow for having your contribution accepted into the ``pattoo`` repository.


#. Create an Issue or comment on an existing issue to discuss the feature
#. If the feature is approved, assign the issue to yourself
#. Fork the project
#. Clone the fork to your local machine
#. Run ``make setup`` to install dependencies to virtualenv (information about virtualenv found further below in this doc)
#. Add the original project as a remote (git remote add upstream https://github.com/PalisadoesFoundation/pattoo, check with: git remote -v)
#. Create a topic branch for your change (git checkout -b ``BranchName``\ )
#. you may create additional branches if modifying multiple parts of the code
#. Write code and Commit your changes locally. Example proper git commit message below:

.. code-block::

    Make the example in CONTRIBUTING imperative and concrete ...

    Without this patch applied the example commit message in the CONTRIBUTING
    document is not a concrete example.  This is a problem because the
    contributor is left to imagine what the commit message should look like
    based on a description rather than an example.  This patch fixes the
    problem by making the example concrete and imperative.

    The first line is a real life imperative statement with a ticket number
    from our issue tracker.  The body describes the behavior without the patch,
    why this is a problem, and how the patch fixes the problem when applied.

    Resolves Issue: #123
    See also: #456, #789



#. When you need to synch with upstream (pull the latest changes from main repo into your current branch), do: git fetch upstream -> -> git merge upstream/master. (or run ``make synch`` to let the projects makefile handle synching)
#. Check for uneccesary whitespace with ``git diff --check``.
#. Write the necessary unit tests for your changes.
#. Run all the tests to assure nothing else was accidentally broken (run: ``make test``\ )
#. Push your changes to your forked repository (git push origin ``branch``\ )
#. Perform a pull request on GitHub
#. Your code will be reviewed
#. If your code passes review, your pull request will be accepted

The ``make contribute`` command encapsulates steps 8 to 12 when you are ready to make a pull request.
The ``make synch`` command will synch your repository

Code Style Guide
================

For ease of readability and maintainability ``pattoo`` code must follow thse guidelines.
Code that does not comply will not be added to the ``master`` branch.


#. ``pattoo`` uses the Google Python Style Guide for general style requirements
#. ``pattoo`` uses the The Chromium Projects Python Style Guidelines for docstrings.
#. Indentations must be multiples of 4 blank spaces. No tabs.
#. All strings must be enclosed in single quotes
#. In addition too being pylint compliant, the code must be PEP8 and PEP257 compliant too.
#. There should be no trailing spaces in files

Guidelines to remember
----------------------


* Always opt for the most pythonic solution to a problem
* Avoid applying idioms from other programming languages
* Import each module with its full path name. ie: from pack.subpack import module
* Use exceptions where appropriate ( https://google.github.io/styleguide/pyguide.html#Exceptions )
* Use doc strings ( http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html )
* Try not to have returns at multiple points in a function unless they are failure state returns
* If you are in the middle of a development session and have to interrupt your work, it is a good idea to write a broken unit test about what you want to develop next. When coming back to work, you will have a pointer to where you were and get back on track faster.

Commits
-------

``pattoo`` strives to maintain a proper log of development through well structured git commits.
The link below offer insight and advice on the topic of commit messages:
https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message
http://chris.beams.io/posts/git-commit/

PEP8 and PEP257 Compliance
--------------------------

You can verify your code for compliance using running the ``make lint`` command from the project root.

VirtualEnv
----------

``virtualenv`` is a tool to create isolated Python environments.
It creates an environment that has its own installation directories,
that doesn’t share libraries with other virtualenv environments nor does it access the globally installed libraries either.

The ``pattoo`` project's makefile wil automatically set up a makefile for you once you have virutalenv installed globally.
All dependencies that ``pattoo`` requires, aside from pip and virtualenv itself, will be installed to this virtual env.
The makefile will run commands such as ``nosetests`` from the virtual env. If you wish to run these commands manually,
run them as ``venv/bin/nosetests`` as they would not have been installed to your machine globally.

Makefile
--------

This project contains a makefile which contains a list of utilities that can be run using the ``make command`` command.
The list of commands is:


* dependencies - install project dependencies
* setup - same as dependencies, exists for convention
* lint - run pep8 pep257 and pylint on the project. (these can be run individually aswell, ie ``make pep8``\ )
* test - run nosetests
* develop - create pattoo executable in /venv/bin/pattoo and /bin/pattoo
* clean - remove all files and directories created by any other make command(ie venv)
* synch - Pull down updates from the master branch of official repo into current branch of forked repo
* contribute - Set up repository for making pull request

Sample .vimrc File for Compliance
---------------------------------

You can use this sample .vimrc file to help meet our style requirements

.. code-block::

   " Activate syntax
   syntax on
   " set number

   " Disable automatic comment insertion
   autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

   " Delete trailing whitespace
   autocmd BufWritePre * :%s/\s\+$//e

   " Convert tabs to spaces
   set expandtab

   " Set tabs to 4 spaces
   set tabstop=4

   " Set the number of spaces for indentation
   set shiftwidth=4

   " Switch on highlighting the last used search pattern when the terminal has colors
   if &t_Co > 2 || has("gui_running")
     set hlsearch
   endif

   " Tell vim to remember certain things when we exit
   "  '10  :  marks will be remembered for up to 10 previously edited files
   "  "100 :  will save up to 100 lines for each register
   "  :20  :  up to 20 lines of command-line history will be remembered
   "  %    :  saves and restores the buffer list
   "  n... :  where to save the viminfo files
   set viminfo='10,\"100,:20,%,n~/.viminfo

   " Function for viminfo to work
   function! ResCur()
     if line("'\"") <= line("$")
       normal! g`"
       return 1
     endif
   endfunction

   " Function for viminfo to work
   augroup resCur
     autocmd!
     autocmd BufWinEnter * call ResCur()
   augroup END
