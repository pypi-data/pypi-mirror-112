import os
import gdown

from sani_nlu.constants import MODEL_DIR, MODEL_NAME, BASE_URL

def initializeFolder():
	if not os.path.exists(MODEL_DIR):
		os.mkdir(MODEL_DIR)
		print("Directory ", MODEL_DIR," created")

def download_model():
    model_path = MODEL_DIR + MODEL_NAME

    if os.path.isfile(model_path) != True:
        print(f"{MODEL_NAME} will be downloaded...")
        gdown.download(BASE_URL + MODEL_NAME, model_path, quiet=False)

    return model_path