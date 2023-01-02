import requests
import config

# Replace YOUR_TELEGRAM_BOT_TOKEN with your actual Telegram bot token
TOKEN = config.api_token

# Replace CHANNEL_NAME with the name of your channel (without the '@' symbol)
CHANNEL_NAME = config.channel_id


def get_quote_and_image():
    # Make a request to the quote API
    response = requests.get('http://quotes.rest/qod.json')

    print("----------", response)

    # Get the quote and image URL from the response
    quote = response.json()['contents']['quotes'][0]['quote']
    image_url = response.json()['contents']['quotes'][0]['background']

    # Return the quote and image URL
    return quote, image_url


def send_quote_with_image(quote, image_url):
    # Set the base URL for the Telegram API
    base_url = f'https://api.telegram.org/bot{TOKEN}'

    # Download the image
    image_response = requests.get(image_url)
    image = image_response.content

    # Set the URL for sending a message with an image to the channel
    send_message_url = f'{base_url}/sendPhoto'

    # Set the payload for the request
    payload = {
        'chat_id': CHANNEL_NAME,
        'caption': quote
    }

    # Set the headers for the request
    headers = {
        'Content-Type': 'application/octet-stream'
    }

    # Send the message with the image
    response = requests.post(send_message_url, data=image,
                             headers=headers, params=payload)

    # Check the response status code
    if response.status_code != 200:
        # Print the error message
        print(response.json()['description'])
    else:
        # Print a success message
        print('Message sent successfully!')


def main():
    # Get a quote and image URL
    quote, image_url = get_quote_and_image()

    # Send the quote and image to the Telegram channel
    send_quote_with_image(quote, image_url)


# Run the main function
if __name__ == '__main__':
    main()
