import logging
import azure.functions as func
import subprocess
import tempfile
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file_data = req.get_body()
        if not file_data:
            return func.HttpResponse("No file provided", status_code=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
            tmp_input.write(file_data)
            tmp_input.flush()
            input_path = tmp_input.name

        output_path = input_path.replace(".mp4", ".mp3")

        subprocess.run([
            "ffmpeg", "-i", input_path, "-vn", "-acodec", "libmp3lame", output_path
        ], check=True)

        with open(output_path, "rb") as f:
            mp3_data = f.read()

        os.remove(input_path)
        os.remove(output_path)

        return func.HttpResponse(
            mp3_data,
            mimetype="audio/mpeg",
            status_code=200,
            headers={"Content-Disposition": "attachment; filename=output.mp3"}
        )

    except subprocess.CalledProcessError as e:
        logging.error("FFmpeg failed: %s", e)
        return func.HttpResponse(f"FFmpeg error: {e}", status_code=500)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return func.HttpResponse(f"Unexpected error: {e}", status_code=500)
