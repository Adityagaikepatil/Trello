import requests  # Import the requests library to make HTTP requests
import argparse  # Import argparse to handle command-line arguments

def create_trello_card(api_key, token, board_id, list_id, card_name, card_desc, labels, comment):
    base_url = "https://api.trello.com/1"  # Base URL for Trello API
    
    # Create card
    card_url = f"{base_url}/cards"  # Endpoint to create a Trello card
    card_data = {
        "name": card_name,   # Name of the card
        "desc": card_desc,   # Description of the card
        "idList": list_id,   # The list where the card should be added
        "key": api_key,      # API key for authentication
        "token": token       # API token for authentication
    }
    
    # Send POST request to create the Trello card
    response = requests.post(card_url, data=card_data)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print("Failed to create card:", response.text)  # Print error message if creation fails
        return  # Exit function
    
    # Parse response JSON to get card details
    card = response.json()
    card_id = card["id"]  # Extract the created card's ID
    print(f"Card created: {card['shortUrl']}")  # Print the card's Trello URL

    # Add labels to the created card
    if labels:
        for label in labels.split(","):  # Split the label string by commas if multiple labels are provided
            label_url = f"{base_url}/cards/{card_id}/idLabels"  # Endpoint to add labels to a card
            label_data = {"value": label.strip(), "key": api_key, "token": token}  # Label data
            requests.post(label_url, data=label_data)  # Send request to add label
        print("Labels added.")  # Print success message

    # Add comment to the card
    if comment:
        comment_url = f"{base_url}/cards/{card_id}/actions/comments"  # Endpoint to add a comment to a card
        comment_data = {"text": comment, "key": api_key, "token": token}  # Comment data
        requests.post(comment_url, data=comment_data)  # Send request to add comment
        print("Comment added.")  # Print success message

# Main execution block
if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Add a card to a Trello board.")
    
    # Define required and optional arguments
    parser.add_argument("--api_key", required=True, help="Your Trello API Key")  # Trello API key
    parser.add_argument("--token", required=True, help="Your Trello API Token")  # Trello API token
    parser.add_argument("--board_id", required=True, help="Trello Board ID")  # Trello board ID
    parser.add_argument("--list_id", required=True, help="Trello List ID")  # Trello list ID where card will be added
    parser.add_argument("--card_name", required=True, help="Card title")  # Title of the Trello card
    parser.add_argument("--card_desc", required=False, help="Card description", default="")  # Optional card description
    parser.add_argument("--labels", required=False, help="Comma-separated list of label IDs")  # Optional labels
    parser.add_argument("--comment", required=False, help="Comment to add to the card")  # Optional comment

    # Parse command-line arguments
    args = parser.parse_args()

    # Call function to create Trello card with parsed arguments
    create_trello_card(args.api_key, args.token, args.board_id, args.list_id, args.card_name, args.card_desc, args.labels, args.comment)
