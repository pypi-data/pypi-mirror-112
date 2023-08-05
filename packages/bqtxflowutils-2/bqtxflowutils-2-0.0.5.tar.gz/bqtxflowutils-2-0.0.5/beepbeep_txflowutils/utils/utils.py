import os

class Utilities:
    def __init__(self):
        pass
    def _root_path(self):
            ABSPATH = os.path.abspath(__file__)
            BASE_AUTH_DIR = os.path.dirname(ABSPATH) # auth/
            BASE_BASES_DIR = os.path.dirname(BASE_AUTH_DIR) # bases/
            ROOT_DIR_PATH = os.path.dirname(BASE_BASES_DIR) # sync_from_bq_to_github/

            return ROOT_DIR_PATH
    
    def _markdown_dir_path(self):
            MARKDOWN_DIR_PATH = os.path.join(_root_path(), 'markdown')
            return MARKDOWN_DIR_PATH


def _root_path():
            ABSPATH = os.path.abspath(__file__)
            BASE_AUTH_DIR = os.path.dirname(ABSPATH) # auth/
            BASE_BASES_DIR = os.path.dirname(BASE_AUTH_DIR) # bases/
            ROOT_DIR_PATH = os.path.dirname(BASE_BASES_DIR) # sync_from_bq_to_github/

            return ROOT_DIR_PATH
            
if __name__ == "__main__":
    pass