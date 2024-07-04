#%%
import sys
sys.path.append('G:\Shared drives\RPA')
import web_in_mpd.database.database as db
from google.cloud import bigquery
from flask import Flask, render_template, request,Blueprint

main = Blueprint('main', __name__)

def get_tracking(table_name, condition):
    if condition[0] == '0':
        condition =  '66' + condition[1:]
    print(condition)
    bigquery_client   = db.database.get_google_qigquery()
    query = f"""
        SELECT *
        FROM `{table_name}`
        WHERE recipient_phone = @condition
    """

    query_params = [
        bigquery.ScalarQueryParameter("condition", "STRING", condition)
    ]

    # Configure the job
    job_config = bigquery.QueryJobConfig(
        query_parameters=query_params
    )

    # Run the query
    query_job = bigquery_client.query(query, job_config=job_config)
    results = query_job.result()
    return results

table_name = 'mpd-dekmeepoom.warehouse.all_tracking'


#app = Flask(__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    telephone_no = request.form.get('telephone_no', '')

    if telephone_no:
        result =  get_tracking(table_name, telephone_no)
        if result.total_rows > 0:
            result_list = [dict(row) for row in result]
            return render_template('tracking_for_customer.html', result=result_list)
        else:
            return render_template('tracking_for_customer.html', result=None, error="ไม่พบข้อมูล ! กรุณาตรวจสอบหมายเลขโทรศัพท์ให้ถูกต้องอีกครั้ง")

    return render_template('tracking_for_customer.html', result=None)
