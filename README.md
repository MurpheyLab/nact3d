# nact3d
An ros package communcating with the NACT3D over an ethernet connection. This should be run in conjunction with a node publishing dynamics and a biasforce to the topics:
* cursor_dyn
* cursor_bias 
It publishes the current state of the robot end effector to the topic:
* cursor_state
The default dynamics are set in the python package src/act3d


