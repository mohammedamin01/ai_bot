import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    CRYPTO_COMPARE_API_KEY = os.environ.get('CRYPTO_COMPARE_API_KEY') or 'your-crypto-compare-api-key'
    DATA_FILE_PATH = os.environ.get('DATA_FILE_PATH') or 'data/historical_data.csv'
    RNN_MODEL_PATH = os.environ.get('RNN_MODEL_PATH') or 'models/rnn_model.h5'
    CNN_MODEL_PATH = os.environ.get('CNN_MODEL_PATH') or 'models/cnn_model.h5'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
