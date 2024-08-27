import boto3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Specify your region here
AWS_REGION = 'ap-south-1'  # Change to your region

s3 = boto3.client('s3', region_name=AWS_REGION)
sqs = boto3.client('sqs', region_name=AWS_REGION)

ORIGINAL_BUCKET = 'source-bucket-conversion'  # Replace with Actual Source Bucket
CONVERTED_BUCKET = 'destination-bucket-conversion'  # Replace with Actual Destination Bucket
SQS_QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/891377318947/file-conversion-queue'  # Replace with your Actual URL

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <style>
            .container {
                max-width: 500px;
                margin: 0 auto;
                text-align: center;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                margin-top: 50px;
            }
            h1 {
                font-family: Arial, sans-serif;
                color: #333;
            }
            input[type="file"] {
                margin: 10px 0;
            }
            button {
                padding: 10px 15px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }
            /* Modal styles */
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0, 0, 0, 0.5);
                padding-top: 60px;
            }
            .modal-content {
                background-color: white;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
                max-width: 300px;
                text-align: center;
            }
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }
            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Upload Files to S3</h1>
            <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required />
                <button type="submit" value="Upload">Upload</button>
            </form>
        </div>

        <!-- The Modal -->
        <div id="uploadModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <p id="modalMessage">File uploaded and conversion started!</p>
            </div>
        </div>

        <script>
            document.getElementById('uploadForm').onsubmit = function(event) {
                event.preventDefault();
                const formData = new FormData(this);

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                }).then(response => response.json())
                .then(data => {
                    document.getElementById('modalMessage').textContent = data.message || 'File upload failed';
                    document.getElementById('uploadModal').style.display = 'block';
                });

                return false;
            };

            // Get the modal
            var modal = document.getElementById("uploadModal");

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName("close")[0];

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        </script>

    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'})
    if file:
        try:
            s3.upload_fileobj(file, ORIGINAL_BUCKET, file.filename)
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,  # Replace the Queue URL with your Actual URL
                MessageBody=file.filename
            )
            return jsonify({'message': 'File uploaded and conversion started'})
        except Exception as e:
            return jsonify({'message': f'File upload failed: {str(e)}'})
    return jsonify({'message': 'File upload failed'})

@app.route('/converted/<filename>', methods=['GET'])
def get_converted_file(filename):
    try:
        s3.download_file(CONVERTED_BUCKET, filename, '/tmp/' + filename)
        return send_from_directory('/tmp', filename)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
