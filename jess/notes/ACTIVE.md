# Add opentelemetry

The first goal is to do a standard installation of OpenTelemetry.
I should be able to set some environment variables and see the existing logs exported to Honeycomb.

# Run the app

First, I need to see the 'before' behavior, and make sure I can run the app at all.
I want to run it in headless mode.

[] Create `oh-headless` script that runs it with a default request

[] get it to operate on a small repository, like jessitron/simple-web-page. That'll save tokens during our testing.

# Install OTel

Instructions are here: https://docs.honeycomb.io/send-data/python/opentelemetry-sdk/#add-automatic-instrumentation

[] poetry add opentelemetry-instrumentation \
    opentelemetry-distro \
    opentelemetry-exporter-otlp

[] poetry run opentelemetry-bootstrap
then `poetry add` each of those libraries

[] set environment variables
export OTEL_SERVICE_NAME="openhands-headless"
export OTEL_TRACES_EXPORTER="otlp"
export OTEL_LOGS_EXPORTER="otlp"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io:443" # US instance
#export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.eu1.honeycomb.io:443" # EU instance
export OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=<your-api-key>"
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

