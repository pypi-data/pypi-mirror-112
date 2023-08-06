from pyocs import pyocs_config
from pyocs.pyocs_database import pyocsDataBase

class commonDataBase:
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(commonDataBase, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = pyocs_config.PyocsConfig.get_config()
        self.database = pyocsDataBase(
            pyocsDataBase.sql_server(config['sql_host'], int(config['sql_port']), config['sql_user_name'],
                                     config['sql_password'], config['sql_database_name']))

    def get_code_mapping_info_by_project(self, project):
        data = self.database.get_value_of_key('pyocs_jenkins_autobuild_map', 'project', project)
        result = list(data)
        return result

    def get_download_link_of_dt_by_customer(self, customer):
        data = self.database.get_value_of_key('pyocs_customer_need_map', 'customer', customer)
        return data[0]

