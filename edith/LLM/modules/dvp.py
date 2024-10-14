import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QMessageBox, QMainWindow, QVBoxLayout,
    QWidget, QComboBox, QPushButton, QCheckBox
)
import random

class PlotViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Set dark theme for the application
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

        # Create a FigureCanvas to display Matplotlib plots
        self.canvas = FigureCanvas(plt.Figure())
        self.layout.addWidget(self.canvas)

        # Create a placeholder text for the graph
        self.placeholder_text = self.canvas.figure.text(
            0.5, 0.5, "Graph will be displayed here..",
            fontsize=16, ha='center', va='center', color='white'
        )

        # Set dark background for the canvas
        self.canvas.figure.patch.set_facecolor('#2e2e2e')

        # Combo box for graph type selection
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Scatter Plot", "Line Plot", "Bar Plot", "Histogram", "Box Plot"])
        self.layout.addWidget(self.graph_type_combo)

        # Checkbox for 3D plotting option
        self.three_d_checkbox = QCheckBox("Enable 3D Plot")
        self.layout.addWidget(self.three_d_checkbox)

        # Button to select file
        self.file_button = QPushButton("Select Data File")
        self.file_button.clicked.connect(self.load_data_file)
        self.layout.addWidget(self.file_button)

        # Button to generate plot
        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.generate_plot)
        self.layout.addWidget(self.plot_button)

        # Define a color scheme
        self.color_scheme = ['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FFC300']

    def load_data_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", 
            "CSV files (*.csv);;Text files (*.txt);;"
            "Excel files (*.xlsx *.xls);;"
            "JSON files (*.json);;"
            "Parquet files (*.parquet);;"
            "Feather files (*.feather);;"
            "All Files (*)",
            options=options)

        if file_path:
            self.load_file(file_path)

    def load_data(self, file_path):
        """Load data from various file types."""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.txt'):
                return pd.read_csv(file_path, sep='\t')
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                return pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            elif file_path.endswith('.parquet'):
                return pd.read_parquet(file_path)
            elif file_path.endswith('.feather'):
                return pd.read_feather(file_path)
            else:
                raise ValueError("Unsupported file type.")
        except Exception as e:
            raise RuntimeError(f"Error loading data: {e}")

    def generate_plot(self):
        """Generate a plot based on the selected type."""
        if not hasattr(self, 'df'):
            QMessageBox.warning(self, "Warning", "No data loaded. Please select a file first.")
            return
        
        plot_type = self.graph_type_combo.currentText()
        numeric_cols = self.df.select_dtypes(include='number').columns.tolist()

        if len(numeric_cols) < 2:
            QMessageBox.critical(self, "Error", "Not enough numerical columns to create a plot.")
            return
        
        x_column, y_column = numeric_cols[0], numeric_cols[1]

        self.canvas.figure.clear()  # Clear the canvas for the new plot
        ax = self.canvas.figure.add_subplot(111, projection='3d' if self.three_d_checkbox.isChecked() else None)

        # Set dark background for the plot
        ax.set_facecolor('#2e2e2e')
        self.canvas.figure.patch.set_facecolor('#2e2e2e')

        # Select a random color from the color scheme
        color = random.choice(self.color_scheme)

        if plot_type == "Scatter Plot":
            ax.scatter(self.df[x_column], self.df[y_column], color=color)
            ax.set_title(f'Scatter Plot: {y_column} vs {x_column}', color='white')
        elif plot_type == "Line Plot":
            ax.plot(self.df[x_column], self.df[y_column], color=color)
            ax.set_title(f'Line Plot: {y_column} vs {x_column}', color='white')
        elif plot_type == "Bar Plot":
            ax.bar(self.df[x_column], self.df[y_column], color=color)
            ax.set_title(f'Bar Plot: {y_column} vs {x_column}', color='white')
        elif plot_type == "Histogram":
            ax.hist(self.df[x_column], bins=30, color=color)
            ax.set_title(f'Histogram of {x_column}', color='white')
        elif plot_type == "Box Plot":
            ax.boxplot([self.df[y_column][self.df[x_column] == x] for x in self.df[x_column].unique()],
                       labels=self.df[x_column].unique())
            ax.set_title(f'Box Plot: {y_column} by {x_column}', color='white')

        # Set labels and colors
        ax.set_xlabel(x_column, color='white')
        ax.set_ylabel(y_column, color='white')
        ax.tick_params(colors='white')  # Change tick color to white
        
        # Add grid lines
        ax.grid(True, color='grey', linestyle='--', linewidth=0.5)

        # Set the viewing angle for 3D plots
        if self.three_d_checkbox.isChecked():
            ax.view_init(elev=20, azim=30)  # Adjust these values as needed

        self.canvas.draw()  # Render the new plot

    def load_file(self, file_path):
        """Load data and prepare for plotting."""
        try:
            self.df = self.load_data(file_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            QMessageBox.information(self, "Success", "Data loaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

def dvp():
    app = QApplication(sys.argv)
    viewer = PlotViewer()
    viewer.show()
    sys.exit(app.exec_())
