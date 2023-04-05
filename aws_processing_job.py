import boto3
import time
import json


def star_job():
    processing_job_name = f"json-generation-{int(time.time())}"
    sagemaker_client = boto3.client("sagemaker")

    response = sagemaker_client.create_processing_job(
        ProcessingJobName=processing_job_name,
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.t3.medium",
                "VolumeSizeInGB": 8,
            }
        },
        AppSpecification={
            "ImageUri": "",
            "ContainerEntrypoint": [
                "python3",
                "/opt/ml/processing/json_generator.py",
            ],
        },
        NetworkConfig={
            "EnableNetworkIsolation": False,
        },
        RoleArn="",
        StoppingCondition={
            "MaxRuntimeInSeconds": 720
        }
    )

    processing_job_arn = response["ProcessingJobArn"]
    print(f"Processing job ARN: {processing_job_arn}")
    return processing_job_name


def stop_job(job_name):
    sagemaker = boto3.client('sagemaker')

    sagemaker.stop_processing_job(ProcessingJobName=job_name)
    print("job is stopped")


def get_log_stream_name(job_name):
    logs_client = boto3.client('logs')

    log_group_name = '/aws/sagemaker/ProcessingJobs'

    response = logs_client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True
    )

    log_streams = response['logStreams']

    for log_stream in log_streams:
        if log_stream['logStreamName'].startswith(job_name):
            return log_stream['logStreamName']


def log_retrieve(job_name):

    cloudwatch_logs = boto3.client('logs')

    # Specify the log group name and log stream name
    log_group_name = '/aws/sagemaker/ProcessingJobs'
    log_stream_name = get_log_stream_name(job_name)

    # Filter the log events
    response = cloudwatch_logs.filter_log_events(
        logGroupName=log_group_name,
        logStreamNames=[log_stream_name],
        limit=10000
    )

    event_length = len(response['events'])-1

    return response['events'][event_length]['message']


def load_data(job_name):
    try:
        data = log_retrieve(job_name)
        data_to_string = json.loads(data)

        data_to_json = json.dumps(data_to_string, indent=4)
        print(data_to_json)

        with open("data.json", "w") as f:
            f.write(data_to_json)
    except Exception as e:
        print('no data')
