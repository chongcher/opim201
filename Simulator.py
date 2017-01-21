
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
    conche_asis = ConcheAsIs()
    conche_tobe = ConcheToBe()
    ball_mill = BallMillToBe()
    tempering = Tempering()
    moulding = Moulding()
    workflow = [bean_cleaner, roaster, winnower, melangeur]
    if as_is == "true":
        workflow.append(conche_asis)
        workflow.append(tempering)
        workflow.append(moulding)
        print("Beginning as-is simulation")
    else:
        workflow.append(conche_tobe)
        workflow.append(ball_mill)
        workflow.append(tempering)
        workflow.append(moulding)
        print("Beginning to-be simulation")

    queue = [to_be_processed]
    for i in range(0, len(workflow)):
        queue.append(0)
    last_machine = len(queue) - 1
    elapsed_time = -1
    while queue[last_machine] < expected_output:
        elapsed_time += 1
        print(elapsed_time, ": ", queue.__str__())
        for i in range(0, len(workflow)):
            result = workflow[i].step()
            if result == -1:
                pass
            elif result == 0:
                temp = min(workflow[i].max_input, queue[i])
                #print("Hey!", workflow[i].max_input)
                #print("Hey Hey!", queue[i])
                #print("Hey Hey Hey!", min(workflow[i].max_input, queue[i]))
                if temp <= 0: pass
                else:
                    queue[i] -= temp
                    workflow[i].start_cycle(min(workflow[i].max_input, temp))
            else:
                #print("What! ", queue[i+1])
                #print("Result: ", result)
                queue[i+1] += result
                #print("What What! ", queue[i+1])
                #print("What What What! ", queue)

    print("Elapsed Time: ", elapsed_time)
