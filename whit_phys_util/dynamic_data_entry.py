import pandas as pd
import numpy as np
import sys
import threading
from ipydatagrid import DataGrid
import matplotlib.pyplot as plt

class DynamicDataEntry:
    """Allows interactive data entry in notebook with connection to a csv file.

    Inputs
    ------
    fname : string
        Name of CSV file associated with the data (does not need to exist yet).
    columns : list of strings
        Names of columns. If CSV file already exists, these must match the column names in that file.
    rows : int or tuple
        Only used if CSV file does not exist.
    
        If int, then it specifies the number of rows in the data table.
        
        If tuple, it specifies linearly spaced values for first column using the format (start value, stop value, and step value). The number of rows is implied.
    """
    def __init__(self,fname,columns,rows):
        self.max_height = 200
        self.in_colab = "google.colab" in sys.modules
        if self.in_colab:
            from google.colab import output
            output.enable_custom_widget_manager()
        self.fname = fname
        try:
            df = pd.read_csv(self.fname)
            num_rows = df.shape[0]
        except FileNotFoundError:
            d = {}
            if isinstance(rows,int):
                num_rows = rows
                indep_col = np.zeros(num_rows)
            elif isinstance(rows,(list,tuple)) and len(rows) == 3:
                num_rows = int((rows[1]-rows[0])/rows[2])+1
                indep_col = np.linspace(rows[0],rows[1],num_rows)
            else:
                raise ValueError("Invalid row specification")
            d[columns[0]] = indep_col
            for col in columns[1:]:
                d[col] = np.zeros(num_rows)
            df = pd.DataFrame(data=d)
        if df.columns.tolist() != columns:
            self.dg = None
            raise ValueError("Columns in file do not match those specified in command.")
        self.height = min(20*num_rows + 30, self.max_height)
        self.dg = DataGrid(df, editable=True, auto_fit_columns=True,selection_mode='row',header_visibility='column')
        self.autosave_minutes = 5 # time interval for autosave

    def edit_sheet(self,autosave=True):
        """Display interactive table for entry/editing or row selection."""
        if self.dg is not None:
            self.autosave = autosave
            self.save_timer_set = False
            self.dg.on_cell_change(self._change_tracking)
            self.dg.layout = {'height': f"{self.height}px"}
            return self.dg
        else:
            raise RuntimeError("Valid DynamicDataEntry object does not exist")  
    
    def save(self):
        """Save table data to CSV file."""
        self.dg.layout = {'height': "0px"}
        self.save_timer_set = False
        self.dg.data.to_csv(self.fname,index=False)

    def get_dataframe(self):
        """Copy of table data as DataFrame."""
        self.dg.layout = {'height': "0px"}
        df = self.dg.data.copy(deep=True)
        df.index.name = None
        return df
    
    def quick_graph(self):
        """Graph of table data using first column as independent variable."""
        df = self.dg.data
        indep_col = df.columns[0]
        for col in df.columns[1:]:
            plt.plot(df[indep_col],df[col],marker='o',linestyle='solid')
        plt.xlabel(indep_col)
        plt.legend(df.columns[1:])
        plt.show()

    def add_rows(self, num_new_rows):
        """Expand table by appending specified number of rows (filled with zeros)."""
        self.dg.layout = {'height': "0px"}
        df = self.dg.data
        curr_rows = df.shape[0]
        i0 = df.index[-1] # index label and index number may not agree
        num_rows = curr_rows + num_new_rows
        zero_row = dict.fromkeys(df.columns,0)
        for i in range(i0+1,i0+num_new_rows+1):
            df.loc[i] = zero_row
        self.height = min(20*num_rows + 30, self.max_height)
        self.dg = DataGrid(df, editable=True, auto_fit_columns=True,selection_mode='row',header_visibility='column')

    def drop_all_zero_rows(self):
        """Shrink the table by dropping any row in which each every column has a value of 0."""
        self.dg.layout = {'height': "0px"}
        df = self.dg.data
        all_zero_row = (df[df.columns] == 0).all(axis=1)
        df.drop(df[all_zero_row].index, inplace=True)
        num_rows = df.shape[0]
        self.height = min(20*num_rows + 30, self.max_height)
        self.dg = DataGrid(df, editable=True, auto_fit_columns=True,selection_mode='row',header_visibility='column')

    def drop_selected_rows(self):
        """Shrink the table by dropping rows selected in interactive view."""
        self.dg.layout = {'height': "0px"}
        df = self.dg.data
        regions = self.dg.selections
        for rect in regions:
            for i in range(rect['r1'],rect['r2']+1):
                df.drop(i,inplace=True)
        num_rows = df.shape[0]
        self.height = min(20*num_rows + 30, self.max_height)
        self.dg = DataGrid(df, editable=True, auto_fit_columns=True,selection_mode='row',header_visibility='column')

    def _change_tracking(self,cell):
        if not self.save_timer_set and self.autosave:
          self.save_timer_set = True
          threading.Timer(60*self.autosave_minutes,self.__autosave()).start()

    def __autosave(self):
        if self.save_timer_set:
          self.dg.data.to_csv(self.fname,index=False)
          self.save_timer_set = False