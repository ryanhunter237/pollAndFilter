from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
db = SQLAlchemy(app)


# Define the 'files' table
class File(db.Model):
    __tablename__ = "files"
    file_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    md5 = db.Column(db.Text, nullable=False)
    __table_args__ = (db.UniqueConstraint("group_id", "filename"),)


# Define the 'tags' table
class Tag(db.Model):
    __tablename__ = "tags"
    md5 = db.Column(db.Text, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.Text, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint("md5", "sequence"),)


@app.route("/")
def index():
    return render_template("index.html")


# API route to add a new file
@app.route("/api/files", methods=["PUT"])
def add_file():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    group_id = data.get("group_id")
    filename = data.get("filename")
    md5 = data.get("md5")
    if not all([group_id, filename, md5]):
        return jsonify({"error": "Missing required parameters"}), 400
    # Check for uniqueness of (group_id, filename)
    existing_file = File.query.filter_by(group_id=group_id, filename=filename).first()
    if existing_file:
        return (
            jsonify({"error": "File with this group_id and filename already exists"}),
            400,
        )
    new_file = File(group_id=group_id, filename=filename, md5=md5)
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File added successfully"}), 200


# API route to add a new tag
@app.route("/api/tags", methods=["PUT"])
def add_tag():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    md5 = data.get("md5")
    sequence = data.get("sequence")
    tag = data.get("tag")
    if not all([md5, sequence, tag]):
        return jsonify({"error": "Missing required parameters"}), 400
    # Check for uniqueness of (md5, sequence)
    existing_tag = Tag.query.filter_by(md5=md5, sequence=sequence).first()
    if existing_tag:
        return jsonify({"error": "Tag with this md5 and sequence already exists"}), 400
    new_tag = Tag(md5=md5, sequence=sequence, tag=tag)
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"message": "Tag added successfully"}), 200


# API route to fetch all files and associated tags
@app.route("/api/files_and_tags", methods=["GET"])
def get_files_and_tags():
    files = File.query.order_by(File.group_id, File.file_id).all()
    result = {}
    for file in files:
        tags = Tag.query.filter_by(md5=file.md5).order_by(Tag.sequence).all()
        tag_list = [tag.tag for tag in tags]
        file_data = {
            "file_id": file.file_id,
            "filename": file.filename,
            "tags": tag_list,
        }
        result.setdefault(file.group_id, []).append(file_data)
    return jsonify(result)


if __name__ == "__main__":
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
