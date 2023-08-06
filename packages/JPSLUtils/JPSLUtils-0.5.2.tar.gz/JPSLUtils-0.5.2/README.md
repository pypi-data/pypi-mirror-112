## JPSLUtils
(aka Jupyter Physical Science Lab Utilities)

#### Introduction
These are utilities used by multiple packages within the [Jupyter Physical
Science Lab project](https://github.com/JupyterPhysSciLab). It is unlikely 
that anyone 
but a 
developer would
have reason to install these independently. They are installed when
required by other packages/modules.

#### Contents
This package mostly provides tools for running javascript operations that
impact the notebook. This includes things such as selecting a certain cell,
inserting text into an existing cell, or running python code and using the
result from javascript. Some custom dialogs for user interaction are also
included.

#### Change Log
  * 0.5.2 Minor bug fixes and updates to README.
  * 0.5.1 Introduced "one time Javascript" (`OTJS(...)`) alternative to 
    `display(JS(...))`. This allows javascript calls from python that will 
    not be run the next time the notebook is opened and trusted.
  * 0.5.0 Initial release.

##### [This software is distributed under the GNU V3 license](https://gnu.org/licenses)
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Copyright - Jonathan Gutow, 2021.