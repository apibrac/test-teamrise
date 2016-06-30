from graphviz import Digraph
from openpyxl import load_workbook



def extract(worksheet):
    '''extract information in worksheet according to the first line'''
    rows = worksheet.iter_rows()
    heading = next(rows)
    fields = dict()
    for i,cell in enumerate(heading) :
        if cell.value is not None :
            fields[i]=cell.value
    values = []
    for row in rows :
        row_dict=dict()
        for key,field in fields.items() :
            row_dict[field] = row[key].value
        values.append(row_dict)
    return fields,values


def flat_graph(list_of_elements, function = lambda x: x['id']):
    '''plot a graph with no link between elements'''
    out = Digraph()
    for element in list_of_elements :
        out.node(str(element['id']), str(function(element)))
    return out


class Tree():
    '''tree of dictionaries
    
    children of an element are stored in a list, stored in the element itself, under a chosen key ('childs' by default)
    organised using id (need to be unique for each element)
    and parent_id to connect an element to its parent, if parent_id==None the element in a root
    '''
    
    def __init__(self, elements = [], key_word = 'childs', roots=[]):
        self.roots = roots
        self.key = key_word
        self.store_nodes = []
        for element in self :
            self.store_nodes.append(element['id'])
        self.fill_with(elements)
    
    def fill_some(self, elements):
        '''put some elements in the tree: if their parents are already in there; and delete them from elements'''
        for element in elements :
            if element['parent_id'] is None : #this is a level 1
                self.roots.append(element)
            elif element['parent_id'] in self.store_nodes :
                self.put(element)
            else :
                continue
            elements.remove(element)
            self.store_nodes.append(element['id'])
            
    def put(self, element):
        '''put element in the tree (the parent needs to be in the tree)'''
        for parent in self :
            if element['parent_id'] == parent['id'] :
                if self.key not in parent :
                    parent[self.key] =[]
                parent[self.key].append(element)
                return
    
    def fill_with(self, elements):
        '''recursive calls of fill_some until elements in empty
        control that the tree can be built
        '''
        n = len(elements)
        while(elements) :
            self.fill_some(elements)
            assert (len(elements) != n), 'Element list not coherent'
            n = len(elements)
    
    def iter_over(self, element):
        '''iterator on an element: send all his  'family' '''
        if self.key in element :
            for children in element[self.key] :
                for deep_children in self.iter_over(children) :
                    yield deep_children
        yield element
        
    
    def __iter__(self):
        '''iterator over the tree: send all elements one by one'''
        for root in self.roots :
            for deep_children in self.iter_over(root) :
                yield deep_children
    
    def to_graph(self, function=lambda x:x['id'] ):
        '''create a graph with graphviz package
        function is applied to each node to choose what to write
        '''
        out = Digraph()
        for root in self.roots :
            self.add_to_graph(out, root, function)
        return out
    
    def add_to_graph(self, graph, element, function, parent=None):
        '''add element and all its children to the graph'''
        graph.node(str(element['id']), str(function(element)))
        if parent :
            graph.edge(str(parent['id']), str(element['id']))
        if self.key in element :
            for children in element[self.key]:
                self.add_to_graph(graph, children, function, parent=element)
            
    def filter_at_root(self, root_filter):
        '''send a new Objective_Tree with only the objectives of the team team'''
        return Tree(roots = [r for r in self.roots if root_filter(r)])
    
    def filter_at_elements(self, personal_filter):
        '''return a list of elements of level N'''
        return [e for e in self if personal_filter(e)] 
                
                
                
class Objective_Tree(Tree):
    '''Tree specialised for the test'''

    
    #children progress computation
    
    def children_progress_calculation(self, element):
        '''compute the children progress of element (if it has children)'''
        if self.key in element :
            cp = []
            for children in element[self.key]:
                cp.append(children['progress_value']*100/children['progress_target']) #percentage
            element['children_progress'] = sum(cp)/len(cp) #average


    def compute_children_progress(self):
        '''compute children progress for all elements'''
        for e in self :
            self.children_progress_calculation(e)
        
        
    #level and team computation  
            
    def fill_element_level_and_team(self, element, level, id_team):
        '''fill the levele and id_team of element, and call the function for the children'''
        element['level'] = level
        element['team_id'] = id_team
        if self.key in element :
            for children in element[self.key]:
                self.fill_element_level_and_team(children, level+1, id_team)



    def fill_level_and_team(self, team_ids):
        '''fill all level and id_team fields based on the team_ids correspondance'''
        for root in self.roots :
            id_team=team_ids[root['owner_id']]
            self.fill_element_level_and_team(root, 0, id_team)
            

        