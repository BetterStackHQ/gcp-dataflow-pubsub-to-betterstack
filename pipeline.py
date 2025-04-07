import argparse
import json
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows
import requests
import gzip
from typing import Dict, Any, List
from datetime import timedelta

class PubSubToBetterStack(beam.DoFn):
    def __init__(self, source_token: str, ingesting_host: str, batch_size: int):
        self.source_token = source_token
        self.ingesting_url = ingesting_host if '://' in ingesting_host else f'https://{ingesting_host}'
        self.batch_size = batch_size
        self.headers = {
            'Authorization': f'Bearer {source_token}',
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'
        }
        self.batch = []

    def process(self, element: bytes) -> None:
        try:
            # Parse the Pub/Sub data
            data = json.loads(element.decode('utf-8'))
            
            # Rename timestamp key to dt to be understood by Better Stack
            if 'timestamp' in data:
                data['dt'] = data.pop('timestamp')
            
            self.batch.append(data)
            
            # If we've reached the batch size, send the batch
            if len(self.batch) >= self.batch_size:
                self._send_batch()
                
        except Exception as e:
            # Log the error but don't fail the pipeline
            print(f"Error processing message: {str(e)}")

    def finish_bundle(self):
        # Send any remaining messages in the batch
        if self.batch:
            self._send_batch()

    def _send_batch(self):
        try:
            # Convert batch to JSON and compress with gzip
            json_data = json.dumps(self.batch)
            compressed_data = gzip.compress(json_data.encode('utf-8'))
            
            # Send compressed batch to Better Stack
            response = requests.post(
                self.ingesting_url,
                headers=self.headers,
                data=compressed_data
            )
            
            if response.status_code != 202:
                raise Exception(f"Failed to send to Better Stack: {response.text}")
                
            # Clear the batch after successful send
            self.batch = []
                
        except Exception as e:
            # Log the error but don't fail the pipeline
            print(f"Error sending batch to Better Stack: {str(e)}")

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_subscription',
        required=True,
        help='The name of the Pub/Sub subscription to read from'
    )
    parser.add_argument(
        '--better_stack_source_token',
        required=True,
        help='The source token of your telemetry source in Better Stack'
    )
    parser.add_argument(
        '--better_stack_ingesting_host',
        required=True,
        help='The ingesting host of your telemetry source in Better Stack'
    )
    parser.add_argument(
        '--batch_size',
        default=100,
        type=int,
        help='Number of messages to batch before sending to Better Stack'
    )
    parser.add_argument(
        '--window_size',
        default=10,
        type=int,
        help='Window size in seconds for batching messages'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(
        pipeline_args,
        save_main_session=True
    )

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                subscription=known_args.input_subscription
            )
            | 'Window into fixed windows' >> beam.WindowInto(
                FixedWindows(known_args.window_size)
            )
            | 'Send to Better Stack' >> beam.ParDo(
                PubSubToBetterStack(
                    known_args.better_stack_source_token,
                    known_args.better_stack_ingesting_host,
                    known_args.batch_size
                )
            )
        )

if __name__ == '__main__':
    run() 
