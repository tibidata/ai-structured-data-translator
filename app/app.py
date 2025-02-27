import logging
from flask import Flask, request, jsonify
from tools import TranslatorClient

# Initialize Flask app
app = Flask(__name__)

# Initialize TranslatorClient
client = TranslatorClient()

# Configure logging to store logs in a file
logging.basicConfig(
    filename="logs/app.log",  # Log file location
    level=logging.DEBUG,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)


@app.route("/")
def healthcheck():
    """
    Health check endpoint to verify that the API is running.

    Returns:
        dict: A JSON response indicating the API's operational status.
    """
    return jsonify({"success": True})


@app.route("/translate", methods=["POST"])
def translate():
    """
    Endpoint for handling translation requests.

    This function processes incoming POST requests for translation,
    logs the interaction, and returns the translated text.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
               The JSON response includes either the translated message or an error message.
    """
    try:
        # Parse incoming JSON request
        data = request.json

        # Process the translation request using the TranslatorClient
        response = client(data)

        # Log the incoming data for monitoring and debugging purposes
        logging.info(f"Translation request received: {data}")

        # Return the translated text as a JSON response
        return (
            jsonify(
                {
                    "success": True,
                    "translation": response,
                }
            ),
            200,
        )

    except Exception as e:
        # Log any errors that occur during processing
        logging.exception("Error processing translation request")

        # Return an error response with a 500 status code
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


if __name__ == "__main__":
    # Run Flask app on all available network interfaces
    app.run(host="0.0.0.0", port=5000)
