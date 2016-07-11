'''Functions for data reading and displaying'''

#modules
from test_teamrise.toolbox import extract, Objective_Tree, flat_graph
from openpyxl import load_workbook

def extract_team_id(user_list):
    '''Extract id of users'''
    out = dict()
    for user in user_list :
        out[user['id']] = user['team_id']
    return out

def extract_user_names(user_list):
    '''Extract name of users'''
    out = dict()
    for user in user_list :
        out[user['id']] = user['name']
    return out


def load_dataset(name):
    '''Read the users and objectives tables of dataset'''
    wb = load_workbook(name)
    _, u = extract(wb["users"])
    _, o = extract(wb["objectives"])
    return o, u

def create_tree(objectives, users):
    '''Create and fill the Objective tree from objectives and users'''
    out = Objective_Tree(objectives)
    out.compute_children_progress()
    out.fill_level_and_team(extract_team_id(users), extract_user_names(users))
    return out


def classic_presentation(obj):
    '''Function for a classic presentation of objectives.'''
    return '{0:.0f} : {1}\n {2:.0f}/{3:.0f} ({4})'.format(obj['id'], obj['title'],
                                                          obj['progress_value'], obj['progress_target'], obj['owner_name'])

class Data_reader():
    '''Read the objectives and users datasets and create the corresponding tree.
    'display' display the tree according to several filters
    '''
    def __init__(self, dataset_name):
        self.tree = create_tree(*load_dataset(dataset_name))
    def display(self, team='all', level='all', minimum_progress='all', presentation = classic_presentation):
        working_tree = self.tree
        if team is not 'all' :
            working_tree = working_tree.filter_at_root(lambda x: (x['team_id']==team))
        filtering_functions=[]
        if level is not 'all' :
            filtering_functions.append(lambda x: (x['level']==level))
        if minimum_progress is not 'all' :
            filtering_functions.append(lambda x: (x['progress_value']/x['progress_target']>=minimum_progress))
        if not filtering_functions :
            return working_tree.to_graph(function=presentation)
        return flat_graph(working_tree.filter_at_elements(lambda x:all(f(x) for f in filtering_functions)), function=presentation)