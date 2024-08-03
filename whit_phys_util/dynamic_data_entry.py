import pandas as pd
import numpy as np
import sys
from ipydatagrid import DataGrid

class DynamicDataEntry:
    """
    DynamicDataEntry

    Uses the ipydatagrid widget to allow interactive data frame entry with data stored in a csv file.

    INPUTS:
    fname - name of CSV file associated with the data (doesn't need to exist yet)
    columns - list of strings specifying the names of columns (only used if CSV file doesn't exist)
    num_rows - number of rows in data file
    """
    def __init__(self,fname,columns,num_rows):
        self.max_height = 200
        self.in_colab = "google.colab" in sys.modules
        if self.in_colab:
            from google.colab import output
            output.enable_custom_widget_manager()
        self.fname = fname
        try:
            df = pd.read_csv(self.fname)
        except FileNotFoundError:
            d = {}
            for col in columns:
                d[col] = np.zeros(num_rows)
            df = pd.DataFrame(data=d)
        height = min(20*num_rows + 30, self.max_height)
        self.dg = DataGrid(df, editable=True, layout={'height': f"{height}px"}, auto_fit_columns=True,selection_mode='row')

    def edit_sheet(self):
        return self.dg
  
    def save(self):
        self.dg.data.to_csv(self.fname,index=False)
  
    def get_dataframe(self):
        return self.dg.data.copy(deep=True)