# Description


This is a deterministic pushdown automata simulator program. The DPDA recognizes DCFLs. 

Made by:
Longno, Darren
Lu, Juhlia
Villarama, Kenn

STALGCM S13

## How to Use

When it comes to the input and output format of the simulation
of the machine, "  ̃ " is used to represent lambda/epsilon λ . As
for the inputted fields and format for the machine definition
file, the machine either accepts its input through the GUI itself
or it can be attached a machine definition file in .txt format
through the "Load DPDA" button. A machine definition file
for DPDA contains the contents of text fields 2 to 7. Moreover,
the following fields and their functionalities are as follows:

Text Field 1: Name of the DPDA program (Note: This can
also be the .txt file’s file name.)
Text Field 2: Symbols to be used for the input alphabet that
is separated by a comma " (Note: "  ̃ " is not allowed as an
alphabet character)
Text Field 3: Symbols to be used for the stack alphabet that is
separated by a comma (Note:" ̃" is not allowed as an alphabet
character)
Text Field 4: Names of the states separated by commas (ex:
q0,q1,qs)
Text Field 5: The Start State (ex: q0)
Text Field 6: List of state names separated by commas that are
considered as the accepting states (ex. q1,qs)
Text Field 7: One transition rule per line with the format:
<InitialStateName>,<InputSymbol>, <stacktop> | <NewState-
Name>, <newstacktop> (Note: Processing of rules stops with
the end of the .txt file)

After pressing the "Start Machine" button, the DPDA simulator
will display the steps that the DPDA took throughout its run.
All logs of the steps taken are indicated in a text box that can be
scrolled through by the user. In each step, the logs will contain
the current state, the input symbol being processed, and the
contents of the stack. Finally, the machine status will also be
indicated in the logs as well as in a dialog box. Additionally,
users can choose to save their machine definition in a .txt file
through the "Save DPDA" button for convenience



## Dependencies

You need to install the following dependencies in order to run the program in your computer:

- tkinter
- customtkinter

pip install tkinter
pip install customtkinter