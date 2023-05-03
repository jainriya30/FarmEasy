_crop_data = {
  "wheat": {
    "states": "U.P., Punjab, Haryana, Rajasthan, M.P., Bihar",
    "type": "rabi",
    "countries": "Sri Lanka, United Arab Emirates, Taiwan"
  },
  "paddy": {
    "states": "W.B., U.P., Andhra Pradesh, Punjab, T.N.",
    "type": "kharif",
    "countries": "Bangladesh, Saudi Arabia, Iran"
  },
  "barley": {
    "states": "Rajasthan, Uttar Pradesh, Madhya Pradesh, Haryana, Punjab",
    "type": "rabi",
    "countries": "Oman, UK, Qatar, USA"
  },
  "maize": {
    "states": "Karnataka, Andhra Pradesh, Tamil Nadu, Rajasthan, Maharashtra",
    "type": "kharif",
    "countries": "Hong Kong, United Arab Emirates, France"
  },
  "bajra": {
    "states": "Rajasthan, Maharashtra, Haryana, Uttar Pradesh and Gujarat",
    "type": "kharif",
    "countries": "Oman, Saudi Arabia, Israel, Japan"
  },
  "copra": {
    "states": "Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Orissa, West Bengal",
    "type": "rabi",
    "countries": "Veitnam, Bangladesh, Iran, Malaysia"
  },
  "cotton": {
    "states": "Punjab, Haryana, Maharashtra, Tamil Nadu, Madhya Pradesh, Gujarat",
    "type": " China, Bangladesh, Iran, Malaysia"
  },
  "masoor": {
    "states": "Uttar Pradesh, Madhya Pradesh, Bihar, West Bengal, Rajasthan",
    "type": "rabi",
    "countries": "Pakistan, Cyprus,United Arab Emirates"
  },
  "gram": {
    "states": "Madhya Pradesh, Maharashtra, Rajasthan, Uttar Pradesh, Andhra Pradesh & Karnataka",
    "type": "rabi",
    "countries": "Veitnam, Spain, Myanmar"
  },
  "groundnut": {
    "states": "Andhra Pradesh, Gujarat, Tamil Nadu, Karnataka, and Maharashtra",
    "type": "kharif",
    "countries": "Indonesia, Jordan, Iraq"
  },
  "arhar": {
    "states": "Maharashtra, Karnataka, Madhya Pradesh and Andhra Pradesh",
    "type": "kharif",
    "countries": "United Arab Emirates, USA, Chicago"
  },
  "sesamum": {
    "states": "Maharashtra, Rajasthan, West Bengal, Andhra Pradesh, Gujarat",
    "type": "rabi",
    "countries": "Iraq, South Africa, USA, Netherlands"
  },
  "jowar": {
    "states": "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Gujarat",
    "type": "kharif",
    "countries": "Torronto, Sydney, New York"
  },
  "moong": {
    "states": "Rajasthan, Maharashtra, Andhra Pradesh",
    "type": "rabi",
    "countries": "Qatar, United States, Canada"
  },
  "niger": {
    "states": "Andha Pradesh, Assam, Chattisgarh, Gujarat, Jharkhand",
    "type": "kharif",
    "countries": "United States of American,Argenyina, Belgium"
  },
  "rape": {
    "states": "Rajasthan, Uttar Pradesh, Haryana, Madhya Pradesh, and Gujarat",
    "type": "rabi",
    "countries": "Veitnam, Malaysia, Taiwan"
  },
  "jute": {
    "states": " West Bengal , Assam , Orissa , Bihar , Uttar Pradesh",
    "type": "kharif",
    "countries": "JOrdan, United Arab Emirates, Taiwan"
  },
  "safflower": {
    "states": "Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Orissa",
    "type": "kharif",
    "countries": " Philippines, Taiwan, Portugal"
  },
  "soyabean": {
    "states": "Madhya Pradesh, Maharashtra, Rajasthan, Madhya Pradesh and Maharashtra",
    "type": "kharif",
    "countries": "Spain, Thailand, Singapore"
  },
  "urad": {
    "states": "Andhra Pradesh, Maharashtra, Madhya Pradesh, Tamil Nadu",
    "type": "rabi",
    "countries": "United States, Canada, United Arab Emirates"
  },
  "ragi": {
    "states": "Maharashtra, Tamil Nadu and Uttarakhand",
    "type": "kharif",
    "countries": "United Arab Emirates, New Zealand, Bahrain"
  },
  "sunflower": {
    "states": "Karnataka, Andhra Pradesh, Maharashtra, Bihar, Orissa",
    "type": "rabi",
    "countries": "Phillippines, United States, Bangladesh"
  },
  "sugarcane": {
    "states": "Uttar Pradesh, Maharashtra, Tamil Nadu, Karnataka, Andhra Pradesh",
    "type": "kharif",
    "countries": "Kenya, United Arab Emirates, United Kingdom"
  }
}

def crop_details(crop_name):
    return _crop_data[crop_name]
