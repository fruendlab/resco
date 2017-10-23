import os


def create_tree(tree):
    if isinstance(tree, str):
        open(tree, 'a').close()
    elif isinstance(tree, (list, tuple)):
        for element in tree:
            create_tree(element)
    elif isinstance(tree, dict):
        for folder, content in tree.items():
            os.path.makedirs(folder, exist_ok=True)
            create_tree(content)
    else:
        raise ValueError('Invalid tree specification')
