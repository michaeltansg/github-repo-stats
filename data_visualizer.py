import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
from pandas import DataFrame

class DataVisualizer:
    """ Class to visualize the data """
    def __init__(self, data_frame: DataFrame):
        self.data_frame = data_frame

    def show_table(self):
        """ Show the data frame as a table """
        # Copy the data frame
        data_frame_copy = self.data_frame.copy()
        data_frame_copy.drop(columns=['Contribution data'], inplace=True)
        data_frame_copy.drop(columns=['Significant Contributors'], inplace=True)
        print(data_frame_copy)

    def plot_data(self):
        """ Plot the data as a bar chart """
        # Function that converts large numbers to 'K' (thousands)
        def ticker_formatter(value, _tick_number):
            # convert value to thousands
            if value >= 1000:
                value_in_k = int(value / 1000)
                return f'{value_in_k}K'
            else:
                return int(value)

        # Function to format the numbers
        def format_num(num):
            return str(num) if num < 1000 else str(np.round(num / 1000, 1)) + 'K'

        # Helper function to create a bar chart for a given axis and column
        def create_bar_chart(ax, title, ylabel, column, round_values=False):
            values = self.data_frame[column].round(1) if round_values else self.data_frame[column]
            ax.bar(self.data_frame['Project Name'], values, color='skyblue')
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            max_height = max(values)
            ax.set_ylim(0, max_height * 1.2)
            for i, v in enumerate(values):
                ax.text(i, v + 3, format_num(v), ha='center', va='bottom')
            ax.tick_params(axis='x', rotation=45)

        # Set up the figure and the axes
        _fig, axs = plt.subplots(nrows=3, figsize=(10, 8))

        # Use FuncFormatter to apply the function to the y-axis labels
        formatter = ticker.FuncFormatter(ticker_formatter)
        for ax in axs:
            ax.yaxis.set_major_formatter(formatter)

        # Create bar charts
        create_bar_chart(axs[0], 'Number of Contributors for Each Project', 'Number of Contributors', 'Number of Contributors')
        create_bar_chart(axs[1], 'Number of Stars for Each Project', 'Number of Stars', 'Stars')
        create_bar_chart(axs[2], 'Average Commits per Month for Each Project', 'Average Commits per Month', 'Average Commits per Month', round_values=True)

        # Adjust the layout
        plt.tight_layout()
        plt.show()