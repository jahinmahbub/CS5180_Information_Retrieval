from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


def extract_faculty_info(faculty_div):
    """Extract information from a faculty member's div"""
    info = {
        'name': '',
        'title': '',
        'office': '',
        'phone': '',
        'email': '',
        'website': ''
    }

    try:
        # Extract name (now checking multiple possible heading tags)
        name_tag = faculty_div.find(['h2', 'h3', 'h4', 'strong'])
        if name_tag:
            info['name'] = name_tag.text.strip()

        # Extract all paragraphs
        paragraphs = faculty_div.find_all('p')

        for p in paragraphs:
            text = p.text.strip()

            # Extract title
            if any(title_word in text.lower() for title_word in ['professor', 'chair', 'lecturer']):
                if not any(exclude_word in text.lower() for exclude_word in ['office:', 'phone:', 'email:']):
                    info['title'] = text.strip()
                    continue

            # Extract office
            office_match = re.search(r'Office:\s*(.*?)(?:\s*(?:Phone|Email|$))', text, re.I)
            if office_match:
                info['office'] = office_match.group(1).strip()

            # Extract phone
            phone_match = re.search(r'Phone:\s*(.*?)(?:\s*(?:Office|Email|$))', text, re.I)
            if phone_match:
                info['phone'] = phone_match.group(1).strip()

            # Extract email from mailto link
            email_link = p.find('a', href=re.compile(r'mailto:', re.I))
            if email_link:
                email = email_link['href'].replace('mailto:', '').strip()
                info['email'] = email

            # Extract website from regular link
            website_link = p.find('a', href=re.compile(r'http', re.I))
            if website_link and 'mailto:' not in website_link['href'].lower():
                info['website'] = website_link['href'].strip()

    except Exception as e:
        print(f"Error extracting faculty info: {e}")

    return info


def main():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['cs_faculty_db']

        # Find the target page in the database
        target_page = db.pages.find_one({'is_target': True})

        if not target_page:
            print("Target page not found in database")
            return

        print("Found target page, parsing faculty information...")

        # Parse the HTML
        soup = BeautifulSoup(target_page['html'], 'html.parser')

        # Try different possible container classes/IDs
        faculty_containers = [
            soup.find_all('div', class_='faculty-staff-bio'),
            soup.find_all('div', class_='faculty-bio'),
            soup.find_all('div', class_='bio'),
            soup.find_all('div', class_=re.compile(r'faculty|bio', re.I))
        ]

        # Use the first non-empty container list
        faculty_divs = next((containers for containers in faculty_containers if containers), [])

        if not faculty_divs:
            print("No faculty divs found. Trying alternative approach...")
            # Alternative approach: look for sections containing faculty information
            faculty_divs = []
            for tag in soup.find_all(['div', 'section']):
                if any(name in tag.text.lower() for name in ['professor', 'chair', 'faculty']):
                    faculty_divs.append(tag)

        print(f"Found {len(faculty_divs)} faculty divisions")

        # Clear existing professors collection
        db.professors.drop()

        # Process each faculty member
        for div in faculty_divs:
            faculty_info = extract_faculty_info(div)

            # Only store if we have at least a name
            if faculty_info['name']:
                db.professors.insert_one(faculty_info)
                print(f"Stored information for: {faculty_info['name']}")
            else:
                print("Found div without name:", div.text[:100])

        # Print summary
        professor_count = db.professors.count_documents({})
        print(f"\nTotal professors stored in database: {professor_count}")

        if professor_count == 0:
            print("\nDebug information:")
            print("HTML content sample:")
            print(target_page['html'][:500])

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()