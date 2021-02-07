from flask import Flask
from flask_restful import Api, Resource, reqparse,abort, fields,marshal_with
from flask_sqlalchemy import SQLAlchemy


#create app within flask
app = Flask(__name__)
api = Api(app) #wrapping our app in an api

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)




class WordModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(3), nullable=False)
    vowel=db.Column(db.String(1), nullable=False)
    views=db.Column(db.Integer, nullable=False)

    #just to make sure we get something that is valid, this will always print the value of whataver the keys represent
    #ideally when you only want to have a look at the representation internally
    def __repr__(self):
        return f"Word(name = {name}, vowel = {vowel}, views = {views})"

#this creates a db for us that has all this model inside of it 
db.create_all()        

word_put_args = reqparse.RequestParser()
word_put_args.add_argument("name", type=str, help="Naming of word is required")
word_put_args.add_argument("vowel", type=str, help="Vowel is required")
word_put_args.add_argument("views", type=int, help="Views of word")

#use resource fields- this defines how the object should be serialized, basically defines this dictionary based on the fields of the video model
resource_fields = {
    'id': fields.Integer,
    'name' : fields.String,
    'vowel' : fields.String,
    'views' :fields.Integer

}
#words = {}


#to avoid crashing the prog,do
#def abort_if_word_id_not_there(word_id):
 #   if word_id not in words:
 #       abort(404, message = "Could not find word...")

#def abort_if_word_exists(word_id):
 #   if word_id in words:
  #      abort(409, message ="Word already exists...")        


#create resource within the api, inherits from Resource
class Word(Resource):
    @marshal_with(resource_fields)
    def get(self, word_id):
        #abort_if_word_id_not_there(word_id)
        result = WordModel.query.filter_by(id=word_id).first #gives results of an instance word model
        if not result:
            abort(404, message="Could not find word with this id")
        return result

    #for post requests+adding new words to the database
    @marshal_with(resource_fields)
    def put(self, word_id):
        args = word_put_args.parse_args()

        result = WordModel.query.filter_by(id="word_id").first()
        if result:
            abort (409, message="Word id taken...")
            #we already have this word ID so you can't use it

        word = WordModel(id=word_id, name = args['name'], views =args['views'], vowel = args['vowel'])
        db.session.add(word)
        db.session.commit()
        return word,201 

    #for deleting words
    def delete(self,word_id):
        abort_if_word_id_not_there(word_id)
        del words[word_id]
        return '', 204




#register the resource and specifiy how it can be accessed
api.add_resource(Word, "/word/<int:word_id>")



if __name__ == "__main__":  
    app.run(debug = True)