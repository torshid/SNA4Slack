from flask import *
from GraphInfo import do_it
import os, uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route("/")
def hello():
    #json_data = do_it(api_key='',threshold = 0,sna_metric = 'Degree')
    #print(json_data)
    return render_template('home.html')

@app.route('/show', methods = ['POST', 'GET'])
def show():
    key = request.form['slack-key']
    #threshold = request.form['threshold']
    sna_metric = request.form['sna-metric']
    
    json_data = do_it(key,0,sna_metric)
    print(json_data)
    # need to save the data
    # graph uses cached data have to make new file and send that filename to html
    # so we can see it in alchemy config
    save_path = './static/graph_data'
    file_name = str(uuid.uuid4()) + ".json"
    realFileName = os.path.join(save_path, file_name)
    file = open(realFileName,'w+')
    file.write(json_data)
    file.close()

    allFiles = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))]
    for f in allFiles:
        if f != file_name and f != '.gitignore':
            try:
                os.remove(os.path.join(save_path, f))
            except OSError as e:
                print(e)

    return render_template('graph.html',file_name=file_name)

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug= True)
