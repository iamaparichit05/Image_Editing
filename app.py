from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
import cv2
import os
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key='super secret key'
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            img_Processed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,img_Processed)
            return newfilename
        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpg":
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cbinary":
            _, img_Processed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            newfilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img_Processed)
            return newfilename
        case "cnorm":
            img_Processed = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            newfilename = f"static/{filename.split('.')[0]}_norm.png"
            cv2.imwrite(newfilename, img_Processed)
            return newfilename
    pass

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/edit",methods=["GET","POST"])
def edit():
   if request.method == "POST":
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"Your image has been processed and is available at <a href='/{new}' target='_blank'>here</a>")

            return render_template("index.html")
        
  

if __name__=="__main__":
    app.run(debug=True,port=5000)