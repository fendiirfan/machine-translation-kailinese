from fastapi import FastAPI
from src.translator import Predict
import pandas as pd
import asyncio
import datetime
import pytz


app = FastAPI()

contribute_lock = asyncio.Lock()
translate_semaphore = asyncio.Semaphore(3)

@app.post("/translate")
async def translate(user_input: str, lang_src: str):
    async with translate_semaphore:
        obj = Predict(user_input,lang_src)
        return {"prediction": obj.translate()}


@app.post("/contribute")
async def contribute(indonesian_user_input: str, kailinese_user_input: str):
    try:
        # Acquire lock to prevent concurrent access to the file
        async with contribute_lock:
            # Get the current time in WIB timezone
            wib_timezone = pytz.timezone('Asia/Jakarta')
            created_datetime = datetime.datetime.now(wib_timezone)
            formatted_datetime = created_datetime.strftime('%d-%m-%YT%H:%M')


            csv_path = 'input/mt-kaili-contribute.csv'

            # Load the CSV file
            df = pd.read_csv(csv_path)

            # Create a new row with the contributed data
            new_row = {'indonesian': indonesian_user_input, 
                        'kailinese': kailinese_user_input, 
                        'created_datetime': formatted_datetime}

            # Append the new row to the existing dataframe
            df = df.append(new_row, ignore_index=True)

            # Write the updated dataframe back to the CSV file
            df.to_csv(csv_path, index=False)

            # Return a success message
            return {'message': 'Contribution added successfully. Thank you 😊'}
    except Exception as e:
        # If there is an error, log it and return an error message
        logging.error(str(e))
        return {'error': f'{str(e)}'}



