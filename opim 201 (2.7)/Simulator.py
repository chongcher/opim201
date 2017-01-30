
import sys

from models.BallMillToBe import BallMillToBe
from models.BeanCleaner import BeanCleaner
from models.ConcheAsIs import ConcheAsIs
from models.ConcheToBe import ConcheToBe
from models.Melangeur import Melangeur
from models.Moulding import Moulding
from models.Roaster import Roaster
from models.Tempering import Tempering
from models.Winnower import Winnower


class Simulator:

    percentage = sys.argv[1]
    as_is = sys.argv[2]

    if percentage == '62':
        to_be_processed = 1197
        expected_output = 850
    else:
        raise Exception("Percentage not recognised!")

    bean_cleaner = BeanCleaner()
    roaster = Roaster()
    winnower = Winnower()
    melangeur = Melangeur()
    conche_asis = ConcheAsIs(expected_output)
    conche_tobe = ConcheToBe(expected_output)
    ball_mill = BallMillToBe(expected_output)
    tempering = Tempering(expected_output*0.1)  # Tempering and moulding takes 10%
    moulding = Moulding(expected_output*0.1)    # of output of conche machine
    workflow = [bean_cleaner, roaster, winnower, melangeur]
    if as_is == "true":
        workflow.append(conche_asis)
        workflow.append(tempering)
        workflow.append(moulding)
        print "Beginning as-is simulation"
    else:
        workflow.append(conche_tobe)
        workflow.append(ball_mill)
        workflow.append(tempering)
        workflow.append(moulding)
        print "Beginning to-be simulation"

    queue = [to_be_processed]
    for i in range(0, len(workflow)):
        queue.append(0)
    last_machine = len(queue) - 1
    elapsed_time = -1
    #while queue[last_machine] < expected_output * 0.35: # Only 35% is packed by Scharffen Berger
    while queue[last_machine] < expected_output:
        elapsed_time += 1
        print "{}: {}".format(elapsed_time, queue.__str__())
        if elapsed_time > 100:
            break
        for i in range(0, len(workflow)):
            result = workflow[i].step()
            if result == -1:
                pass
            elif result == 0:
                
                if queue[i] >= workflow[i].max_input:
                    queue[i] -= workflow[i].max_input
                    workflow[i].start_cycle(workflow[i].max_input)
                    
                elif sum(queue[0:i]) == 0 and queue[i] > 0:
                    waiting = False
                    for j in range(0, i):
                        if workflow[j].current_input != 0:
                            waiting = True
                    if not waiting:
                        workflow[i].start_cycle(queue[i])
                        queue[i] = 0
            else:
                queue[i+1] += result
        if (elapsed_time % 15) == 0:
            print "Time: {}".format(elapsed_time)
            if len(workflow) == 7:
                machine_names = ['Bean Cleaner', 'Roaster', 'Winnower', "Melangeur", 'Conche', 'Tempering',
                                 'Moulding']
            else:
                machine_names = ['Bean Cleaner', 'Roaster', 'Winnower', "Melangeur", 'Conche', 'Ball Mill',
                                 'Tempering', 'Moulding']
            for i in range(0, len(queue) - 1):
                break
                print "{}\n\tIn queue = {}\n\tProcessing = {}".format(machine_names[i], queue[i], workflow[i].current_input)
            
            print "Total Output = {}".format(queue[len(queue) - 1])
            print"\n"

    print "---End of workflow---"
    print "Total Elapsed Time: {}".format(elapsed_time)
    print "Final Output: {}".format(queue[last_machine])
    if len(workflow) == 7:
        machine_names = ['Bean Cleaner', 'Roaster', 'Winnower', "Melangeur", 'Conche', 'Tempering',
                         'Moulding']
    else:
        machine_names = ['Bean Cleaner', 'Roaster', 'Winnower', "Melangeur", 'Conche', 'Ball Mill',
                         'Tempering', 'Moulding']
    for i in range(0, len(queue) - 1):
        break
#        print"{}\n\tIn queue = {}\n\tProcessing = {}".format(machine_names[i], queue[i], workflow[i].current_input)
#    print "Total Output = {}".format(queue[len(queue) - 1])
#    print "\n"
