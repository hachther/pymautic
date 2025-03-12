# Mautic Python Client

A Python client for interacting with the Mautic API. This library provides a simple and intuitive way to manage your Mautic instance programmatically, allowing you to automate tasks, manage contacts, campaigns, assets, and more.

## Features

- **Contact Management**: Create, update, and delete contacts.
- **Segment Management**: Manage contact segments.
- **Campaign Management**: Create and manage campaigns (coming soon).
- **Asset Management**: Upload and manage assets (coming soon).
- **Form Management**: Manage forms and form submissions (coming soon).
- **Email Management**: Manage email templates and send emails.
- **API Rate Limiting Handling**: Built-in handling for Mautic's API rate limits. (coming soon).

## Installation

You can install the Mautic Python Client using pip:

```bash
pip install pymautic
```

## Usage

### Initialization

First, you need to initialize the client with your Mautic instance URL and API credentials.

```python
from pymautic import MauticClient

# Initialize the client
client = MauticClient('username', 'password', 'https://your-mautic-instance.com')
```

### Managing Contacts

#### Create a Contact

```python
contact_data = {
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john.doe@example.com',
    'ipAddress': '192.168.1.1',
}

response = client.contacts.create(contact_data)
print(response)
```

#### Get a Contact by ID

```python
contact_id = 1
response = client.contacts.get(contact_id)
print(response)
```

#### Update a Contact

```python
contact_id = 1
update_data = {
    'firstname': 'Jane',
    'lastname': 'Doe'
}

response = client.contacts.update(contact_id, update_data)
print(response)
```

#### Delete a Contact

```python
contact_id = 1
response = client.contacts.delete(contact_id)
print(response)
```

### Managing Segments

#### Create a Segment

```python
segment_data = {
    'name': 'New Segment',
    'alias': 'new-segment',
    'description': 'A new segment created via API'
}

response = client.segments.create(segment_data)
print(response)
```

#### Add a Contact to a Segment

```python
segment_id = 1
contact_id = 1
response = client.segments.add_contact(segment_id, contact_id)
print(response)
```

### Managing Campaigns

#### Create a Campaign

```python
campaign_data = {
    'name': 'New Campaign',
    'description': 'A new campaign created via API',
    'isPublished': True
}

response = client.campaigns.create(campaign_data)
print(response)
```

#### Add a Contact to a Campaign

```python
campaign_id = 1
contact_id = 1
response = client.campaigns.add_contact(campaign_id, contact_id)
print(response)
```

### Managing Assets

#### Upload an Asset

```python
file_path = '/path/to/your/file.pdf'
response = client.assets.upload(file_path)
print(response)
```

### Managing Forms

#### Get Form Submissions

```python
form_id = 1
response = client.forms.get_submissions(form_id)
print(response)
```

### Managing Emails

#### Send an Email

```python
email_id = 1
contact_id = 1
response = client.emails.send(email_id, contact_id)
print(response)
```

## Rate Limiting

The Mautic API has rate limits in place to prevent abuse. This client automatically handles rate limiting by waiting the appropriate amount of time before retrying the request.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mautic API Documentation
- Python Requests Library

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/your-repo/mautic-python-client).

---

Happy coding! 🚀
