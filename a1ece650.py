import sys
import re

class TrafficGraph(object):
    def __init__(self):
        # store street information with a dictionary
        self.street_info = dict()
        # store initial street information with a dictionary
        self.street_info_init = dict()
        # store vertices with a list after generating a graph
        self.vertex = set()
        # store edges with a list after generating a graph
        self.edge = set()
        # a flag used to mark whether the "street_info" is changed
        self.is_changed = True
    
    def addStreet(self, key, value):
        self.street_info_init[key] = value
        self.street_info[key] = list(value)
        self.is_changed = True
    
    def changeStreet(self, key, value):
        #if one item is changed, recover the "street_info" first
        for k, v in self.street_info_init.items():
            self.street_info[k] = list(v)  
        self.addStreet(key, value)
    
    def removeStreet(self, key):
        for k, v in self.street_info_init.items():
            self.street_info[k] = list(v)       
        del self.street_info[key]
        del self.street_info_init[key]
        self.is_changed = True
    
    def generate(self):
        # there is no need to regenerate a graph if the "street_info" is not changed
        if not self.is_changed:
            return
        # if the info is changed clear "vertex" and "edge" to regenerate a new graph
        self.vertex.clear()
        self.edge.clear()
        for k1, v1 in self.street_info.items():
            for k2, v2 in self.street_info.items():
                if k2 == k1:
                    continue
                # for each line in two streets we try to find the intersection 
                # and put proper vertices and edges into "vertex" and "edge"
                for line1 in v1:
                    for line2 in v2:
                        if line1 not in v1:
                            continue
                        intersect = self._cross(line1, line2)
                        # if line1 and line2 do not have intersection we go on with another two lines
                        if len(intersect) == 0:
                            continue 
                            
                        # this part tries to find out whether line1 and line2 will be separated by intersection
                        # if so we remove the line from street_info for we have to use two sublines in the future
                        # if the line lies in "edge" we also have to remove it because it is invalid now
                        l1 = self._formEdge(line1[0], line1[1])                        
                        if intersect != line1[0] and intersect != line1[1]: 
                            if l1 in self.edge:
                                self.edge.remove(l1)
                            v1.remove(line1)
                        l2 = self._formEdge(line2[0], line2[1])                        
                        if intersect != line2[0] and intersect != line2[1]: 
                            if l2 in self.edge:
                                self.edge.remove(l2)
                            if line2 in v2:
                                v2.remove(line2)
                                
                        # check the intersection and four verteices of line1 and line2
                        # if the vetices and edges are valid then put them into corresponding sets
                        # and put the new separated lines into street_info
                        for point in (intersect, line1[0], line1[1], line2[0], line2[1]):
                            new_vertex = (str(point[0]) + ':' + str(point[1]), point)
                            self.vertex.add(new_vertex)
                            if point != intersect:
                                e = self._formEdge(intersect, point)
                                self.edge.add(e)
                                new_line = (min(intersect, point), max(intersect, point))
                                if point in line1 and new_line not in v1:
                                    v1.append(new_line)
                                if point in line2 and new_line not in v2:
                                    v2.append(new_line)       
        self.is_changed = False
    
    # compute the intersection of two lines, return empty tuple if there is none
    @staticmethod
    def _cross(line1, line2):
        l1p1 = min(line1[0], line1[1])
        l1p2 = max(line1[0], line1[1])
        l2p1 = min(line2[0], line2[1])
        l2p2 = max(line2[0], line2[1])
        intersect = ()
        k1 = k2 = b1 = b2 = 0
        if l1p1[0] == l1p2[0] and l2p1[0] == l2p2[0]:
            if l1p1 == l2p2:
                intersect = l1p1
            elif l1p2 == l2p1:
                intersect = l1p2
        elif l1p1[0] == l1p2[0]:
            k2 = float((l2p1[1] - l2p2[1]) / (l2p1[0] - l2p2[0]))
            b2 = float((l2p1[0] * l2p2[1] - l2p2[0] * l2p1[1]) / (l2p1[0] - l2p2[0]))
            x = round(l1p1[0], 2)
            y = round(k2 * x + b2, 2)            
            if y >= l1p1[1] and y <= l1p2[1] and x >= l2p1[0] and x <= l2p2[0]:
                if x == 0:
                    x = 0.0
                if y == 0:
                    y = 0.0
                intersect = (x, y)
        elif l2p1[0] == l2p2[0]:
            k1 = float((l1p1[1] - l1p2[1]) / (l1p1[0] - l1p2[0]))
            b1 = float((l1p1[0] * l1p2[1] - l1p2[0] * l1p1[1]) / (l1p1[0] - l1p2[0]))
            x = round(l2p1[0], 2)
            y = round(k1 * x + b1, 2)
            if y >= l2p1[1] and y <= l2p2[1] and x >= l1p1[0] and x <= l1p2[0]:
                if x == 0:
                    x = 0.0
                if y == 0:
                    y = 0.0
                intersect = (x, y)
        else: 
            k1 = float((l1p1[1] - l1p2[1]) / (l1p1[0] - l1p2[0]))
            b1 = float((l1p1[0] * l1p2[1] - l1p2[0] * l1p1[1]) / (l1p1[0] - l1p2[0]))
            k2 = float((l2p1[1] - l2p2[1]) / (l2p1[0] - l2p2[0]))
            b2 = float((l2p1[0] * l2p2[1] - l2p2[0] * l2p1[1]) / (l2p1[0] - l2p2[0]))
            if k1 == k2:
                if l1p1 == l1p2:
                    intersect = l1p1
                elif l1p2 == l2p1:
                    intersect = l1p2
                return intersect
            x = round((b2 - b1) / (k1 - k2), 2)
            y = round((k1 * b2 - k2 * b1) / (k1 - k2), 2)
            if x >= max(l1p1[0], l2p1[0]) and x <= min(l1p2[0], l2p2[0]) and ((y >= max(l1p1[1], l2p1[1]) and y <= min(l1p2[0], l2p2[0])) or (y >= max(l1p2[1], l2p2[1]) and y <= min(l1p1[0], l2p1[0]))):
                if x == 0:
                    x = 0.0
                if y == 0:
                    y = 0.0
                intersect = (x, y)
#       print line1, line2, '---', intersect
        return intersect
    
    # compute the valid edge formation of two vertices
    def _formEdge(self, point1, point2):
        p1 = min(point1, point2)
        p2 = max(point1, point2)
        id1 = str(p1[0]) + ':' + str(p1[1])
        id2 = str(p2[0]) + ':' + str(p2[1])
        return (id1, id2)

    
# check whether the input is valid
def inputCheck(inputs, graph_obj):
    if inputs[0] == 'a' or inputs[0] == 'c':
        if len(inputs) < 3:
            alertFormatError()
            return False
        if not re.match(r'^[a-zA-Z][a-zA-Z\s]*', inputs[1]) or len(inputs[1]) > 50:
            alertFormatError()
            return False
        if inputs[0] == 'a' and inputs[1] in graph_obj.street_info:
            print 'Adding Street Error: Specified street already exits'
            return False
        if inputs[0] == 'c' and inputs[1] not in graph_obj.street_info:
            print 'Changing StreetError: Specified street does not exit'
            return False
        for t in re.split(r'\s+', inputs[2]):
            if not re.match(r'(\([-]?\d+[\.\d+]*,[-]?\d+[\.\d+]*\)\s*)+', t):
                alertFormatError()
                return False
        return True           
    elif inputs[0] == 'r':
        if len(inputs) != 2:
            alertFormatError()
            return False
        if not re.match(r'', inputs[1]):
            alertFormatError()
            return False
        if inputs[1] not in graph_obj.street_info:
            print 'Removing Street Error: Specified street does not exit'
            return False
        return True    
    elif inputs[0] == 'g':
        if len(inputs) > 1:
            alertFormatError()
            return False
        return True
    else:
        alertFormatError()
        return False

    
def alertFormatError():
    print 'Command Format Error: Please type again referring to the example below.'
    print '\t- Add a street (x1, x2, y1, y2 are numbers): a "street name" (x1,y1) (x2,y2) .. '
    print '\t- Chang a street (x1, x2, y1, y2 are numbers): c "street name" (x1,y1) (x2,y2) ..'
    print '\t- Remove a street: r "street name"'
    print '\t- Generate the graph (output the vertices and edges): g'
    print '\t- The length of street name should not exceed 50 words'

    
# parse the coordinate into valid format
def parseCoordinate(coordinate):
    street_vertex = re.split(r'\)\s*\(', coordinate[1:-1])
    street_lines = []
    for i in range(len(street_vertex) - 1):
        t1 = street_vertex[i].split(',')
        t2 = street_vertex[i+1].split(',')
        try:
            t10 = round(float(t1[0]), 2)
            t11 = round(float(t1[1]), 2)
            t20 = round(float(t2[0]), 2)
            t21 = round(float(t2[1]), 2)
        except:
            alertFormatError()
        p1 = min((t10, t11), (t20, t21))
        p2 = max((t10, t11), (t20, t21))
        street_lines.append((p1, p2))
    return street_lines
    

def main():
    graph = TrafficGraph()
    while True:        
        command = raw_input('Enter a command then press "enter", or just press "enter" to exit\n')
        # process the input string
        command = command.strip()
        if command == '':
            break
        arguments = re.split(r'"', command)
        for i in range(len(arguments)):
            arguments[i] = arguments[i].strip()
        arguments = filter(None, arguments)
        
        # check the input
        if not inputCheck(arguments, graph):
            continue
            
        # parse the input coordinate and get the output
        if arguments[0] == 'a' or arguments[0] == 'c':
            value = parseCoordinate(arguments[2])
            key = arguments[1]            
            if arguments[0] == 'a':
                graph.addStreet(key, value)
                print 'One item added:', key
            if arguments[0] == 'c':
                graph.changeStreet(key, value)
                print 'One item changed:', key
        elif arguments[0] == 'r':
            graph.removeStreet(arguments[1])
            print 'One item removed:', arguments[1]
        else:
            graph.generate()
            print 'V = {'
            for v in graph.vertex:
                print '\t', v[0], ':', v[1]
            print '}'
            print 'E = {'
            for e in graph.edge:
                print '\t<', e[0], ',', e[1], '>,'
            print '}'
#           print graph.street_info
#           print graph.street_info_init

    print 'Application terminated'
    sys.exit(0)

    
if __name__ == '__main__':
    main()
