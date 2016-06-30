
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