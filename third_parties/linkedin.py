import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def clean_response_data(response):
    data = response.json()

    data = {
        k: v for k, v in data.items()
        if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from LinkedIn profiles."""
    api_key = os.environ["LINKEDIN_API_KEY"]
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        #'twitter_profile_url': 'https://x.com/johnrmarty/',
        #'facebook_profile_url': 'https://facebook.com/johnrmarty/',
        'linkedin_profile_url': linkedin_profile_url
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)
    if response.status_code != 200:
        mocked_endpoint = 'https://gist.githubusercontent.com/srdjanbocanji/865ba02f454f3a19a8f6e778e30e9974/raw/a183c53c09eb7d168f808acc121629e74288e69c/mock_linkedin_data.json'
        response = requests.get(mocked_endpoint, timeout=10)

    data = clean_response_data(response)
    return data

if __name__ == '__main__':
    print(scrape_linkedin_profile('https://www.linkedin.com/in/johnrmarty/'))
