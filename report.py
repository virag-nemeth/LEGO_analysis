# report.py
import os
from analysis import *
from fpdf import FPDF
import matplotlib.pyplot as plt

# Create a folder to store plot images
#IMG_DIR = "report_images"
#os.makedirs(IMG_DIR, exist_ok=True)

# Helper function to save a plot to image
def save_plot(filename):
    path = os.path.join(IMG_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

# Create and configure PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 7, "LEGO Sets Analysis Report", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def add_paragraph(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 4, text)
        self.ln(5)

    def add_image(self, image_path, width=180):
        self.image(image_path, w=width)
        self.ln(10)
        
    def add_table(self, data, col_widths=None):
        self.set_font("Arial", "", 10)
        line_height = self.font_size * 2.5

        if col_widths is None:
            col_widths = [40] * len(data[0])

        for row in data:
            for datum, width in zip(row, col_widths):
                self.cell(width, line_height, str(datum), border=1)
            self.ln(line_height)

def main():
    merged = load_data()
    pdf = PDF()
    pdf.add_page()

    # --- Star Wars Analysis ---
    pdf.chapter_title("Star Wars Sets")
    sw_percentage, star_wars = calc_star_wars_percentage(merged)
    sw_peak_year = calc_peak_star_wars_year(star_wars)
    pdf.add_paragraph(f"Percentage of licensed sets that are Star Wars: {sw_percentage}%.")
    pdf.add_paragraph(f"Year with the most Star Wars sets released: {sw_peak_year}.")

    # --- Sets Over Time ---
    pdf.chapter_title("Set Release Over Time")
    plot_sets_over_time(merged)
    pdf.add_image(os.path.join('images', "sets_over_time.png"))

    # --- Top 5 Parent Themes ---
    pdf.chapter_title("Top 5 Most Common Parent Themes")
    top_themes = calc_top_themes_by_set_count(merged)
    #pdf.add_paragraph(top_themes.to_string(index=False))
    top_themes_table = [top_themes.columns.tolist()] + top_themes.values.tolist()
    col_widths = [60, 40, 40] 
    pdf.add_table(top_themes_table, col_widths=col_widths)
    plot_top_themes(top_themes)
    pdf.add_image(os.path.join('images', "top_themes.png"))

    # --- Licensed Sets Percentage ---
    pdf.chapter_title("Licensed Sets Percentage")
    licensed_counts, licensed_percentage = calc_licensed_percentage(merged)
    pdf.add_paragraph(f"Licensed sets account for {licensed_percentage}% of all LEGO sets.")
    plot_licenses_percentage(licensed_counts)
    pdf.add_image(os.path.join('images', "licensed_percentage.png"))

    # --- Licensed Themes with Most Sets ---
    pdf.chapter_title("Licensed Themes with the Most Sets")
    licensed_themes = calc_licensed_highest_sets(merged)
    licensed_themes_table = [licensed_themes.columns.tolist()] + licensed_themes.values.tolist()
    col_widths = [60, 40, 40] 
    pdf.add_table(licensed_themes_table, col_widths=col_widths)
    plot_licensed_highest_sets(licensed_themes)
    pdf.add_image(os.path.join('images', "licensed_highest.png"))

    # --- Set Count Trends for Top 5 Themes ---
    pdf.chapter_title("Set Count Trends for Top 5 Themes")
    top5_themes_data = calc_set_count_for_top_themes(merged)
    plot_set_count_for_top_themes(top5_themes_data)
    pdf.add_image(os.path.join('images', "top5_trends.png"))

    # --- Licensed vs Non-Licensed Sets Over Time ---
    pdf.chapter_title("Licensed vs Non-Licensed Sets Over Time")
    licensed_trends = calc_licensed_non_licensed_sets(merged)
    plot_licensed_non_licensed_sets(licensed_trends)
    pdf.add_image(os.path.join('images', "licensed_trend.png"))

    # --- Box Plot: Set Size Comparison ---
    pdf.chapter_title("Set Size Comparison (Boxplot)")
    box_plot_set_comparison_licensed_non_licensed(merged)
    pdf.add_image(os.path.join('images', "boxplot_comparison.png"))

    # --- Sub-themes in Top 3 Parent Themes ---
    pdf.chapter_title("Sub-themes in Top 3 Parent Themes")
    subtheme_counts = calc_subthemes_top_3_parent_themes(merged)
    plot_subthemes_top_3_parent_themes(subtheme_counts)
    pdf.add_image(os.path.join('images', "subthemes_top3.png"))
    
    # --- Set Size Distribution Across Sets ---
    pdf.chapter_title("Set Size Distribution Across Sets")
    merged_df = calc_distribution_set_sizes(merged)
    plot_distribution_set_sizes(merged_df)
    pdf.add_image(os.path.join('images', "distribution_set_sizes.png"))
    
    # --- Highest Number of Themes Introduced ---
    pdf.chapter_title("Highest Number of Themes Introduced")
    highest_num_themes, themes_per_year = calc_top_new_theme_year(merged)
    pdf.add_paragraph(f"The highest number of new themes was introduced in: {highest_num_themes.iloc[0,0]}.\n" )
    plot_top_new_theme_year(themes_per_year)
    pdf.add_image(os.path.join('images', "top_new_themes_year.png"))
    
    # --- Average Number of Parts for the Top 5 Themes Over Time ---
    pdf.chapter_title("Average Number of Parts for the Top 5 Themes Over Time")
    avg_part_trend = calc_set_compexity_top_themes(merged)
    plot_set_complexity_top_themes(avg_part_trend)
    pdf.add_image(os.path.join('images', "set_complexity_top_themes.png"))
    
    #--- Theme Popularity vs. Set Complexity ---
    pdf.chapter_title("Theme Popularity vs. Set Complexity")
    theme_stats = calc_theme_set_complexity_corr(merged)
    plot_theme_set_complexity_corr(theme_stats)
    pdf.add_image(os.path.join('images', "theme_set_complexity_corr.png"))

    # Save PDF
    output_pdf = "lego_analysis_report.pdf"
    pdf.output(output_pdf)
    print(f"\n Report saved as: {output_pdf}")

main()
