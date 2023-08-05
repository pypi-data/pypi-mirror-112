import os
import sys
import json

class InfoSchema():
    # Methods
    def _root_path(self):
        ABSPATH = os.path.abspath(__file__)
        BASE_AUTH_DIR = os.path.dirname(ABSPATH) # auth/
        BASE_BASES_DIR = os.path.dirname(BASE_AUTH_DIR) # bases/
        ROOT_DIR_PATH = os.path.dirname(BASE_BASES_DIR) # sync_from_bq_to_github/

        return ROOT_DIR_PATH
    

    # dataset_name_and_type return a dataset object from the instance
    def dataset_instance(client_instance=None, project_id=None, dataset_id=None):
        project_id = project_id
        dataset_id = dataset_id
        bigquery_client = client_instance

        dataset_list_table = bigquery_client.get_dataset(dataset_id)  # Make an API request.
        full_dataset_id = "{}.{}".format(dataset_list_table.project, dataset_list_table.dataset_id)
        print("Got dataset '{}'.".format(full_dataset_id))
        print("DATASET MODIFIED AT: ", dataset_list_table.modified)
        return dataset_list_table


    def download_and_create_file(self,
                                    ref_one_name: str,
                                    ref_two_name: str, 
                                    directory_name: str, 
                                    payload: str, 
                                    fname: str = None
                                    ) -> str:  


        directory_name_path = os.path.join(self._root_path(), directory_name)

        if fname is None:
            fname = "{}_{}_{}_{}".format(
                                    self.project_id,
                                    self.dataset_id,
                                    ref_one_name,
                                    ref_two_name
                                )
        fname_path = os.path.join(directory_name_path, fname)


        if self.check_filename_path_exists(fname_path, directory_name_path):
            print(f"Filename: {fname} already exist")
            return None

        try:
            with open(fname_path, 'w') as f:
                if isinstance(payload, str):
                    f.write(payload)
                else:
                    f.write(json.dumps(payload, indent=4))
        except Exception as err:
            print(err)
        
        return fname_path


    def check_filename_path_exists(self, filename: str, filesdir_name: str) -> bool:
        """
        This function test whether a path exist. Returns False for broken filename path
        """
        filesdir_name_path = os.path.join(self._root_path(), filesdir_name)
        filename_path = os.path.join(filesdir_name_path, filename)
        os.makedirs(filesdir_name_path, exist_ok=True)
        file_result = os.path.exists(filename_path)

        return file_result

if __name__ == "__main__":
    pass