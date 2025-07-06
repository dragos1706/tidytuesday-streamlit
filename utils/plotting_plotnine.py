from plotnine import ggplot, aes, geom_histogram, geom_boxplot, geom_point, geom_bar, geom_line, labs, theme_minimal
import matplotlib.pyplot as plt

def plotnine_histogram(df, column):
    p = (
        ggplot(df, aes(x=column)) +
        geom_histogram(bins=30, fill='steelblue', color='white') +
        theme_minimal() +
        labs(title=f"Histogram of {column}")
    )
    return p.draw()

def plotnine_boxplot(df, x_col, y_col):
    p = (
        ggplot(df, aes(x=x_col, y=y_col)) +
        geom_boxplot() +
        theme_minimal() +
        labs(title=f"Boxplot of {y_col} by {x_col}")
    )
    return p.draw()

def plotnine_scatter(df, x_col, y_col):
    p = (
        ggplot(df, aes(x=x_col, y=y_col)) +
        geom_point(alpha=0.7) +
        theme_minimal() +
        labs(title=f"Scatter Plot of {y_col} vs {x_col}")
    )
    return p.draw()

def plotnine_bar_chart(df, category_col):
    p = (
        ggplot(df, aes(x=category_col)) +
        geom_bar(fill='skyblue') +
        theme_minimal() +
        labs(title=f"Bar Chart of {category_col}")
    )
    return p.draw()

def plotnine_line_chart(df, x_col, y_col):
    p = (
        ggplot(df, aes(x=x_col, y=y_col)) +
        geom_line() +
        theme_minimal() +
        labs(title=f"Line Chart of {y_col} over {x_col}")
    )
    return p.draw()
