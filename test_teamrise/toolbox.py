
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




class Tree():
    '''tree of dictionaries
    
    children of an element are stored in a list, stored in the element itself, under a chosen key ('childs' by default)
    organised using id (need to be unique for each element)
    and parent_id to connect an element to its parent, if parent_id==None the element in a root
    '''
    
    def __init__(self, elements = [], key_word = 'childs'):
        self.roots = []
        self.store_nodes = []
        self.key = key_word
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
                
                
                
                
                
                
class Objective_Tree(Tree):

    
    #children progress computation
    
    def children_progress_calculation(self, element):
        if self.key in element :
            cp = []
            for children in element[self.key]:
                cp.append(children['progress_value']*100/children['progress_target']) #percentage
            element['children_progress'] = sum(cp)/len(cp) #average


    def compute_children_progress(self):
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
            
            