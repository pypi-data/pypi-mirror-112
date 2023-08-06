import logging

from torch_sdk.events.job_events import JobStartEvent
from torch_sdk.events.log_events import LogEvent
from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

# Set up torch_sdk_code client
torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

# create pipeline object
pipeline = CreatePipeline(
    uid='monthly_reporting-40',
    name='Monthly reporting Pipeline-40',
    description='Pipeline to create monthly reporting tables',
    meta=PipelineMetadata('vaishvik', 'torch_sdk_code', '...'),
    context={'key1': 'value1'}
)
# creating pipeline using torch_sdk_code client
pipeline_response = torch_client.create_pipeline(pipeline=pipeline)
print('Newly Created Pipeline Response : ', pipeline_response)


# create a pipeline run of the pipeline
pipelineRunResponse = pipeline_response.create_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'})
print('pipeline Run Created :', pipelineRunResponse)

# update a pipeline run of the pipeline
update_pipeline_res = pipelineRunResponse.update_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'},
                                                              result=PipelineRunResult.SUCCESS,
                                                              status=PipelineRunStatus.COMPLETED)
print('pipeline run updated :', update_pipeline_res)

# create span in the pipeline run
span_context = pipelineRunResponse.create_span(uid='span_uid_40')
print('Span Created :', span_context)

# start span event
# print('Span Start Event Response :', spanContext.start({'k': 'v'}))

# check current span is root or not
print('span is root or not : ', span_context.is_root())

job_start_event = JobStartEvent(context_data={'job':'start job'})

log_event = LogEvent(log_data='this is log event -ex2')
# send log event for the current span
print('Span job start event Response :', span_context.send_event(span_event= job_start_event))
print('Span log event Response :', span_context.send_event(span_event= log_event))

# # send custom event
# print('Span Custom Event Response :', span_context.send_custom_event(event_type='CUSTOM_EVENT', context_data={'custom_key': 'custom_value'}))

# end the span event
print('Span End Event Response :', span_context.end())
