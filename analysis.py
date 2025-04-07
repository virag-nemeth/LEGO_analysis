# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

IMG_DIR = "images" 
os.makedirs(IMG_DIR, exist_ok=True)


# Read data from CSV files into pandas DataFrames
def load_data():
    """Load and merge LEGO set data with parent theme data. Returns the merged DataFrame."""
    lego_sets = pd.read_csv('/Users/viragnemeth/Projects/Python/LEGO_analysis/lego_sets.csv')
    parent_themes = pd.read_csv('/Users/viragnemeth/Projects/Python/LEGO_analysis/parent_themes.csv')

    # Merge the LEGO sets data with the parent themes data based on the 'parent_theme' column
    merged = lego_sets.merge(parent_themes, how= 'inner', left_on = 'parent_theme', right_on='name', suffixes=('_ls', '_pt'))
    return merged

def calc_star_wars_percentage(merged):
    """What percentage of all licensed sets ever released were Star Wars themed?"""
    licensed = merged[merged['is_licensed'] == True] # Filter out only licensed sets
    star_wars = licensed[licensed['parent_theme'] == 'Star Wars'] # Filter Star Wars licensed sets
    the_force = round((len(star_wars) / len(licensed)) * 100, 2)  # Calculate the percentage of Star Wars themed sets
    return the_force, star_wars

def calc_peak_star_wars_year(star_wars):
    """In which year was the highest number of Star Wars sets released?"""
    new_era = int(star_wars.groupby('year').size().sort_values(ascending=False).index[0])
    return new_era

def plot_sets_over_time(merged):
    """How has the number of LEGO sets released changed over time?"""
    sets_yearly = merged.groupby('year').size().reset_index(name='count')

    # Plot the number of LEGO sets released over time (line plot)
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sets_yearly, x='year', y='count', marker='o', palette='#294c60')
    plt.title('Number of Lego Sets Released Over Time (1950-2017)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Years', fontsize=12, fontweight='bold')
    plt.ylabel('Number of sets', fontsize=12, fontweight='bold')
    plt.yticks(range(0,800,50))
    plt.xticks(range(1945,2025,5), rotation=45)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "sets_over_time.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_top_themes_by_set_count(merged):
    """What are the top 5 most common parent themes in terms of the number of sets released?"""
    themes_by_set = merged.groupby('parent_theme')['set_num'].count().sort_values(ascending=False).reset_index().head(5)
    return themes_by_set

def plot_top_themes(themes_by_set):
    """Plot the top 5 most common parent themes (bar plot)"""
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 4))
    sns.barplot(data=themes_by_set, x='parent_theme', y='set_num', palette='pastel')
    plt.title('The 5 most common themes based on the number of sets released', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Parent Themes', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylabel('Number of sets', fontsize=12, fontweight='bold')
    plt.yticks(range(0,1200,100))
    plt.grid(True, linestyle="--", alpha=0.5)

    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "top_themes.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_licensed_percentage(merged):
    """What percentage of all LEGO sets are from licensed themes?"""
    prop_licensed = int((merged[merged['is_licensed'] == True].shape[0] / merged.shape[0]) * 100)
    #print(f"{prop_licensed}% of the LEGO sets are licensed.")
    licensed_counts = merged['is_licensed'].value_counts().to_list()
    return licensed_counts, prop_licensed

def plot_licenses_percentage(licensed_counts):
    """Plot the percentage of licensed vs non-licensed sets (pie chart)"""
    plt.figure(figsize=(5, 5))
    plt.pie(x=licensed_counts, labels=['Not Licensed', 'Licensed'], autopct='%1.1f%%', colors=['#3a8aa5', '#ffc49b'], startangle=90, wedgeprops={'edgecolor': 'black'})
    plt.title('Percentage of Licensed vs. Non-Licensed LEGO Sets', fontsize=14, fontweight='bold', pad=15)
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "licensed_percentage.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_licensed_highest_sets(merged):
    """Which licensed themes have the highest number of sets?"""
    licensed = merged[merged['is_licensed'] == True]
    licensed_themes = licensed.groupby('parent_theme')['set_num'].count().sort_values(ascending=False).reset_index().head(10)
    return licensed_themes

def plot_licensed_highest_sets(licensed_themes):
    """Plot the licensed themes with the highest number of sets (bar plot)"""
    ten_colours = ['#001219', '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702', '#bb3e03', '#ae2012', '#9b2226']
    plt.figure(figsize=(12, 6))
    sns.barplot(data=licensed_themes, x='parent_theme', y='set_num', palette=ten_colours)

    plt.title('Licensed Themes with the Highest Number of Sets', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Parent Themes', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Number of Sets', fontweight='bold')
    plt.yticks(range(10,615,20))
    plt.grid(True, linestyle="--", alpha=0.5)
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "licensed_highest.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_set_count_for_top_themes(merged):
    """How has the number of sets of the top 5 parent themes changed over time?"""
    themes_by_set_year = merged.groupby(['parent_theme', 'year'])['set_num'].count().reset_index().sort_values(by=['year', 'set_num'], ascending=[True, False])

    # Add a new column to hold the total number of sets for each parent theme
    themes_by_set_year['theme_count'] = themes_by_set_year.groupby('parent_theme')['set_num'].transform('sum')

    # Sort data by theme count and year
    sorted_df = themes_by_set_year.sort_values(by=['theme_count', 'year'], ascending=[False, True])

    # Extract the top 5 themes
    top_5_themes = themes_by_set_year['parent_theme'].unique()[:5]
    top_5_themes_data = themes_by_set_year[themes_by_set_year['parent_theme'].isin(top_5_themes)]
    return top_5_themes_data

def plot_set_count_for_top_themes(top_5_themes_data):
    """Plot the change in the number of sets for the top 5 themes (line plot)"""
    sns.set_style("whitegrid")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=top_5_themes_data, x='year', y='set_num', hue='parent_theme', marker='o')

    plt.title('Number of LEGO Sets Released by Top 5 Parent Themes Over Time', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Sets', fontsize=12, fontweight='bold')
    plt.xticks(range(1945,2025,5), rotation=45)
    plt.yticks(range(0,110,10))
    plt.legend(title='Parent Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "top5_trends.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_licensed_non_licensed_sets(merged):
    """What are the trends in licensed vs. non-licensed LEGO sets over the years? (Stacked Bar Chart or Line Chart)"""
    licensed_trends = merged.groupby(['year', 'is_licensed'])['set_num'].count().reset_index()

    # Pivot the data to create a stacked bar chart
    licensed_trends_pivot = licensed_trends.pivot(index='year', columns='is_licensed', values='set_num')
    licensed_trends_pivot.columns = ['Non-Licensed', 'Licensed']
    return licensed_trends_pivot

def plot_licensed_non_licensed_sets(licensed_trends_pivot):
    """Plot the trends (stacked bar chart)"""
    plt.figure(figsize=(16, 8))
    licensed_trends_pivot.plot(kind='bar', stacked=True, color=['#ee6c4d', '#98c1d9'], figsize=(14, 7))

    plt.title('Trends in Licensed vs. Non-Licensed LEGO Sets Over the Years', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Sets', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(range(0,750,50))
    plt.legend(title='Set Type', loc='upper left', labels=['Non-Licensed', 'Licensed'])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "licensed_trend.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def box_plot_set_comparison_licensed_non_licensed(merged):
    """Do licensed LEGO sets tend to have more parts compared to non-licensed ones?"""
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=merged, x='is_licensed', y='num_parts', palette='pastel')
    plt.title('Licensed vs. Non-Licensed Set Sizes')
    plt.xlabel('Is Licensed')
    plt.ylabel('Number of Parts')
    plt.ylim(0, merged['num_parts'].quantile(0.95))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "boxplot_comparison.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_subthemes_top_3_parent_themes(merged):
    """What are the most common sub-themes within the top 3 parent themes?"""
    top3_themes = merged['parent_theme'].value_counts().head(3).index.tolist()
    top3_data = merged[merged['parent_theme'].isin(top3_themes)]

    # Calculate the count of sets for each sub-theme within the top 3 themes
    subtheme_counts = (top3_data.groupby(['parent_theme', 'theme_name'])['set_num'].count().reset_index(name='set_count'))
    return subtheme_counts

def plot_subthemes_top_3_parent_themes(subtheme_counts):
    """Plot the sub-themes (bar plot)"""
    plt.figure(figsize=(16, 7))
    sns.barplot(data=subtheme_counts, x='theme_name', y='set_count', hue='parent_theme', palette=['#219ebc', '#023047', '#ffb703'])
    plt.title('Most Common Sub-themes in Top 3 Parent Themes', fontsize=14, fontweight='bold')
    plt.xlabel('Sub-themes', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Sets', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(range(0,250,20))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.legend(title='Parent Theme')
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "subthemes_top3.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_distribution_set_sizes(merged):
    """What is the distribution of set sizes (number of parts) across all sets?"""
    if 'num_parts' in merged.columns:
        merged_df = merged.dropna(subset=['num_parts']) # Drop rows with missing 'num_parts' values
    else:
        raise ValueError("'num_parts' column not found in the merged dataset.")
    return merged_df

def plot_distribution_set_sizes(merged_df):
    """Plot the distribution of set sizes (histogram with KDE)"""
    plt.figure(figsize=(12, 6))
    sns.histplot(data=merged_df, x='num_parts', bins=50, kde=True, color='#0f392b')

    plt.title('Distribution of LEGO Set Sizes (Number of Parts)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Parts', fontweight='bold')
    plt.ylabel('Number of Sets', fontweight='bold')
    plt.yticks(range(0,5500,500))
    plt.xticks(range(0,700,50))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(0, merged_df['num_parts'].quantile(0.95))
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "distribution_set_sizes.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_top_new_theme_year(merged):
    """Which year had the highest number of new themes introduced?"""
    new_themes = merged.drop_duplicates(subset=['parent_theme', 'year'])  # Remove duplicates by year and theme
    themes_per_year = new_themes.groupby('year')['parent_theme'].nunique().reset_index(name='new_themes')
    highest_num_themes = themes_per_year.sort_values(by='new_themes', ascending=False).head(1)
    #print(highest_num_themes)
    return highest_num_themes, themes_per_year

def plot_top_new_theme_year(themes_per_year):
    """Plot the years with the highest number of new themes (bar plot)"""
    plt.figure(figsize=(16, 8))
    sns.barplot(data=themes_per_year, x='year', y='new_themes', color='#155e8d')
    plt.title('New Themes Introduced per Year', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year', fontweight='bold')
    plt.ylabel('Number of New Themes', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(range(0,40,2))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "top_new_themes_year.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_set_compexity_top_themes(merged):
    """What are the trends in LEGO set complexity (average number of parts) for the top 5 themes over time?"""
    top5_themes = merged['parent_theme'].value_counts().head(5).index
    top5_data = merged[merged['parent_theme'].isin(top5_themes)]
    avg_parts_trend = top5_data.groupby(['year', 'parent_theme'])['num_parts'].mean().reset_index()
    return avg_parts_trend

def plot_set_complexity_top_themes(avg_parts_trend):
    """Plot the trends in LEGO set complexity (average number of parts) for the top 5 themes over time"""
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=avg_parts_trend, x='year', y='num_parts', hue='parent_theme', linewidth=2, marker='o', palette=['#8ecae6', '#219ebc', '#023047', '#ffb703', '#fb8500'])
    plt.title('Average Number of Parts in Sets (Top 5 Themes Over Time)',  fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year', fontweight='bold')
    plt.ylabel('Average Number of Parts', fontweight='bold')
    plt.yticks(range(0,1200,100))
    plt.xticks(range(1975,2020,3))
    plt.legend(title='Parent Theme')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "set_complexity_top_themes.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def calc_theme_set_complexity_corr(merged):
    """How does the number of sets per theme correlate with the number of parts per set?"""
    theme_stats = merged.groupby('parent_theme').agg(total_sets=('set_num', 'count'),avg_parts=('num_parts', 'mean')).reset_index()
    return theme_stats

def plot_theme_set_complexity_corr(theme_stats):
    """Plot the number of sets per theme and its correlattion with the number of parts per set"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=theme_stats, x='total_sets', y='avg_parts', hue='total_sets', palette='coolwarm', size='total_sets', sizes=(50, 200))
    plt.title('Theme Popularity vs. Set Complexity', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Sets', fontweight='bold')
    plt.ylabel('Average Parts Per Set', fontweight='bold')
    plt.xticks(range(0,700,50))
    plt.yticks(range(0,700,50))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.ylim((0, theme_stats['avg_parts'].quantile(0.95)))
    plt.legend(title='Total Sets')
    plt.tight_layout()
    
    # Save plot 
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    path = os.path.join(IMG_DIR, "theme_set_complexity_corr.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

