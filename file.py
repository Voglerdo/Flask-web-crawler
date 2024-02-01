from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    driver = webdriver.Chrome()

    # Navigate to the URL
    url = 'https://www.foodbooking.com/ordering/restaurant/menu?restaurant_uid=9c1be368-be49-4568-8038-1c338b9a7fc6&client_is_mobile=true&return_url=https%3A%2F%2Fkerasusfood.com%2F'
    driver.get(url)

    # Wait for the page to load (adjust wait time as needed)
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'm-item-name')))
    except:
        return jsonify({"error": "Timeout waiting for page to load"})

    # Extract all spans
    all_spans = driver.find_elements(By.TAG_NAME, 'span')
    span_texts = [span.text for span in all_spans]

    # Extract all <div> elements with class "m-item-name"
    all_divs = driver.find_elements(By.CLASS_NAME, 'm-item-name')
    div_texts = [div.text for div in all_divs]

    # Close the browser
    driver.quit()

    # Combine div_texts and span_texts into a 2D array
    combined_2d_array = list(zip(div_texts, span_texts))

    # Return the 2D array as JSON with explicit encoding
    response = jsonify({'data': combined_2d_array})
    response.charset = 'utf-8'

    return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
