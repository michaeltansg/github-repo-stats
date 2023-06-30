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
        def ticker_formatter(value, tick_number):
            # convert value to thousands
            if value >= 1000:
                value_in_k = int(value/1000)
                return f'{value_in_k}K'
            else:
                return int(value)

        # Function to format the numbers
        def format_num(num):
            return str(num) if num < 1000 else str(np.round(num/1000, 1)) + 'K'

        # Set up the figure and the axes
        fig, axs = plt.subplots(nrows=3, figsize=(10, 8))
        # fig.subplots_adjust(top=0.9)  # Adjust the top space

        # Use FuncFormatter to apply the function to the y-axis labels
        formatter = ticker.FuncFormatter(ticker_formatter)
        [ax.yaxis.set_major_formatter(formatter) for ax in axs]

        # Number of Contributors
        axs[0].bar(self.data_frame['Project Name'], self.data_frame['Number of Contributors'], color='skyblue')
        axs[0].set_title('Number of Contributors for Each Project')
        axs[0].set_ylabel('Number of Contributors')
        for i, v in enumerate(self.data_frame['Number of Contributors']):
            axs[0].text(i, v + 3, format_num(v), ha='center', va='bottom')
        axs[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

        # Number of Stars
        axs[1].bar(self.data_frame['Project Name'], self.data_frame['Stars'], color='skyblue')
        axs[1].set_title('Number of Stars for Each Project')
        axs[1].set_ylabel('Number of Stars')
        for i, v in enumerate(self.data_frame['Stars']):
            axs[1].text(i, v + 3, format_num(v), ha='center', va='bottom')
        axs[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

        # Average Commits per Month
        axs[2].bar(self.data_frame['Project Name'], self.data_frame['Average Commits per Month'], color='skyblue')
        axs[2].set_title('Average Commits per Month for Each Project')
        axs[2].set_xlabel('Project Name')
        axs[2].set_ylabel('Average Commits per Month')
        for i, v in enumerate(self.data_frame['Average Commits per Month']):
            axs[2].text(i, v + 3, format_num(round(v)), ha='center', va='bottom')
        axs[2].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

        # Adjust the layout
        plt.tight_layout()
        plt.show()
