# Holds constants common to all ML modules

import os

# Path of the current package
PACKAGE_DIR = os.path.dirname(__file__)

# Path where pre-trained models could be available
PRE_TRAINED_MODELS_DIR_PATH = os.path.join(PACKAGE_DIR, 'pretrained_models')

# Path where the datasets required by the module are located
DATASETS_DIR_PATH = os.path.join(PACKAGE_DIR, 'datasets')

# Path where the price datasets of each crop is present
PRICE_DATASETS_DIR_PATH = os.path.join(DATASETS_DIR_PATH, 'crop_price_data')