import asyncio
import random
import re

first_names = ['Apex', 'Elite', 'Summit', 'Global', 'Golden', 'Nomad', 'Compass', 'Horizon', 'Vanguard', 'Blue Sky', 'Voyage', 'Pioneer', 'Echo', 'Infinite']
second_names = ['Travels', 'Adventures', 'Agencies', 'Expeditions', 'Getaways', 'Holidays', 'Tours', 'Journeys', 'Escapes', 'Destinations', 'Leisure', 'Pathfinders']
generic_second_names = ['Solutions', 'Group', 'Partners', 'Services', 'Associates', 'Co', 'Hub', 'Network', 'International', 'Enterprises']
domains = ['.com', '.org', '.net', '.in', '.co.uk', '.travel']

def generate_business_name(category: str, area: str) -> str:
    is_travel = any(word in category.lower() for word in ['travel', 'tour', 'agent'])
    word1 = random.choice(first_names)
    
    if is_travel:
        word2 = random.choice(second_names)
    else:
        cat_words = category.strip().split()
        base_cat = cat_words[-1] if cat_words else "Service"
        capitalized_base = base_cat.capitalize()
        word2 = capitalized_base if random.random() > 0.4 else f"{capitalized_base} {random.choice(generic_second_names)}"
        
    if random.random() < 0.15:
        clean_area = area.split(',')[0].strip().capitalize()
        return f"{clean_area} {word1} {word2}" if random.random() > 0.5 else f"{word1} {word2} of {clean_area}"
        
    return f"{word1} {word2}"

async def scrape_simulated(category: str, area: str, limit: int = 10, on_progress=None):
    if on_progress:
        await on_progress(5, "[INFO] Initializing Python Simulated Browser environment...")
        await asyncio.sleep(0.4)
        await on_progress(10, "[INFO] Adjusting user-agent credentials and proxy mappings...")
        await asyncio.sleep(0.3)
        await on_progress(15, "[INFO] Connecting to https://www.google.com/maps")
        await asyncio.sleep(0.5)
        await on_progress(20, f"[INFO] Searching for '{category} in {area}'...")
        await asyncio.sleep(0.6)
        await on_progress(25, "[SUCCESS] Google Maps sidebar loaded successfully. Found list viewport.")
        await asyncio.sleep(0.3)

    items = []
    base_lat = 23.0225 + (random.random() - 0.5) * 0.1
    base_lng = 72.5714 + (random.random() - 0.5) * 0.1

    for i in range(limit):
        progress = min(25 + int((i / limit) * 70), 95)
        name = generate_business_name(category, area)
        
        if on_progress:
            await on_progress(progress, f"[SCRAPING] [{i+1}/{limit}] Scrolling & extracting details for: '{name}'...")
            await asyncio.sleep(0.2 + random.random() * 0.3)
            
        rating = round(3.8 + (random.random() * 1.2), 1)
        reviews = random.randint(5, 450)
        
        clean_name = re.sub(r'[^a-z0-9]', '', name.lower())
        domain = random.choice(domains)
        website = f"https://www.{clean_name}{domain}"
        email = f"contact@{clean_name}{domain}"
        
        address_no = random.randint(1, 200)
        block = random.choice(['A', 'B', 'C', 'D', 'G', 'H', 'Saffron', 'Titanium', 'Shivalik'])
        street = random.choice(['Main Rd', 'Satellite Rd', 'Ring Road', 'High Street', 'Commercial Lane'])
        address = f"{address_no}, {block} Block, Near Circle, {street}, {area}, India"
        phone = f"+91 {random.randint(90000, 99999)} {random.randint(10000, 99999)}"
        
        facebook = f"https://facebook.com/{clean_name}" if random.random() > 0.4 else ""
        instagram = f"https://instagram.com/{clean_name}" if random.random() > 0.5 else ""
        
        items.append({
            "id": i + 1,
            "name": name,
            "rating": rating,
            "reviewsCount": reviews,
            "category": category.capitalize(),
            "address": address,
            "phone": phone,
            "website": website,
            "email": email,
            "socials": {
                "facebook": facebook,
                "instagram": instagram
            },
            "latitude": round(base_lat + (random.random() - 0.5) * 0.02, 6),
            "longitude": round(base_lng + (random.random() - 0.5) * 0.02, 6)
        })

    if on_progress:
        await on_progress(98, f"[INFO] Lead extraction complete. Compiled {limit} records.")
        await asyncio.sleep(0.4)
        await on_progress(100, "[SUCCESS] Scraping completed successfully! Report compiled and ready.")
        
    return items
