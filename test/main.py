from flask import Flask, render_template, request, abort
from models import CropRecommendationModel, PricePredictionModelManager, ProductionStatsModel, CropNotFoundException, StateNotFoundException
import traceback
import json

crop_recommender = CropRecommendationModel()
crop_stats = ProductionStatsModel()

app = Flask(__name__, static_url_path='/')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/location-select')
def home():
    return render_template('location_select.html')

CROP_RECOMMENDATION_ARGS = ['temperature', 'humidity', 'rainfall', 'ph', 'n-val', 'p-val', 'k-val']

@app.route('/crop-recommendation', methods=["GET", "POST"])
def crop_prediction_page():
    if request.method == "POST":
        try:
            temperature = request.form["temperature"]
            humidity = request.form["humidity"]
            rainfall = request.form["rainfall"]
            ph = request.form["ph"]
            n = request.form["n-val"]
            p = request.form["p-val"]
            k = request.form["k-val"]

            crop = crop_recommender.recommend(n, p, k, temperature, humidity, ph, rainfall)

            return json.dumps(crop)

        except KeyError as e:
            traceback.print_exc()
            abort(e)

    return render_template('crop_recommendation.html')

@app.route('/price-prediction')
def price_prediction_page():
    return render_template('price_prediction.html')

@app.route('/top-crops')
def top_crops():
    data = crop_stats.top_states_for_all_crops()
    for d in data:
        data[d] = json.dumps(data[d]).title()
    
    return render_template('top_crops.html', crops=ProductionStatsModel.CROPS, crop_data=data)

@app.route('/list-all-states')
def list_all_states():
    return json.dumps(ProductionStatsModel.STATES)

@app.route('/list-all-crops')
def list_all_crops():
    return json.dumps(ProductionStatsModel.CROPS)

@app.route('/mapdata.js')
def mapdata_js():
    return render_template('mapdata.js', states=['', 'Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra And Nagar Haveli', 'Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', '', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttaranchal', 'West Bengal', 'Jammu And Kashmir', 'Telangana', 'Ladakh'], crop_data=crop_stats.top_crops_for_all_states()), 200, {'Content-Type': 'text/js; charset=utf-8'}

@app.route('/top-crops-for-state', methods=["GET"])
def top_crops_for_state():
    if "state" in request.args:
        state = request.args["state"]
        try:
            data = crop_stats.top_crops_for_state(state)
            return json.dumps(data)
        except StateNotFoundException:
            abort(404)
        except:
            print("/top-crops-for-state (args): ", request.args)
            traceback.print_exc()
            abort(500)
            
    return abort(403)

@app.route('/top-states-for-crop', methods=["GET"])
def top_states_for_crop():
    if "crop" in request.args:
        crop = request.args["crop"]
        try:
            data = crop_stats.top_states_for_crop(crop)
            return json.dumps(data)
        except StateNotFoundException:
            abort(404)
        except:
            print("/top-states-for-crop (args): ", request.args)
            traceback.print_exc()
            abort(500)
            
    return abort(403)

# @app.route('/top-state-for-crops', methods=["GET"])
# def top_state_for_crops():
#     if "state" in request.args:
#         state = request.args["state"]
#         try:
#             data = crop_stats.top_crops_for_state(state)
#             return json.dumps(data)
#         except StateNotFoundException:
#             abort(404)
#         except:
#             print("/top-crops-for-state (args): ", request.args)
#             traceback.print_exc()
#             abort(500)
            
#     return abort(403)

@app.route('/test')
def test():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True)
    
