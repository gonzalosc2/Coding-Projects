####################################
# author: Gonzalo Salazar
# course: 2020 Complete Python Bootcamps: From Zero to Hero in Python
# purpose: milestone project 1 - create a Tic-Tac-Toe game
# description: main file
# other: N/A
####################################

#recall: to set working directory
#cd ..
#cd Python/Udemy_PythonBootcamp/MilestoneProject_1

import T3_functions as fx

while fx.game() == True:
    if fx.replay() in ['y','Y']:
        continue
    else:
        break

exit()
