import os
import tempfile
import azure.functions as func
import subprocess
import logging

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("🔧 Function triggered.")

    try:
        uploaded_file = req.files.get('file')
        if not uploaded_file:
            logging.warning("⚠️ No file uploaded in the request.")
            return func.HttpResponse("No file uploaded", status_code=400)

        logging.info(f"📦 Received file: {uploaded_file.filename}")

        # Geçici dosya yolları
        input_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
        output_path = os.path.join(tempfile.gettempdir(), 'output.mp3')

        uploaded_file.save(input_path)
        logging.info(f"💾 Saved input file to: {input_path}")

        # FFmpeg komutu
        command = ['ffmpeg', '-y', '-i', input_path, output_path]
        logging.info(f"▶️ Running FFmpeg command: {' '.join(command)}")

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            logging.error(f"❌ FFmpeg error: {result.stderr.decode('utf-8')}")
            return func.HttpResponse("Error processing file with FFmpeg", status_code=500)

        logging.info(f"✅ FFmpeg successfully converted file to: {output_path}")

        with open(output_path, 'rb') as f:
            mp3_bytes = f.read()

        logging.info("📤 Returning MP3 file to client.")
        return func.HttpResponse(mp3_bytes, mimetype="audio/mpeg")

    except Exception as e:
        logging.exception("🚨 Unexpected error occurred:")
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
