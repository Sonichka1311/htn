from pddl_classes import *

def parse_Domain(Domain_file):
    try:
        head = []
        for line in Domain_file:
            head = clear_line(line)
            if len(head) > 0:
                break
        
        D = Domain(head[2])
            
        ### parsing Predicates
    
        for line in Domain_file:
            cur = clear_line(line)           
            if len(cur) != 0:
                break
        for line in Domain_file:
            cur = line.split()
            if len(cur) == 0:
                continue
            elif cur[0] == ')':
                break
            for i in range(len(cur)):
                cur[i] = cur[i].strip('(').strip(')')
            pred_name = cur[0]
            D.preds[pred_name] = Predicate(pred_name, len(cur) - 1)
        
        ### parsing tasks
        for line in Domain_file:
            cur = cur = line.split()
            if cur[0] == ')':
                break
            for i in range(len(cur)):
                cur[i] = cur[i].strip('(').strip(')')
            if len(cur) == 0:
                continue
            
        ### parsing operators
        
        for line in Domain_file:
            cur = line.split()
            if len(cur) > 0 and cur[0] == ')':
                break
            for i in range(len(cur)):
                cur[i] = cur[i].strip('(').strip(')')
            if len(cur) == 0:
                continue
            op = Operator(cur[1], '', [], [])
            for line in Domain_file:
                cur = line.split()
                if len(cur) > 0:
                    break
            op.taskname = line[1][1:-1]
            for line in Domain_file:
                cur = line.split()
                if len(cur) > 0:
                    break

            param_map = dict()
            param_num = 0                
            state = 1
            for line in Domain_file:
                cur = line.split()
                for i in range(len(cur)):
                    cur[i] = cur[i].strip('(')
                    if state != 4:
                        cur[i] = cur[i].strip(')')           
                if state == 1:
                    if len(cur) == 0:
                        continue
                    if cur[0] == ':parameters':
                        state = 2
                    continue
                elif state == 2:
                    if len(cur) == 0:
                        continue
                    if cur[0] == ':precondition':
                        state = 3
                        continue
                    else:
                        cur_param_name = cur[0]
                        param_map[cur_param_name] = param_num
                        param_num += 1   
                elif state == 3:                   
                    if len(cur) == 0 or cur[0] == 'and':
                        continue
                    elif cur[0] == ':effect':
                        state = 4
                        continue
                    else:
                        start = (cur[0] == 'not')
                        pred = D.preds[cur[start]]
                        pred_params = [param_map[param] for param in cur[start + 1:]]
                        act.preconds.append([start ^ 1, pred, pred_params])
                elif state == 4:
                    if len(cur) == 0 or cur[0] == 'and':
                        continue                
                    elif cur[0] == ')':
                        break
                    for i in range(len(cur)):
                        cur[i] = cur[i].strip(')') 
                    start = (cur[0] == 'not')
                    pred = D.preds[cur[start]]
                    pred_params = []
                    for param in cur[start + 1:]:
                        pred_params.append(param_map[param])
                    op.effects.append([start ^ 1, pred, pred_params])
            D.operators.append(op)
        
        ### parsing methods
        
        
        
        return D
    except:
        print('Wrong format: unable to recognize\n')
        return
