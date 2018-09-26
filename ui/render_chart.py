from flask import Flask, Markup, render_template
import scrape, json

app = Flask(__name__)

labels = []
values = []

data = json.loads(scrape.get_posts_from_db())

for entry in data['history']:
    label = entry['update_time']
    value = entry['total_cashout']
    labels.append(label)
    values.append(value)

@app.route('/')
def chart():
    return render_template( 
                            'chart.html', 
                            title="What are your shares worth now?", 
                            labels=labels, 
                            values=values,
                            max=15000,
                            min=10500
                            )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
