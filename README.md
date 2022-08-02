# Transform-tool
Maya python script and plug-in that enables users to transform selected geometry using arithmetic operators.

This tool is a more efficent implementation of native maya transformation operations. It allows users to 
transform selected polygonal geometry by arithmetic operations within the attribute editor and the custom 
Maya window upon its execution.

By default the tool is set to global transform, but users can toggle between the global and local transform
space by checking and unchecking the global checkbox within the custom maya window.

The user can specify 1+2, 2/1, 2%1 and all such transform operations in any one of the provided float fields 
and the tool will apply those transformations whenever the apply button is pressed. 

Trigonometric and negative operations are also supported within this tool. 

//WARNING//

This tool is only compatible with polygonal meshes and mesh components. If the user tries to apply changes to
NURBS or curve selected geometry, the tool will not apply those changes.

Compatible with Maya 2019, 2020 and all Python 2.7.7 versions.
