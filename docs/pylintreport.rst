
::

	************* Module anchorman.configuration
	C: 10, 0: Line too long (85/80) (line-too-long)
	C: 13, 0: Line too long (86/80) (line-too-long)
	************* Module anchorman.main
	C: 38, 0: Line too long (112/80) (line-too-long)
	W:  8, 0: Dangerous default value [] as argument (dangerous-default-value)
	************* Module anchorman.utils
	C: 14, 0: Line too long (121/80) (line-too-long)
	C: 17, 0: Final newline missing (missing-final-newline)
	************* Module anchorman.generator.candidate
	C: 97, 0: Line too long (82/80) (line-too-long)
	C:  5, 0: Empty function docstring (empty-docstring)
	R: 12, 0: Too many local variables (18/15) (too-many-locals)
	************* Module anchorman.generator.text
	C:  7, 4: Invalid variable name "x" (invalid-name)
	************* Module anchorman.positioner.interval
	C:  6, 0: Invalid argument name "t" (invalid-name)
	
	
	
Report
======
184 statements analysed.

Statistics by type
------------------

+---------+-------+-----------+-----------+------------+---------+
|type     |number |old number |difference |%documented |%badname |
+=========+=======+===========+===========+============+=========+
|module   |13     |13         |=          |30.77       |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|class    |0      |0          |=          |0           |0        |
+---------+-------+-----------+-----------+------------+---------+
|method   |0      |0          |=          |0           |0        |
+---------+-------+-----------+-----------+------------+---------+
|function |18     |17         |+1.00      |94.44       |0.00     |
+---------+-------+-----------+-----------+------------+---------+



External dependencies
---------------------
::

    anchorman 
      \-configuration (anchorman.main)
      \-generator 
      | \-candidate (anchorman.main)
      | \-element (anchorman.generator.candidate)
      | \-highlight (anchorman.generator.element)
      | \-tag (anchorman.generator.element)
      | \-text (anchorman.main)
      \-positioner 
        \-interval (anchorman.main)
    bs4 (anchorman.generator.tag,anchorman.positioner.slices)
    intervaltree (anchorman.positioner.interval)
    yaml (anchorman.configuration)



Raw metrics
-----------

+----------+-------+------+---------+-----------+
|type      |number |%     |previous |difference |
+==========+=======+======+=========+===========+
|code      |200    |50.38 |188      |+12.00     |
+----------+-------+------+---------+-----------+
|docstring |54     |13.60 |57       |-3.00      |
+----------+-------+------+---------+-----------+
|comment   |41     |10.33 |72       |-31.00     |
+----------+-------+------+---------+-----------+
|empty     |102    |25.69 |108      |-6.00      |
+----------+-------+------+---------+-----------+



Duplication
-----------

+-------------------------+------+---------+-----------+
|                         |now   |previous |difference |
+=========================+======+=========+===========+
|nb duplicated lines      |0     |0        |=          |
+-------------------------+------+---------+-----------+
|percent duplicated lines |0.000 |0.000    |=          |
+-------------------------+------+---------+-----------+



Messages by category
--------------------

+-----------+-------+---------+-----------+
|type       |number |previous |difference |
+===========+=======+=========+===========+
|convention |9      |10       |-1.00      |
+-----------+-------+---------+-----------+
|refactor   |1      |1        |=          |
+-----------+-------+---------+-----------+
|warning    |1      |1        |=          |
+-----------+-------+---------+-----------+
|error      |0      |0        |=          |
+-----------+-------+---------+-----------+



% errors / warnings by module
-----------------------------

+------------------------------+------+--------+---------+-----------+
|module                        |error |warning |refactor |convention |
+==============================+======+========+=========+===========+
|anchorman.main                |0.00  |100.00  |0.00     |11.11      |
+------------------------------+------+--------+---------+-----------+
|anchorman.generator.candidate |0.00  |0.00    |100.00   |22.22      |
+------------------------------+------+--------+---------+-----------+
|anchorman.utils               |0.00  |0.00    |0.00     |22.22      |
+------------------------------+------+--------+---------+-----------+
|anchorman.configuration       |0.00  |0.00    |0.00     |22.22      |
+------------------------------+------+--------+---------+-----------+
|anchorman.positioner.interval |0.00  |0.00    |0.00     |11.11      |
+------------------------------+------+--------+---------+-----------+
|anchorman.generator.text      |0.00  |0.00    |0.00     |11.11      |
+------------------------------+------+--------+---------+-----------+



Messages
--------

+------------------------+------------+
|message id              |occurrences |
+========================+============+
|line-too-long           |5           |
+------------------------+------------+
|invalid-name            |2           |
+------------------------+------------+
|too-many-locals         |1           |
+------------------------+------------+
|missing-final-newline   |1           |
+------------------------+------------+
|empty-docstring         |1           |
+------------------------+------------+
|dangerous-default-value |1           |
+------------------------+------------+



Global evaluation
-----------------
Your code has been rated at 9.40/10 (previous run: 9.31/10, +0.09)

