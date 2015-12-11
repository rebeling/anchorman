
::

	************* Module anchorman.configure
	C: 10, 0: Line too long (83/80) (line-too-long)
	C: 13, 0: Line too long (84/80) (line-too-long)
	************* Module anchorman.main
	C: 51, 0: Line too long (98/80) (line-too-long)
	************* Module anchorman.utils
	C: 14, 0: Line too long (121/80) (line-too-long)
	C: 17, 0: Final newline missing (missing-final-newline)
	************* Module anchorman.generator.candidate
	C:  5, 0: Empty function docstring (empty-docstring)
	R: 66, 0: Too many local variables (16/15) (too-many-locals)
	C: 79, 8: Invalid variable name "u" (invalid-name)
	C: 80, 8: Invalid variable name "u" (invalid-name)
	W: 77, 8: Unused variable 'i' (unused-variable)
	************* Module anchorman.generator.text
	C:  7, 4: Invalid variable name "x" (invalid-name)
	************* Module anchorman.positioner.interval
	C:  6, 0: Invalid argument name "t" (invalid-name)
	
	
	
Report
======
175 statements analysed.

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
|function |17     |17         |=          |94.12       |0.00     |
+---------+-------+-----------+-----------+------------+---------+



External dependencies
---------------------
::

    anchorman 
      \-configure (anchorman.main)
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
    yaml (anchorman.configure)



Raw metrics
-----------

+----------+-------+------+---------+-----------+
|type      |number |%     |previous |difference |
+==========+=======+======+=========+===========+
|code      |188    |44.24 |188      |=          |
+----------+-------+------+---------+-----------+
|docstring |57     |13.41 |57       |=          |
+----------+-------+------+---------+-----------+
|comment   |72     |16.94 |72       |=          |
+----------+-------+------+---------+-----------+
|empty     |108    |25.41 |108      |=          |
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
|convention |10     |16       |-6.00      |
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
|anchorman.generator.candidate |0.00  |100.00  |100.00   |30.00      |
+------------------------------+------+--------+---------+-----------+
|anchorman.utils               |0.00  |0.00    |0.00     |20.00      |
+------------------------------+------+--------+---------+-----------+
|anchorman.configure           |0.00  |0.00    |0.00     |20.00      |
+------------------------------+------+--------+---------+-----------+
|anchorman.positioner.interval |0.00  |0.00    |0.00     |10.00      |
+------------------------------+------+--------+---------+-----------+
|anchorman.main                |0.00  |0.00    |0.00     |10.00      |
+------------------------------+------+--------+---------+-----------+
|anchorman.generator.text      |0.00  |0.00    |0.00     |10.00      |
+------------------------------+------+--------+---------+-----------+



Messages
--------

+----------------------+------------+
|message id            |occurrences |
+======================+============+
|line-too-long         |4           |
+----------------------+------------+
|invalid-name          |4           |
+----------------------+------------+
|unused-variable       |1           |
+----------------------+------------+
|too-many-locals       |1           |
+----------------------+------------+
|missing-final-newline |1           |
+----------------------+------------+
|empty-docstring       |1           |
+----------------------+------------+



Global evaluation
-----------------
Your code has been rated at 9.31/10 (previous run: 8.97/10, +0.34)

