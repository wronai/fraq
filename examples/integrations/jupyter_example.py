"""
Jupyter Notebook integration example for fraq.

Shows how to use fraq in Jupyter notebooks with visualizations.
"""

from __future__ import annotations

from IPython.display import display, HTML
import pandas as pd
import matplotlib.pyplot as plt

from fraq import generate, FraqSchema, infer_fractal


def jupyter_basic_usage():
    """Basic fraq usage in Jupyter."""
    # Generate data
    records = generate({
        'temperature': 'float:10-40',
        'humidity': 'float:30-80',
        'pressure': 'float:980-1020',
    }, count=100, seed=42)
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Display
    display(df.head(10))
    
    return df


def jupyter_visualization():
    """Visualize fraq data in Jupyter."""
    records = generate({
        'x': 'float:0-100',
        'y': 'float:0-100',
        'z': 'float:0-100',
    }, count=500, seed=42)
    
    df = pd.DataFrame(records)
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Scatter plot
    axes[0, 0].scatter(df['x'], df['y'], alpha=0.5, s=10)
    axes[0, 0].set_title('X vs Y')
    axes[0, 0].set_xlabel('X')
    axes[0, 0].set_ylabel('Y')
    
    # Histogram
    axes[0, 1].hist(df['z'], bins=30, alpha=0.7)
    axes[0, 1].set_title('Z Distribution')
    axes[0, 1].set_xlabel('Z')
    
    # Line plot
    axes[1, 0].plot(df['x'][:100])
    axes[1, 0].set_title('X First 100 Values')
    
    # Box plot
    axes[1, 1].boxplot([df['x'], df['y'], df['z']], labels=['X', 'Y', 'Z'])
    axes[1, 1].set_title('Value Distributions')
    
    plt.tight_layout()
    plt.show()
    
    return df


def jupyter_interactive_widget():
    """Interactive widget for fraq in Jupyter."""
    try:
        from ipywidgets import interact, IntSlider, FloatSlider
        
        @interact(
            count=IntSlider(min=10, max=1000, step=10, value=100),
            temp_min=FloatSlider(min=0, max=50, value=10),
            temp_max=FloatSlider(min=50, max=100, value=40),
        )
        def interactive_generate(count, temp_min, temp_max):
            records = generate({
                'temperature': f'float:{temp_min}-{temp_max}',
                'humidity': 'float:0-100',
            }, count=count, seed=42)
            
            df = pd.DataFrame(records)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df['temperature'], label='Temperature')
            ax.plot(df['humidity'], label='Humidity', alpha=0.7)
            ax.set_title(f'Generated Data (n={count})')
            ax.legend()
            plt.show()
            
            display(df.describe())
    
    except ImportError:
        print("ipywidgets not installed. Run: pip install ipywidgets")


def jupyter_fractal_analysis():
    """Analyze fractal patterns in generated data."""
    from fraq.inference import infer_fractal
    
    # Generate hierarchical data
    records = generate({
        'level_1': 'float:0-1',
        'level_2': 'float:0-0.5',
        'level_3': 'float:0-0.25',
    }, count=200, seed=42)
    
    # Infer fractal schema
    schema = infer_fractal(records)
    
    # Display patterns
    print("Detected Patterns:")
    for col, pattern in schema.patterns.items():
        print(f"  {col}: {pattern.pattern_type} (depth={pattern.depth})")
    
    # Visualize
    df = pd.DataFrame(records)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for i, col in enumerate(['level_1', 'level_2', 'level_3']):
        axes[i].hist(df[col], bins=20, alpha=0.7)
        axes[i].set_title(f'{col} Distribution')
    
    plt.tight_layout()
    plt.show()
    
    return schema


if __name__ == "__main__":
    print("This script is designed for Jupyter notebooks.")
    print("Copy the functions into notebook cells.")
