import json
import time
import base64
import logging
import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS  # type: ignore

from biolib.biolib_binary_format import SavedJob
from biolib.compute_node.compute_process import compute_process_config
from biolib.compute_node.webserver import webserver_utils
from biolib.compute_node.webserver import webserver_config
from biolib.compute_node.webserver.gunicorn_flask_application import GunicornFlaskApplication
from biolib.biolib_logging import logger, TRACE

app = Flask(__name__)
CORS(app)


@app.route('/hello/')
def hello():
    return 'Hello'


@app.route('/v1/job/', methods=['POST'])
def start_job():
    saved_job = json.loads(request.data.decode())

    if not webserver_utils.validate_saved_job(saved_job):
        return jsonify({'job': 'Invalid job'}), 400

    job_id = saved_job['job']['public_id']
    saved_job['BASE_URL'] = webserver_utils.BASE_URL

    compute_state = webserver_utils.get_compute_state(webserver_utils.UNASSIGNED_COMPUTE_PROCESSES)
    compute_state['job_id'] = job_id
    webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id] = compute_state

    if webserver_utils.RUNNING_IN_ENCLAVE:
        saved_job['enclave_ecr_token'] = webserver_utils.ENCLAVE_ECR_TOKEN
        if not webserver_utils.DEV_MODE:
            # Cancel the long general timer and replace with shorter shutdown timer
            webserver_utils.start_shutdown_timer(webserver_config.COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES)

    saved_job_bbf_package = SavedJob().serialize(json.dumps(saved_job))
    send_package_to_compute_process(job_id, saved_job_bbf_package)

    if webserver_utils.RUNNING_IN_ENCLAVE:
        return Response(base64.b64encode(compute_state['attestation_document']), status=201)
    else:
        return '', 201


@app.route('/v1/job/<job_id>/start/', methods=['POST'])
def start_compute(job_id):
    module_input_package = request.data
    send_package_to_compute_process(job_id, module_input_package)
    return '', 201


@app.route('/v1/job/<job_id>/status/')
def status(job_id):
    # TODO Implement auth token
    current_status = webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['status'].copy()
    response = jsonify(current_status)

    if current_status['status_updates']:
        webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['status']['status_updates'] = []

    # Check if any error occurred
    if 'error_code' in current_status:
        response.call_on_close(lambda: webserver_utils.finalize_and_clean_up_compute_job(job_id))

    return response


@app.route('/v1/job/<job_id>/result/')
def result(job_id):
    if webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['result']:
        result_data = webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['result']
        # remove result from state dict, so we know the user has started the download
        webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['result'] = None
        response = Response(result_data)
        response.call_on_close(lambda: webserver_utils.finalize_and_clean_up_compute_job(job_id))

        return response
    else:
        return '', 404


def send_package_to_compute_process(job_id, package_bytes):
    message_queue = webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT[job_id]['messages_to_send_queue']
    message_queue.put(package_bytes)


def start_webserver(port, host, specified_biolib_host, is_running_in_enclave=False):
    webserver_utils.BASE_URL = specified_biolib_host

    if is_running_in_enclave:
        webserver_utils.RUNNING_IN_ENCLAVE = True

    def worker_exit(server, worker):  # pylint: disable=unused-argument
        active_compute_states = list(
            webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT.values()) + webserver_utils.UNASSIGNED_COMPUTE_PROCESSES
        logger.debug(f'Sending terminate signal to {len(active_compute_states)} compute processes')
        if active_compute_states:
            for compute_state in active_compute_states:
                if compute_state['worker_thread']:
                    compute_state['worker_thread'].terminate()
            time.sleep(2)
        return

    def post_fork(server, worker):  # pylint: disable=unused-argument
        logger.info("Started compute node")
        webserver_utils.start_compute_process(webserver_utils.UNASSIGNED_COMPUTE_PROCESSES,
                                              webserver_utils.RUNNING_IN_ENCLAVE)

        if webserver_utils.RUNNING_IN_ENCLAVE:
            res = requests.get(f'{compute_process_config.PARENT_REST_SERVER_URL}/init_enclave/')
            enclave_data = res.json()
            webserver_utils.COMPUTE_NODE_INFO = enclave_data['compute_node_info']
            webserver_utils.BASE_URL = enclave_data['base_url']
            webserver_utils.ENCLAVE_ECR_TOKEN = enclave_data['enclave_ecr_token']
            webserver_utils.DEV_MODE = enclave_data['dev_mode']
            webserver_utils.report_availability(webserver_utils.COMPUTE_NODE_INFO, webserver_utils.BASE_URL,
                                                webserver_utils.DEV_MODE)

    if logger.level == TRACE:
        gunicorn_log_level_name = 'DEBUG'
    elif logger.level == logging.DEBUG:
        gunicorn_log_level_name = 'INFO'
    elif logger.level == logging.INFO:
        gunicorn_log_level_name = 'WARNING'
    else:
        gunicorn_log_level_name = logging.getLevelName(logger.level)

    options = {
        'bind': f'{host}:{port}',
        'workers': 1,
        'post_fork': post_fork,
        'worker_exit': worker_exit,
        'timeout': webserver_config.GUNICORN_REQUEST_TIMEOUT,
        'graceful_timeout': 4,
        'loglevel': gunicorn_log_level_name,
    }

    GunicornFlaskApplication(app, options).run()
