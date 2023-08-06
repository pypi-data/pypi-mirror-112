from .chart import Chart
import plotly.express as px

class ViolinPlot(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the violinPlot object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._label_column, 1) and self._is_var_exist(self._numerical_column, 1)

        return is_promote

    def plot(self):
        """
        Generate visualization
        """
        if self.promote_to_candidate():
            self.draw()
        else:
            pass

    def _check_requirements(self):
        """
        Check the requirements for generating violinPlot visualization

        Returns:
            (string) numerical_label: label of numerical column
            (list) label_column: label column
        """
        numerical_label = None
        label_column = None

        if self._is_numerical_column_exist(1):
            numerical_label = self._numerical_column[0]
            if self._is_label_column_exist(1):
                label_column=self._label_column
                
        return numerical_label, label_column      

    def draw(self):
        """
        Generate violinPlot visualization
        """
        numerical_label, label_column  = self._check_requirements()

        if numerical_label is not None and label_column is not None:
            axis_label,group_label,make_axis_label = None,None, None
            if len(label_column) >= 3:
                axis_label,group_label,make_axis_label = self._check_labels()
            else:
                axis_label,group_label = self._check_labels()
                
            orientation = self._check_orientation(axis_label,group_label)

            if make_axis_label is not None:
                axis_label = make_axis_label
            else:
                pass

            if group_label is not None:
                if orientation is not None:
                    fig = px.violin(self.dataframe, x=numerical_label, y=axis_label, color=group_label)
                    fig.show()
                else:
                    fig = px.violin(self.dataframe, x=axis_label, y=numerical_label, color=group_label)
                    fig.show()
            else:
                if orientation is not None:
                    fig = px.violin(self.dataframe, x=numerical_label, y=axis_label)
                    fig.show()
                else:
                    fig = px.violin(self.dataframe, x=axis_label, y=numerical_label)
                    fig.show()                     