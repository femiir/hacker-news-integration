# Hacker News Integration

This project integrates with the Hacker News API to fetch and manage Hacker News items and comments. It provides functionality for listing items, adding new items, updating existing items, deleting items, retrieving item details, and fetching item comments. The integration is done asynchronously using asyncio and aiohttp for efficient handling of HTTP requests.

## Installation

To run this project, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/your_username/hacker-news-integration.git
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the Django project:

   ```
   cd hacker-news-integration
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Start the Django-Q cluster for background task execution:

   ```
   python manage.py qcluster
   ```

5. Run the Hacker News fetching process:

   ```
   python manage.py hackernews
   ```

6. Start the development server:

   ```
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000`.

## Usage

The project provides the following API endpoints:

- `/items`: 
  - GET: Retrieve a list of Hacker News items. Optional query parameter `limit` specifies the maximum number of items to retrieve.
  - POST: Add a new Hacker News item. Requires a JSON payload containing `by`, `title`, and `url` fields.

- `/items/{item_id}`:
  - GET: Retrieve a specific Hacker News item.
  - PUT: Update an existing Hacker News item. Requires a JSON payload containing the updated fields.
  - DELETE: Delete an existing Hacker News item.

- `/items/{item_id}/comments`:
  - GET: Retrieve the comments for a specific Hacker News item.

Refer to the API documentation for detailed information on request and response formats.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project was an test from a company i applied for

## Credits

This project was developed by [femiir](https://github.com/femiir).

