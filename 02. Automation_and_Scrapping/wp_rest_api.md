## 01. Simple Posting
```py
import requests
from requests.auth import HTTPBasicAuth

url = "https://your-wordpress-site.com/wp-json/wp/v2/posts"

username = "your-username"
password = "your-application-password"

post_data = {
    "title": "Text Post",
    "content": "Test Content From App",
    "status": "draft"  # 'publish' / 'schedule'
}

response = requests.post(url, auth=HTTPBasicAuth(username, password), json=post_data)

if response.status_code == 201:
    print("Post created successfully!")
    print("Response:", response.json())  # The created post data
else:
    print(f"Failed to create post. Status code: {response.status_code}")
    print("Response:", response.json())  # Error details
```
