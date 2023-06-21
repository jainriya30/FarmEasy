from flask import Flask, render_template, request, abort
from models import CropRecommendationModel, PricePredictionModelManager, ProductionStatsModel, CropNotFoundException, StateNotFoundException, crop_details
import traceback
import json

crop_recommender = CropRecommendationModel()
prices_predictor = PricePredictionModelManager()
crop_stats = ProductionStatsModel()

app = Flask(__name__, static_url_path='/')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

ALL_MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

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

            recommendations = crop_recommender.recommend(n, p, k, temperature, humidity, ph, rainfall)            

            return render_template("results.html", recommendations=recommendations)

        except KeyError as e:
            traceback.print_exc()
            abort(400)

    return render_template('crop_recommendation.html')

@app.route('/price-prediction')
def price_prediction_page():
    return render_template('price_prediction.html', price_data=prices_predictor.get_stats_for_current_month())

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

@app.route('/commodity/<crop>')
def index(crop):
    if crop in PricePredictionModelManager.ALL_CROPS:
        monthly_data = prices_predictor.predict_prices_for_next_8_months(crop)
        months_as_list = json.dumps([f"{ALL_MONTHS[data[1]]} {data[0]}" for data in monthly_data])
        values_as_list = list(monthly_data.values())
        monthly_data = (months_as_list, values_as_list)

        last_month_price = prices_predictor.predict_price_for_last_month(crop)
        crop_data = crop_details(crop)
        top_producers = None
        try:
            top_producers = crop_stats.top_states_for_crop(crop)
        except CropNotFoundException:
            top_producers = crop_data["states"]
        return render_template("commodity.html", crop_name=crop, last_month_price=last_month_price, monthly_data=monthly_data, crop_info=crop_data, top_producers=top_producers)
    else:
        abort(404)

@app.route('/test')
def test():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True)
