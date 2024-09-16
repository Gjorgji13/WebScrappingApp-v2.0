import tempfile
from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from io import BytesIO, StringIO

app = Flask(__name__)


# Funkcija za chistenje na skrapiranite podatoci pred da bidat vneseni vo dokument.
def clean_data(data):
    if isinstance(data, list):
        cleaned_list = []
        seen = set()
        for item in data:
            if isinstance(item, list) or isinstance(item, dict):
                item_str = str(item)  # Convert mutable items to string for comparison
            else:
                item_str = item.strip() if isinstance(item, str) else item
            if item_str not in seen:
                cleaned_list.append(item)
                seen.add(item_str)
        return cleaned_list
    elif isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, str):
        return data.strip()
    return data


# Funkcija za skrapiranje na celiot website i vrakjanje na skrapiranite html elementi
def scrape_entire_webpage(url):
    try:
        print(f"Scraping URL: {url}")  # Debug print statement
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Debugging: Print the soup object to make sure the page is loaded
        print(soup.prettify()[:500000])  # Print first 500000 characters of the HTML

        elements = {
            "Title": soup.title.string if soup.title else "No title found",
            "Headers": {tag: [h.get_text(strip=True) for h in soup.find_all(tag)] for tag in
                        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']},
            "Paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
            "Images": [urljoin(url, img['src']) for img in soup.find_all('img') if 'src' in img.attrs],
            "Links": [(a.get_text(strip=True), urljoin(url, a['href'])) for a in soup.find_all('a', href=True)],
            "Lists": [[li.get_text(strip=True) for li in ul.find_all('li')] for ul in soup.find_all(['ul', 'ol'])],
            "Tables": [[cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])] for row in
                       soup.find_all('tr')],
            "Forms": [form.get_text(strip=True) for form in soup.find_all('form')],
            "Divs": [div.get_text(strip=True) for div in soup.find_all('div')],
        }

        # Clean data
        elements = clean_data(elements)

        # Debugging: Print the scraped elements
        print("Scraped elements:", elements)
        return elements

    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")  # Error handling
        return {"Error": f"Failed to retrieve data: {e}"}


# Function to convert scraped data into DataFrame
def convert_to_dataframe(elements):
    df_data = {}
    max_length = 0

    # Determine maximum length for each category to ensure alignment
    for key, value in elements.items():
        if isinstance(value, list):
            if value:  # Check if the list is not empty
                if isinstance(value[0], list):
                    max_length = max(max_length, len(value))
                else:
                    max_length = max(max_length, len(value))
            else:
                max_length = max(max_length, 0)  # Handle empty lists
        elif isinstance(value, dict):
            max_length = max(max_length, len(value))

    for key, value in elements.items():
        if isinstance(value, list):
            if value:  # Check if the list is not empty
                if isinstance(value[0], list):
                    # Flatten lists of lists for tables and lists
                    df_data[key] = [", ".join(v) if v else "" for v in value] + [''] * (max_length - len(value))
                else:
                    df_data[key] = value + [''] * (max_length - len(value))
            else:
                df_data[key] = [''] * max_length  # Handling empty lists
        elif isinstance(value, dict):
            df_data[key] = [", ".join(v) if isinstance(v, list) else v for v in value.values()] + [''] * (
                    max_length - len(value))
        else:
            df_data[key] = [value] + [''] * (max_length - 1)

    df = pd.DataFrame(df_data)
    print("DataFrame created:")
    print(df.head())  # Print the first few rows of the DataFrame for debugging
    return df


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle scraping and display results
@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    elements = scrape_entire_webpage(url)
    if "Error" in elements:
        return elements["Error"], 400

    return render_template('results.html', elements=elements, url=url)


# Route to display the content of a specific HTML element
@app.route('/element/<element_type>', methods=['GET'])
def show_element(element_type):
    url = request.args.get('url')
    elements = scrape_entire_webpage(url)
    element_content = elements.get(element_type, "No content found")
    return render_template('element.html', element_type=element_type, element_content=element_content)


# Route to handle searching for a specific HTML element
@app.route('/search', methods=['POST'])
def search():
    url = request.form.get('url')
    search_query = request.form.get('search_query', '').lower()

    if not url:
        return "No URL provided", 400

    elements = scrape_entire_webpage(url)
    filtered_elements = {key: value for key, value in elements.items() if
                         search_query in key.lower() or any(search_query in str(v).lower() for v in value)}

    return render_template('results.html', elements=filtered_elements, url=url)


# Route to download CSV
@app.route('/download_csv', methods=['POST'])
def download_csv():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    elements = scrape_entire_webpage(url)
    df = convert_to_dataframe(elements)

    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    output_bytes = BytesIO(output.getvalue().encode())
    output_bytes.seek(0)

    return send_file(output_bytes, mimetype='text/csv', as_attachment=True, download_name='scraped_data.csv')


# Route to download Excel
@app.route('/download_excel', methods=['POST'])
def download_excel():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    elements = scrape_entire_webpage(url)
    df = convert_to_dataframe(elements)

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        temp_file_path = temp_file.name
        with pd.ExcelWriter(temp_file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

    return send_file(temp_file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name='scraped_data.xlsx')


if __name__ == '__main__':
    app.run(debug=True)
