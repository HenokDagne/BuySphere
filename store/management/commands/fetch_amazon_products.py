import requests
import json
import random
import time
from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductVariation

# API Configuration
API_KEY = ""  # Replace with your actual API key
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
}
PRODUCT_ENDPOINT = "https://real-time-amazon-data.p.rapidapi.com/influencer-post-products"
VARIATION_ENDPOINT = "https://real-time-amazon-data.p.rapidapi.com/product/variations"  # Replace with the actual endpoint for variations

# Define color choices for variations
COLORS = ['Red', 'Blue', 'Green', 'Black', 'Yellow', 'White', 'Purple', 'Orange']

def ensure_utf8(data):
    """
    Ensure the data is UTF-8 encoded. If not, try to decode it correctly.
    """
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        # Try to decode with 'latin1' and then encode to 'utf-8'
        return data.decode('latin1').encode('utf-8').decode('utf-8')

def fetch_product_variations(product):
    """
    Fetches product variations from the API and stores them in the database.
    """
    product_id = product.asin  # Ensure ASIN exists
    if not product_id:
        print(f"Skipping product {product.name} (No ASIN found)")
        return

    params = {
        'asin': product_id,
        'country': 'US'
    }

    try:
        response = requests.get(VARIATION_ENDPOINT, headers=HEADERS, params=params)
        response.raise_for_status()  # Raise an error for HTTP errors
        variations_data = response.json().get('variations', [])[:4]  # Limit to 4 variations

        if not variations_data:
            print(f"No variations found for {product.name}")
            return

        for variation in variations_data:
            color = variation.get('color', random.choice(COLORS))  # Use API color or random color
            additional_price = variation.get('price', random.uniform(0.0, 20.0))
            stock = random.randint(1, 20)

            variation_obj, created = ProductVariation.objects.get_or_create(
                product=product,
                color=color,
                image=variation.get('image', ''),
                additional_price=additional_price,
                stock=stock
            )
            print(f"Variation {color} for {product.name} - Created: {created}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch variations for {product.name}: {e}")

class Command(BaseCommand):
    help = 'Fetch products from Amazon API via RapidAPI and store them in the database'

    def handle(self, *args, **kwargs):
        api_key = API_KEY  # Replace with your actual RapidAPI key
        endpoint = PRODUCT_ENDPOINT  # Replace with the actual endpoint
        headers = HEADERS

        categories = {
            'phone': {'name': 'Phones', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\phone.jpg'},
            'laptop': {'name': 'Laptops', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\Brand New MSI GE66 RAIDER Steel Series.jpg'},
            'clothing': {'name': 'Clothing', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\t shirt.webp'},
            'watch': {'name': 'Watches', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\watch.jpg'},
            'shoes': {'name': 'Shoes', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\shoz.jpg'},
            'videogame': {'name': 'Video Games', 'image': 'C:\\Users\\hp\\OneDrive\\Desktop\\Ecommerce_image\\vdieogame.jpg'},
        }

        for keyword, category_info in categories.items():
            params = {
                'influencer_name': 'madison.lecroy',  # Replace with the actual influencer name
                'post_id': 'amzn1.ideas.382NVFBNK3GGQ'  # Replace with the actual post ID
            }

            # Print the full URL being requested
            full_url = f"{endpoint}?influencer_name={params['influencer_name']}&post_id={params['post_id']}"
            print(f"Requesting URL: {full_url}")

            response = requests.get(endpoint, headers=headers, params=params)
            if response.status_code == 403:
                print(f"Failed to fetch data for keyword: {keyword}, Status Code: {response.status_code} - Forbidden. Check your API key and permissions.")
                continue
            elif response.status_code == 429:
                print(f"Failed to fetch data for keyword: {keyword}, Status Code: {response.status_code} - Too Many Requests. Waiting for 60 seconds before retrying.")
                time.sleep(60)  # Wait for 60 seconds before retrying
                response = requests.get(endpoint, headers=headers, params=params)
                if response.status_code != 200:
                    print(f"Failed to fetch data for keyword: {keyword}, Status Code: {response.status_code} after retrying.")
                    continue

            if response.status_code != 200:
                print(f"Failed to fetch data for keyword: {keyword}, Status Code: {response.status_code}")
                continue

            raw_data = response.content
            data = ensure_utf8(raw_data)
            try:
                products = json.loads(data).get('data', {}).get('products', [])[:10]  # Limit to 10 products
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON for keyword: {keyword}, Error: {e}")
                print(f"Raw response data: {data}")
                continue

            if not products:
                print(f"No products found for keyword: {keyword}")
                print(f"Raw response data: {data}")
                continue

            # Print the fetched data in JSON format
            print(f"Fetched data for keyword '{keyword}':")
            print(json.dumps(products, indent=4))

            for product_data in products:
                print(f"Processing product: {product_data['product_title']}")  # Debug statement
                category, created = Category.objects.get_or_create(
                    name=category_info['name'],
                    slug=category_info['name'].lower().replace(' ', '-'),
                    defaults={'image': category_info['image']}
                )
                print(f"Category: {category.name}, Created: {created}")  # Debug statement

                product, created = Product.objects.get_or_create(
                    name=product_data['product_title'],
                    description='',  # Description is not provided in the response
                    category=category,
                    image=product_data.get('product_url', ''),
                    stock=10,  # Example stock value
                    price=float(product_data['product_price'].replace('$', '').replace(',', '')) if product_data['product_price'] else 0.0,
                    asin=product_data['asin']  # Set the ASIN field
                )
                print(f"Product: {product.name}, Created: {created}")  # Debug statement

                # Fetch and create product variations
                fetch_product_variations(product)

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored products from Amazon API via RapidAPI'))