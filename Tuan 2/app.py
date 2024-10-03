from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Route to display the form and result
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_count = int(request.form['num_count'])  # Get the number of random numbers to generate
            if 1 <= num_count <= 999:
                random_numbers = [random.randint(1, 999) for _ in range(num_count)]  # Generate random numbers
                return render_template('index.html', numbers=random_numbers)
            else:
                error = "Please enter a number between 1 and 999."
                return render_template('index.html', error=error)
        except ValueError:
            error = "Invalid input! Please enter a valid number."
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
