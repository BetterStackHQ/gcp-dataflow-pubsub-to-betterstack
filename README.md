# Google Cloud Pub/Sub to [Better Stack](https://betterstack.com/logs)

[![Better Stack dashboard](https://raw.githubusercontent.com/BetterStackHQ/logs-client-serilog/main/dashboard.png)](https://betterstack.com/telemetry)

[![ISC License](https://img.shields.io/badge/license-ISC-ff69b4.svg)](LICENSE.md)

Experience SQL-compatible structured log management based on ClickHouse. [Learn more ⇗](https://betterstack.com/telemetry)

## Documentation

[Getting started ⇗](https://betterstack.com/docs/logs/google-cloud-pubsub/)

## Need help?
Please let us know at [hello@betterstack.com](mailto:hello@betterstack.com). We're happy to help!

## Releasing new version

After making changes, rebuild the Docker image and the Dataflow template:

```bash
docker build --tag betterstack/gcp-dataflow-pubsub-to-betterstack .
docker push betterstack/gcp-dataflow-pubsub-to-betterstack
gcloud dataflow flex-template build gs://betterstack/pubsub-to-betterstack.json \
    --image "docker.io/betterstack/gcp-dataflow-pubsub-to-betterstack" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json"
```

Requires access to `betterstack` Docker Hub repository, and `betterstack` Google Cloud Bucket.

---

[ISC license](LICENSE.md)
