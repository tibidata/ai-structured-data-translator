import logging
import json
from io import BytesIO

from flask import Flask, request, jsonify, send_file

from tools import TranslatorClient, extract_lua, generate_lua

# Initialize Flask app
app = Flask(__name__)

# Initialize TranslatorClient
client = TranslatorClient()

# Configure logging to store logs in a file
logging.basicConfig(
    filename="app/logs/app.log",  # Log file location
    level=logging.DEBUG,  # Set logging level to debug for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)


@app.route("/")
def healthcheck():
    """
    Health check endpoint to verify that the API is running.

    Returns:
        Response: A JSON response indicating the API's operational status.
    """
    return jsonify({"success": True})


@app.route("/translate", methods=["POST"])
def translate():
    """
    Endpoint for handling translation requests.

    Processes an uploaded file (JSON or Lua), translates its contents,
    and returns the translated file as an attachment.

    Returns:
        Response: The translated file as an attachment.
        HTTP Status Code: 200 on success, 500 on error.
    """
    try:
        # Retrieve uploaded file from request
        file = request.files["file"]
        file_type = file.filename.split(".")[-1]  # Extract file extension
        file_utf = file.read().decode("utf-8")  # Read file content as UTF-8

        # Validate file type
        if file_type not in ["json", "lua"]:
            return jsonify({"error": "Invalid file type."}), 500

        # Process JSON file
        if file_type == "json":
            json_input = json.loads(file_utf)  # Parse JSON content
            response = json.dumps(client(json_input, "json"), ensure_ascii=False)

        # Process Lua file
        if file_type == "lua":
            # Extract key-value pairs from Lua script
            kv_dict = extract_lua(
                lua_code=file_utf, var_name=request.form.get("var_name")
            )

            # Translate values and generate translated Lua script
            response = generate_lua(
                var_name=request.form.get("var_name"),
                kv_dict={k: client(v, "json") for k, v in kv_dict.items()},
            )

        # Return translated file as downloadable attachment
        return send_file(
            BytesIO(response.encode("utf-8")),
            as_attachment=True,
            download_name=f"{file.filename.split('.')[0]}_ai_trs.{file_type}",
            mimetype="text/plain",
        )

    except Exception as e:
        # Log any errors that occur during processing
        logging.exception("Error processing translation request")

        # Return a generic error response with a 500 status code
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


if __name__ == "__main__":
    # Start the Flask app, making it accessible on all network interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
