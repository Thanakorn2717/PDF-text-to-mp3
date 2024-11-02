import os
import boto3
import fitz  # PyMuPDF

pdf_path = "./pdf"
mp3_path = "./mp3"
pdf_files = [file for file in os.listdir(pdf_path) if file.lower().endswith('.pdf')]

access_key = os.environ.get("access_key")
secret_key = os.environ.get("secret_key")

# Initialize the Polly client
polly_client = boto3.client('polly',
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            region_name='ap-southeast-1')  # Choose the appropriate region

for item in pdf_files:

    # Open the PDF file
    with fitz.open(f"./pdf/{item}") as pdf:
        text = ""

        # Loop through each page and extract text
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text = page.get_text() + "\n"

            # Convert text to speech
            response = polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',  # Choose the format you prefer (e.g., mp3, ogg_vorbis, pcm)
                VoiceId='Joanna'  # Choose a voice (e.g., Joanna, Matthew)
            )
            print(response)

            # Save the audio stream to a file
            if 'AudioStream' in response:
                with open(f"{mp3_path}/{item[:-4]+'('+str(page_num+1)+')'}.mp3", "wb") as file:
                    file.write(response['AudioStream'].read())
                print(f"Audio file saved as '{item[:-4]+'('+str(page_num+1)+')'}'.mp3'")
            else:
                print("Could not generate audio")
