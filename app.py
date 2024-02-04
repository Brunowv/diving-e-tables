from flask import Flask, request, render_template
app = Flask(__name__)
def buhlmann(depth, time, temperature, salinity, gas_mix, altitude): # this gave me headache
    try:
        gas_mix = gas_mix.strip() # Remove any whitespaces characters from the gas
        gas_mix_value = float(gas_mix) # Convert gas_mix to a float
    except ValueError:
        raise ValueError("Gas mix is not a valid number")
    if salinity == "Mar Rojo":
        salinity_value = 40 # salinity of the red Sea
    elif salinity == "Mar Mediterraneo":
        salinity_value = 38 # Salinity of the Mediterranean Sea
    elif salinity == "Mar de la China":
        salinity_value = 32 # Salinity of the Suth China Sea
    elif salinity == "Mar de Indonesia":
        salinity_value = 34 # Salinity of the Indonesian Sea
    elif salinity == "Mar de Japón":
        salinity_value = 36 # Salinity of the Japanese Sea
    elif salinity == "Mar de Australia":
        salinity_value = 35 # Salinity of the Australian Sea
    else:
        salinity_value = 35 # Default salinity 
# Aquí va la lógica para calcular el tiempo de descompresión
    t_immersion = float(depth) + float(time) + float(temperature) + float(salinity_value) + gas_mix_value
# Calculate the descompression time
    t_descompression = t_immersion * 2 # this is an eg, i have to replace it with real logic
    altitude_value = float(altitude) # Convert altitude to a float
    descompression_time = t_descompression + (altitude_value * 0.01) # Add the altitude correction to the descompression time
    return t_immersion, descompression_time    # i still have to add and replace logic
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/calculate")
def calculate():
    depth = request.args.get("depth")
    time = request.args.get("time")
    temperature = request.args.get("temperature")
    salinity = request.args.get("salinity")
    gas_mix = request.args.get("gas_mix")
    altitude = request.args.get("altitude")
    try:
        t_immersion, t_descompression = buhlmann(depth, time, temperature, salinity, gas_mix, altitude)
    except ValueError as e:
        return render_template("error.html", message=str(e)), 400
    return render_template("result.html", t_immersion=t_immersion, t_descompression=t_descompression)
if __name__ == "__main__":
    app.run(debug=True)