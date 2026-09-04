import json
import random
import re
from datetime import datetime, timedelta

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

authors = ["marcus-sterling", "elena-rostova", "julian-hayes", "sarah-jenkins", "david-choi"]

states = [
    "California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", 
    "Ohio", "Georgia", "North Carolina", "Michigan", "New Jersey", "Virginia", 
    "Washington", "Arizona", "Massachusetts", "Tennessee", "Indiana", "Missouri", 
    "Maryland", "Wisconsin", "Colorado", "Minnesota", "South Carolina", "Alabama", 
    "Louisiana", "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa", 
    "Nevada", "Arkansas", "Mississippi", "Kansas", "New Mexico", "Nebraska", 
    "Idaho", "West Virginia", "Hawaii", "New Hampshire", "Maine", "Rhode Island", 
    "Montana", "Delaware", "South Dakota", "North Dakota", "Alaska", "Vermont", 
    "Wyoming"
]

topics = [
    "The Ultimate Guide to Auto Transport in {state}",
    "How Much Does it Cost to Ship a Car to {state}?",
    "Top 5 Things to Know Before Shipping Your Car from {state}",
    "Enclosed vs. Open Carrier Transport: A {state} Perspective",
    "Seasonal Car Shipping: The Snowbird Route to {state}",
    "Moving to {state}? Here is How to Transport Your Vehicle Safely",
    "What You Need to Know About Classic Car Transport in {state}",
    "Avoiding Auto Transport Scams When Shipping to {state}",
    "Understanding Transport Insurance Requirements in {state}",
    "Why {state} is Seeing a Surge in Auto Transport Demand",
    "Military PCS Moves: Shipping Your Vehicle to {state}",
    "Buying a Car Out of State and Shipping it to {state}",
    "Heavy Equipment and Oversized Vehicle Transport in {state}",
    "Door-to-Door Auto Transport Explained for {state} Residents",
    "How Weather in {state} Impacts Auto Transport Times",
    "The Future of Electric Vehicle (EV) Transport in {state}",
    "Top Auto Transport Routes Originating from {state}",
    "Preparing Your Vehicle for Transport to {state}",
    "What to Expect During the Vehicle Inspection Process in {state}",
    "How to Choose the Best Auto Transport Company in {state}"
]

background_images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Car_carrier_trailer_in_transit.jpg/1200px-Car_carrier_trailer_in_transit.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Truck_on_Highway.jpg/1200px-Truck_on_Highway.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Interstate_15_in_Utah.jpg/1200px-Interstate_15_in_Utah.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Open_car_carrier.jpg/1200px-Open_car_carrier.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Highway_in_the_US.jpg/1200px-Highway_in_the_US.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Semi-trailer_truck_on_highway.jpg/1200px-Semi-trailer_truck_on_highway.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Car_transporter.jpg/1200px-Car_transporter.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/US_Highway_50_Nevada.jpg/1200px-US_Highway_50_Nevada.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Highway_traffic_at_sunset.jpg/1200px-Highway_traffic_at_sunset.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Truck_driving_at_dawn.jpg/1200px-Truck_driving_at_dawn.jpg"
]

content_paragraphs = [
    "When considering auto transport, it's crucial to understand the logistics involved. Many consumers don't realize the complexity of coordinating a carrier across state lines, dealing with weigh stations, and adhering to strict FMCSA regulations.",
    "Cost is often the primary concern for anyone shipping a vehicle. Prices fluctuate based on fuel costs, driver availability, seasonality, and the specific route. Always ensure you receive a transparent quote with no hidden fees.",
    "Open carrier transport is the industry standard and the most cost-effective option. It is the same method used by manufacturers to deliver new cars to dealerships. However, your vehicle will be exposed to the elements.",
    "For luxury, classic, or highly modified vehicles, enclosed transport is highly recommended. It offers protection from weather, road debris, and provides peace of mind via higher insurance coverage limits.",
    "Preparation is key. Before handing your keys over, document the condition of your vehicle thoroughly. Take clear, well-lit photos from multiple angles, remove all personal items, and ensure the gas tank is only a quarter full.",
    "The auto transport industry sees massive seasonal shifts. The 'Snowbird' season causes prices and demand to spike along North-to-South routes in the fall, and South-to-North routes in the spring. Booking early is essential during these times.",
    "Beware of 'bait-and-switch' tactics used by predatory brokers. They will quote an unrealistically low price to secure a deposit, only to raise the price weeks later when a carrier refuses to move the vehicle for the low rate.",
    "Insurance coverage during transit is mandated by law. Every carrier must maintain valid liability and cargo insurance. It's perfectly acceptable to ask for a copy of the carrier's insurance certificate before they load your vehicle.",
    "Door-to-door service means the truck driver will get as close to your home as legally and safely possible. Due to the massive size of the 80-foot trailers, you may need to meet the driver in a nearby large parking lot.",
    "Communication with your driver is essential. Most professional drivers will call 12 to 24 hours before pickup and delivery to coordinate exact timing. Keep your phone handy on those days to avoid delays."
]

articles = []
generated_slugs = set()
base_date = datetime(2026, 8, 1)

# Generate exactly 1000 articles
while len(articles) < 1000:
    state = random.choice(states)
    topic_template = random.choice(topics)
    title = topic_template.format(state=state)
    slug = slugify(title)
    
    # Ensure unique slugs
    if slug in generated_slugs:
        # Add a random number to make it unique
        slug = f"{slug}-{random.randint(100, 999)}"
        if slug in generated_slugs:
            continue
    
    generated_slugs.add(slug)
    
    # Generate content
    num_paragraphs = random.randint(4, 7)
    content = ""
    selected_paragraphs = random.sample(content_paragraphs, num_paragraphs)
    for p in selected_paragraphs:
        content += f"<p>{p}</p>\n"
        
    author = random.choice(authors)
    bg_image = random.choice(background_images)
    
    # Randomize date slightly backwards from base_date
    days_back = random.randint(0, 365 * 2)
    pub_date = (base_date - timedelta(days=days_back)).isoformat() + "Z"
    
    article = {
        "id": slug,
        "title": title,
        "slug": slug,
        "authorId": author,
        "content": content,
        "excerpt": selected_paragraphs[0][:150] + "...",
        "publishedAt": pub_date,
        "backgroundImage": bg_image,
        "tags": ["Auto Transport", state, "Car Shipping Tips"]
    }
    
    articles.append(article)

# Sort articles by date descending
articles.sort(key=lambda x: x["publishedAt"], reverse=True)

# Save to JSON in the public/data directory for Next.js to consume
output_path = "/Users/silversurfer/Documents/Omniverse2/montway_clone/public/data/news_articles.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2)

print(f"Successfully generated {len(articles)} articles and saved to {output_path}")
