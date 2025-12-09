import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file
import io


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
   if request.method == 'POST':
       # 1. Check if a file was uploaded
       if 'pdf_file' not in request.files:
           return "No file uploaded", 400
      
       file = request.files['pdf_file']
      
       if file.filename == '':
           return "No file selected", 400


       if file:
           try:
               # 2. Read the uploaded file into memory (stream)
               # We use .read() to get the bytes directly
               input_stream = file.read()
              
               # 3. Open PDF from memory using PyMuPDF
               # "pdf" tells fitz that this stream is a PDF
               doc = fitz.open(stream=input_stream, filetype="pdf")
              
               # 4. Create a memory buffer to hold the compressed file
               output_buffer = io.BytesIO()
              
               # 5. Compress and write to the memory buffer
               # garbage=4: Remove unused objects
               # deflate=True: Compress streams
               doc.save(output_buffer, garbage=4, deflate=True, clean=True)
               doc.close()
              
               # 6. Reset buffer position to the beginning so it can be read
               output_buffer.seek(0)
              
               # 7. Generate a new filename
               original_name = file.filename
               new_name = f"compressed_{original_name}"
              
               # 8. Send the file back to the user as a download
               return send_file(
                   output_buffer,
                   as_attachment=True,
                   download_name=new_name,
                   mimetype='application/pdf'
               )


           except Exception as e:
               return f"An error occurred: {str(e)}", 500


   # If it's a GET request, just show the HTML form
   return render_template('index.html')


if __name__ == '__main__':
   app.run(debug=True, port=5001)

