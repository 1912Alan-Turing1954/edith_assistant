import pandas as pd
import plotly.express as px
import os

def load_data(file_path):
    """Load data from various file types."""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.txt'):
            return pd.read_csv(file_path, sep='\t')  # Assuming tab-separated values
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        elif file_path.endswith('.parquet'):
            return pd.read_parquet(file_path)
        elif file_path.endswith('.feather'):
            return pd.read_feather(file_path)
        elif file_path.endswith('.html'):
            return pd.read_html(file_path)[0]  # Read first table found in HTML
        elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
            import sqlite3
            conn = sqlite3.connect(file_path)
            return pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table';", conn)  # Replace with actual query
        elif file_path.endswith('.h5'):
            return pd.read_hdf(file_path)
        elif file_path.endswith('.sas7bdat'):
            from sas7bdat import SAS7BDAT
            with SAS7BDAT(file_path) as file:
                return file.to_data_frame()
        elif file_path.endswith('.dta'):
            return pd.read_stata(file_path)
        else:
            raise ValueError("Unsupported file type.")
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def filter_data(df):
    """Filter data based on user input."""
    print("Available columns for filtering:")
    print(df.columns.tolist())
    
    filter_column = input("Enter the column name to filter by: ")
    if filter_column not in df.columns:
        print("Invalid column name. No filtering applied.")
        return df
    
    filter_value = input(f"Enter the value to filter {filter_column} by: ")
    
    filtered_df = df[df[filter_column] == filter_value]
    print(f"Filtered data shape: {filtered_df.shape}")
    return filtered_df

def visualize_data(df, x_column, y_column, plot_type, z_column=None):
    """Create interactive visualizations based on the user's choice."""
    if plot_type == 'scatter':
        fig = px.scatter(df, x=x_column, y=y_column, title=f'Scatter Plot: {y_column} vs {x_column}')
    elif plot_type == 'bar':
        fig = px.bar(df, x=x_column, y=y_column, title=f'Bar Plot: {y_column} vs {x_column}')
    elif plot_type == 'line':
        fig = px.line(df, x=x_column, y=y_column, title=f'Line Plot: {y_column} vs {x_column}')
    elif plot_type == 'hist':
        fig = px.histogram(df, x=y_column, title=f'Histogram of {y_column}')
    elif plot_type == 'box':
        fig = px.box(df, x=x_column, y=y_column, title=f'Box Plot: {y_column} by {x_column}')
    elif plot_type == '3dscatter':
        if z_column is None:
            print("3D Scatter plot requires a z-axis.")
            return
        fig = px.scatter_3d(df, x=x_column, y=y_column, z=z_column,
                            title=f'3D Scatter Plot: {y_column} vs {x_column} and {z_column}')

    fig.show()

    # Export option
    export_choice = input("Do you want to export this plot as an image? (yes/no): ")
    if export_choice.lower() == 'yes':
        file_format = input("Enter the file format (png/jpeg/pdf): ")
        fig.write_image(f'plot.{file_format}')
        print(f"Plot exported as plot.{file_format}")

def main():
    file_path = input("Enter the path to your file (.csv, .txt, .xlsx, .json, .parquet, .feather, .html, .sqlite, .h5, .sas7bdat, .dta): ")

    if not os.path.exists(file_path):
        print("File not found. Please check the path.")
        return

    try:
        df = load_data(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Filtering the data
        df = filter_data(df)

        print("Available columns after filtering:")
        print(df.columns.tolist())

        # Selecting x and y columns based on user input
        x_column = input("Enter the column name for the x-axis: ")
        y_column = input("Enter the column name for the y-axis: ")

        if x_column not in df.columns or y_column not in df.columns:
            print("Invalid column names. Please check your input.")
            return

        print("Choose a type of visualization:")
        print("1. Line Plot")
        print("2. Bar Plot")
        print("3. Scatter Plot")
        print("4. Histogram")
        print("5. Box Plot")
        print("6. 3D Scatter Plot")
        choice = input("Enter the number corresponding to your choice: ")

        plot_type_map = {
            '1': 'line',
            '2': 'bar',
            '3': 'scatter',
            '4': 'hist',
            '5': 'box',
            '6': '3dscatter'
        }

        plot_type = plot_type_map.get(choice)
        if not plot_type:
            print("Invalid choice.")
            return

        z_column = None
        if plot_type == '3dscatter':
            z_column = input("Enter the column name for the z-axis: ")
            if z_column not in df.columns:
                print("Invalid column name for z-axis.")
                return

        visualize_data(df, x_column, y_column, plot_type, z_column)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()