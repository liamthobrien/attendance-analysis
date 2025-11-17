"""Importing necessary libraries"""
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive

"""Loading and preprocess the attendance data"""
shiny_df = pd.read_csv('cleaned_attendance_data.csv')
# This line was fixed (removed leading space)
module_list = shiny_df['Module Name'].unique().tolist()

"""Defining the UI for the Shiny app in sidebar layout"""
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "module_select",
            "Select Module:",
            choices=module_list,
            selected="Journalism"
        ),
        title="Controls",
    ),

"""Main analysis section with value boxes and plot output"""
    ui.h2("Attendance Analysis"),

    ui.layout_columns(
        ui.value_box(
            "Mean Attendance",
            ui.output_text("mean_attendance_output"),
        ),
        ui.value_box(
            "Std. Deviation",
            ui.output_text("std_attendance_output"),
        )
    ),

    ui.output_plot("attendance_plot")
)

"""Defining the server logic for the Shiny app"""
def server(input, output, session):
    """Reactive expression to filter data based on selected module"""
    @reactive.Calc
    def filtered_data():
        return shiny_df[shiny_df['Module Name'] == input.module_select()]
    
    """Outputting mean attendance"""
    @output
    @render.text
    def mean_attendance_output():
        mean_val = filtered_data()['Student Overall Attendance'].mean()
        return f"{mean_val:.2f}"
    
    """Outputting standard deviation of attendance"""
    @output
    @render.text
    def std_attendance_output():
        std_val = filtered_data()['Student Overall Attendance'].std()
        return f"{std_val:.2f}"
    
    """Rendering plot with filtered data"""
    @output
    @render.plot
    def attendance_plot():

        module_data = filtered_data() 
        
        daily_rate = module_data.groupby('Date')['Attended'].mean()

        plt.figure(figsize=(10, 6))
        daily_rate.plot(kind='line', marker='o', linestyle='-')
        
        plt.title(f'Daily Attendance Rate for {input.module_select()}')
        plt.xlabel('Date')
        plt.ylabel('Average Attendance Rate (0.0 to 1.0)')
        plt.ylim(0, 1.1)
        plt.grid(True)
        
app = App(app_ui, server)