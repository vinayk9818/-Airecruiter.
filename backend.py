from flask import Flask,render_template,request
from dotenv import load_dotenv
import os,requests
import PyPDF2
import os


app=Flask(__name__)
load_dotenv() 
UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route("/",methods=['POST','GET'])
def main():
    story=""
    if request.method=='POST':
        os.makedirs("uploads",exist_ok=True)
        file=request.files.get('file')
        if file and file.filename.endswith('pdf'):
            filename=file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            x=f"this my resume file;{filename}"
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # with open("filename",'rb'):
            #     pages=pages.readerline
            # def extract_text_from_pdf(file_path):
            text = ""
            with open(  file_path, 'rb') as file:
              
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
                # return text
            headers={
            "Authorization":os.getenv("secret_key"),
            "Content-type":os.getenv("mode")
        }
        
        data={
            "model":"llama3-70b-8192",
            "messages":[
                {"role": "system", "content": "You are an expert HR and career coach. Your job is to carefully review resumes, identify missing or weak sections, and suggest specific improvements. Be honest and helpful. Suggest what important sections, skills, achievements, or formatting are missing."},

                {"role":"user","content":text}
            ]
        }

        response=requests.post("https://api.groq.com/openai/v1/chat/completions",headers=headers,json=data)
        story=response.json()['choices'][0]['message']['content']
    return render_template('page.html',story=story)
if __name__=="__main__":
    app.run(debug=True)

