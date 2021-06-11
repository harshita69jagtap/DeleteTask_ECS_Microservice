from flask import Flask, request, redirect,jsonify
import requests
import sys, traceback

##### directory structure - 
##/root/project/deletetask.py
#### this service has no front end therefore no templates/ folder

###dependencies installed
### yum install -y tree python3 python3-pip
### pip3 install flask requests


app = Flask(__name__)

@app.route('/', methods=['GET']) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
def index(): #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    print(" HTTP GET REQUEST FROM pub-alb for health check ON PRIVATE IP - {0}".format(request.method)) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    return(jsonify({'status':'HEALTH CHECK FROM PUB-ALB'})) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH

@app.route('/deletetask/<int:id>', methods=['GET'])

def deletetask(id):

    try:
        r = requests.get('http://dns-name-of-priv-alb:80/dbtask', params = {'service':'deletetask','id': id})
        resp = r.json()
        if resp['status'] == 'deleted':
            return redirect('http://dns-name-of-pub-alb:80/viewtask')  #### redirect is always http get request on public ip of the service
        elif resp['status'] == 'exists':
            return jsonify({'status':'NOT DELETED FROM DB'})
        elif resp['status'] == 'exception in delete DBTASK':
            return jsonify({'status':'EXCEPTION OCCURED IN DELETE OF DBTASK'})
        


    except Exception:
        print("EXCEPTION OCCURED IN /DELETETASK/ID SERVICE")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return jsonify({'status':'EXCEPTION OCCURED IN /DELETETASK/ID SERVICE'})
                

    

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000', debug=True)
