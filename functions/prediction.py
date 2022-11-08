import json
import time
from functions.aws_clients import lambda_client, lambda_function_name
import json
import time


def predict_sentiments(df, utterance_field, placeholder_progress_bar):
    predict_progress_bar = placeholder_progress_bar.progress(0)
    predicted_sentiment = []
    confidence_score = []
    i = 0
    for index, row in df.iterrows():
        i = i+1
        query_string = json.dumps({"utterance": row[utterance_field]})
        lambda_payload_str = json.dumps({"body": query_string})

        retry_attempts = 0

        while True:
            lambda_response = lambda_client.invoke(
                FunctionName=lambda_function_name,
                InvocationType='RequestResponse',
                Payload=bytes(lambda_payload_str, "utf-8")
            )

            if lambda_response['StatusCode'] == 200:
                response_payload = lambda_response['Payload'].read()
                response_dict = json.loads(response_payload)
                if response_dict['statusCode'] != 200:
                    print('Prediction error: ', response_dict['statusCode'])
                else:
                    response = json.loads(response_dict['body'])
                    predicted_sentiment.append(response['predictions'])
                    confidence_score.append(response['confidence score'])
                break

            else:
                if retry_attempts == 3:
                    predicted_sentiment.append(None)
                    confidence_score.append(None)
                    print(
                        f'Unable to get response for case index {index} after 3 attempts. Returning null.')
                    break
                else:
                    print(f'Unable to get response for case index {index}')
                    print(
                        f'Retrying in 5 seconds. Current attempt: {retry_attempts + 1}')
                    time.sleep(5)
                    retry_attempts += 1

        if predict_progress_bar:
            predict_progress_bar.progress(i/df.shape[0])

    df['Predicted sentiment'] = predicted_sentiment
    df['Confidence score'] = confidence_score

    return df
