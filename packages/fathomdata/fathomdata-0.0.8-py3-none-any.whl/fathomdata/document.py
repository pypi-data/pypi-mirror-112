import pandas as pd


class Document:

    def __init__(self, document_data_dict, document_id):
        self.document_id = document_id
        self._materials_dict = document_data_dict['materials'] or {}
        self._steps_dict = document_data_dict['steps'] or {}
        self._parameters_dict = document_data_dict['parameters'] or {}

    def __repr__(self):
        return f'<Fathom Document with ID {self.document_id}>'

    def get_materials_df(self):
        return pd.DataFrame.from_dict(self._materials_dict)

    def get_steps_df(self):
        return pd.DataFrame.from_dict(self._steps_dict)

    def get_parameters_df(self):
        return pd.DataFrame.from_dict(self._parameters_dict)
