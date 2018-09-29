from flask import Flask, Markup, render_template
import json, requests, os

app = Flask(__name__)



@app.route('/')
def chart():
    labels = []
    values = []

    api = os.environ['API']
    url = "%s/api/history" % api
    payload = requests.get(url)
    data = json.loads(json.loads(payload.text))

    for entry in data['history']:
        label = entry['update_time']
        value = entry['total_cashout']
        labels.append(label)
        values.append(value)
        
    return render_template( 
                            'chart.html', 
                            title="What are your shares worth now?", 
                            labels=labels[::-1], 
                            values=values[::-1],
                            max=15000,
                            min=10500
                            )

def newmethod282():
    def chart():
        labels = []
        values = []

        api = os.environ['API']
        url = "%s/api/history" % api
        payload = requests.get(url)
        data = json.loads(json.loads(payload.text))

        for entry in data['history']:
            label = entry['update_time']
            value = entry['total_cashout']
            labels.append(label)
            values.append(value)

        return render_template( 
                                'chart.html', 
                                title="What are your shares worth now?", 
                                labels=labels[::-1], 
                                values=values[::-1],
                                max=15000,
                                min=10500
                                )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    # print(type(data), data)
