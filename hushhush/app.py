from hh_email.email_sender import *
from flask_cors import CORS
from flask import Flask, request
from data_manipulation.model_creation import *
from database.util import *
from scoring_system.scoring_model import get_top_users
from stackexchange_api.extract_data_from_api import fetch_data_from_api
from scraping import collect_urls, extract_profile_data

app = Flask(__name__)
CORS(app)


@app.route('/execute_recruiting_process', methods=['POST'])
def execute_recruiting_process():
    content_type = request.headers.get('Content-Type')

    users_list = list()

    if content_type == 'application/json':
        body = request.json

        if body['scrape_stackoverflow_data']:
            collect_urls.execute()
            extract_profile_data.execute()
            print("Finished Scraping Data from Stackover.")

        if body['fetch_data_from_stackexchange_api']:
            fetch_data_from_api()
            print("Finished Fetching Data via Stackexchange.")

        if body['train_model_again']:
            data = get_refined_user_data()
            create_and_save_questions_predicting_model(data)
            create_and_save_answers_predicting_model(data)
            print("Finished Training the Models on Data and Saved the Models.")

        if body['fetch_top_users']:
            user_count = body['users_count']
            users_list = get_top_users(user_count)
            print("Finished Fetching Top Users.")

        if body['send_email_to_user']:
            for user in users_list:
                update_user_selection_status(user['account_id'], True)
                send_exam_link(str(user['account_id']), user['email_id'])
            print("Finished Sending Email to Selected Candidates.")

    return users_list


@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        try:
            body = request.json

            if body['final_answer'] == "CAB":
                update_user_exam_status(body['account_id'], True, True)
                send_interview_invitation(get_user_email_id(body['account_id']))
            else:
                update_user_exam_status(body['account_id'], True, False)
                send_test_response(get_user_email_id(body['account_id']))

            return {"message": True}
        except Exception as e:
            print(e)

    return {"message": False}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)
