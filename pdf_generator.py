import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from datetime import datetime
import os
from text_report_generator import generate_report

def generate_pdf(report_data, origin):
    # Function to create a line chart for daily stats
    def create_daily_chart(daily_stats, stat_category, stat_measure, title, ylabel, ax):
        dates, values = [], []

        for stat in daily_stats:
            date = datetime.strptime(stat['date'], '%Y-%m-%d')
            if stat_category == 'count':
                # Direct extraction for count
                value = stat.get(stat_category)
            else:
                # Extracting the specific measure from the category in 'stats'
                value = stat.get('stats', {}).get(stat_category, {}).get(stat_measure)

            if value is not None:
                dates.append(date)
                values.append(value)

        ax.plot(dates, values, marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)

    # Function to create a bar chart for provinces
    def create_province_chart(provinces, key, title, ax):
        provinces_names = list(provinces.keys())
        values = [provinces[province]['stats'][key]['median'] for province in provinces_names]
        ax.bar(provinces_names, values, color='skyblue')
        ax.set_xlabel('Province')
        ax.set_ylabel(key.capitalize())
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)

    # Function to create a bar chart for agencies
    def create_agency_chart(agency_data, ax):
        agency_ids = [str(agency['agency_id']) for agency in agency_data]
        values = [agency['count'] for agency in agency_data]
        ax.bar(agency_ids, values, color='lightgreen')
        ax.set_xlabel('Agency ID')
        ax.set_ylabel('Total Price Value')
        ax.set_title('Top 20 Agencies by Listing Count')
        ax.tick_params(axis='x', rotation=45)

    daily_stats = report_data.get('daily_stats', [])
    provinces_data = report_data.get('provinces', {})
    agency_data = sorted(report_data.get('agency_stats', []), key=lambda x: x['count'], reverse=True)[:20]

    pdf_path = f'pdf/{origin}.pdf'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with matplotlib.backends.backend_pdf.PdfPages(pdf_path) as pdf:
        report_text = generate_report(report_data)

        # Add the text report to the first page of the PDF
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.05, 0.95, report_text, transform=ax.transAxes, fontsize=12, va='top', ha='left', linespacing=1.5)
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)

        # Daily stats charts
        if daily_stats:
            fig, ax = plt.subplots(figsize=(12, 6))
            create_daily_chart(daily_stats, 'count', None, 'Daily Listing Count', 'Count', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(12, 6))
            create_daily_chart(daily_stats, 'price', 'median', 'Daily Median Price', 'Median Price', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(12, 6))
            create_daily_chart(daily_stats, 'price', 'total', 'Daily Total Price', 'Total Price', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(12, 6))
            create_daily_chart(daily_stats, 'price_per_square_meter', 'median', 'Daily Median Square Per Meter Price', 'Median Price/Sq Meter', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(12, 6))
            create_daily_chart(daily_stats, 'area', 'median', 'Daily Median Area', 'Median Area', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

        # Province charts
        for key, title in [('price', 'Median Price'), ('area', 'Median Area'), ('price_per_square_meter', 'Median Price per Square Meter')]:
            fig, ax = plt.subplots(figsize=(12, 6))
            create_province_chart(provinces_data, key, f'{title} by Province', ax)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

        # Agency chart
        fig, ax = plt.subplots(figsize=(12, 6))
        create_agency_chart(agency_data, ax)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    print(f"PDF report generated: {pdf_path}")

# You may add more functions or modify the existing ones here as needed.
