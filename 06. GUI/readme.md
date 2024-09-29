# Content
```
Databse Handle with SQLAlchemy ORM (sync) - CRUD
Databse Handle with Tortoise ORM (async) - CRUD with Example
Databe handle without any ORM - CRUD
```

### Databse Handle with SQLAlchemy ORM
```bash
pip install sqlalchemy
```
#### 01. Define the Database Models (Create)
```py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Set up SQLite database and base
Base = declarative_base()

# Website Model
class Website(Base):
    __tablename__ = 'websites'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Relationship to connect website with its pages
    pages = relationship('Page', back_populates='website', cascade='all, delete-orphan')

# Page Model
class Page(Base):
    __tablename__ = 'pages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    content = Column(String, nullable=False)
    
    # Foreign key linking to Website
    website_id = Column(Integer, ForeignKey('websites.id'))
    
    # Relationship to access website from page
    website = relationship('Website', back_populates='pages')

# Create SQLite engine and session
engine = create_engine('sqlite:///websites.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)
```
#### 02. Insering Data (Write)
```py
# Add a website and its pages
new_website = Website(name="Example", url="https://example.com")
new_website.pages = [
    Page(url="https://example.com/page1", content="Content of Page 1"),
    Page(url="https://example.com/page2", content="Content of Page 2")
]

session.add(new_website)
session.commit()

# Add another website and its pages
another_website = Website(name="Another Website", url="https://anotherwebsite.com")
another_website.pages = [
    Page(url="https://anotherwebsite.com/page1", content="Content of Another Website Page 1"),
    Page(url="https://anotherwebsite.com/page2", content="Content of Another Website Page 2")
]

session.add(another_website)
session.commit()
```
#### 03. Querying & Filter Data (Read)
```py
# Fetch all pages of a specific website
website = session.query(Website).filter_by(name="Example").first()

# Access all pages related to this website
for page in website.pages:
    print(f"Page URL: {page.url}, Content: {page.content}")
```
```py
website_id = website.id
pages = session.query(Page).filter_by(website_id=website_id).all()

for page in pages:
    print(f"Page URL: {page.url}, Content: {page.content}")
```
#### 04. Update data (Update)
```py
# Update example function
def update_website(website_id, new_name=None, new_url=None):
    # Fetch the website record by id
    website = session.query(Website).filter(Website.id == website_id).first()
    
    if website:
        if new_name:
            website.name = new_name
        if new_url:
            website.url = new_url
        
        session.commit()  # Save changes to the database
        print(f"Updated website: {website.name}, {website.url}")
    else:
        print("Website not found.")

# Example usage
update_website(1, new_name="Updated Example", new_url="https://updatedexample.com")
```
### Databse Handle with Tortoise ORM
```bash
pip install tortoise-orm aiosqlite
```
#### 01. Define Models in Tortoise ORM (create)
config.json
```json
{
    "connections": {
        "default": "sqlite://websites.db"
    },
    "apps": {
        "models": {
            "models": ["__main__"],
            "default_connection": "default"
        }
    }
}

```
```py
from tortoise import Tortoise, fields
from tortoise.models import Model


# Define Website model
class Website(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)

    # Reverse relation to the Page model
    pages: fields.ReverseRelation['Page']


# Define Page model
class Page(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    content = fields.TextField()

    # ForeignKeyField to link Page to Website
    website = fields.ForeignKeyField('models.Website', related_name='pages')


# Initialize the Tortoise ORM
async def init():
    await Tortoise.init(
        db_url='sqlite://websites.db',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

# Call the init function to initialize the database schema
import asyncio
asyncio.run(init())
```
#### 02. Insert Data into the Database (Write)
```py
async def add_website_with_pages():
    # Create a new website
    website = await Website.create(name="Example", url="https://example.com")

    # Add multiple pages for the website
    await Page.create(url="https://example.com/page1", content="Page 1 content", website=website)
    await Page.create(url="https://example.com/page2", content="Page 2 content", website=website)

    # Add another website with pages
    another_website = await Website.create(name="Another Website", url="https://anotherwebsite.com")
    await Page.create(url="https://anotherwebsite.com/page1", content="Another Website Page 1 content", website=another_website)

# Run the async function to add data
asyncio.run(add_website_with_pages())
```
#### 03. Querying & Filtering Data (Read)
```py
async def filter_pages_by_website():
    # Fetch all pages for the website with id=1
    pages = await Page.filter(website_id=1)

    for page in pages:
        print(f"Page URL: {page.url}, Content: {page.content}")

# Run the filter function
asyncio.run(filter_pages_by_website())
```
#### 04. Data Update (Update)
```py
async def update_website(website_id, new_name=None, new_url=None):
    # Fetch the website record by id
    website = await Website.get(id=website_id)
    
    if website:
        if new_name:
            website.name = new_name
        if new_url:
            website.url = new_url
        
        await website.save()  # Save changes to the database
        print(f"Updated website: {website.name}, {website.url}")
    else:
        print("Website not found.")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await update_website(1, new_name="Updated Example", new_url="https://updatedexample.com")

run_async(main())
```

#### 05. Example Add Web Crawling
```py
import aiohttp
import asyncio
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

# Define your models
class Website(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)
    pages: fields.ReverseRelation['Page']

class Page(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    content = fields.TextField()
    website = fields.ForeignKeyField('models.Website', related_name='pages')

# Tortoise ORM initialization
async def init():
    await Tortoise.init(config="config.json")
    await Tortoise.generate_schemas()

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def crawl_websites(websites):
    async with aiohttp.ClientSession() as session:
        for website in websites:
            main_page_content = await fetch_page(session, website['url'])
            website['pages'] = [{'url': website['url'], 'content': main_page_content}]

async def save_crawled_data(crawled_data):
    for site in crawled_data:
        website, _ = await Website.get_or_create(name=site['name'], url=site['url'])
        for page_data in site['pages']:
            await Page.create(url=page_data['url'], content=page_data['content'], website=website)

async def main():
    await init()  # Initialize Tortoise ORM
    crawled_data = [
        {"name": "Example", "url": "https://example.com"},
        {"name": "Another Website", "url": "https://anotherwebsite.com"},
    ]
    await crawl_websites(crawled_data)  # Step 1: Crawl the websites
    await save_crawled_data(crawled_data)  # Step 3: Save crawled data to DB

run_async(main())
```

