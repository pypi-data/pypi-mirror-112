Installing
----------

.. code-block:: bash

  pip3 install flagopt

Battleship
----------

.. code-block:: python

  import flagopt

  usage = '-x [spot] -y [spot]'

  flags = flagopt.trace(usage)

  content = '-x C -y 7'

  args = flagopt.snip(flags, content)

  print('hit at', args['-x'], args['-y'])

Actions
-------

.. code-block:: python

  import flagopt

  flags = {
    '-move': {
      '-x': 'distance',
      '-y': 'distance'
    },
    '-craft': 'recipe',
    '-scavenge': {
      '-target': 'resource',
      '-finish': {
        '-time': 'hours',
        '-time': 'amount'
      }
    },
    '-rest': 'hours',
    '-target': 'human | animal'
  }

  # show how to use this
  usage = flagopt.draw(flags)

  content = (
    # move right linearly
    '-move -x 10 '
    # then move diagonally right and down;
    # no need to explicitly pass the first flag (-x)
    '-move 5 -y -5 '
    # backslash is used as an escape character;
    # -target will be ignored during the first parse scan
    # and the backslash will be removed so that -target can
    # be considered during the next scan for -scavenge;
    # multiple backslashes can be used to achieve other
    # amounts of iterations for this effect
    '-scavenge \-target wood '
    # arguments can be passed multiple times (-time);
    # scavenge for 3 hours and 60 more wood after that
    '-finish -time 3 -limit 60 '
    # or until 5 hours have passed
    '-finish -time 5'
    # rest for 4 hours, craft a tent, rest for another 3;
    # there is no space between 5 and -rest (line above);
    # spaces do not matter for flags and are stripped away
    # unless there is an escape character before / after
    '-rest 4      '
    # you can pass empty flags,
    # their presence is indicated with an empty string
    '--debug '
    # im bad at coming up with examples
    '-craft spear '
    # especially when they involve games
    '-target rabbit '
    # time to sleep now
    '-rest 3'
  )

  args = flagopt.snip(flags, content)

  moves = args.getall('-move')

  print(moves)


Links
-----

- `Documentation <https://flagopt.readthedocs.io>`_
