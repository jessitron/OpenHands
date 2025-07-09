import { HoneycombWebSDK } from "@honeycombio/opentelemetry-web";
import { getWebAutoInstrumentations } from "@opentelemetry/auto-instrumentations-web";

const defaults = {
  ignoreNetworkEvents: true,
  propagateTraceHeaderCorsUrls: [/.*/g],
};

export default function installOpenTelemetry() {
  try {
    // this SDK installs OpenTelemetry-JS for a web browser, and
    // adds automatic instrumentation for Core Web Vitals and other
    // features.
    const sdk = new HoneycombWebSDK({
      apiKey:
        "hcaik_01jzrfabr5kafh7dyj2tvf5v5tyryategbprk1k8ecqdn94pq408cagfc6",
      serviceName: "react-frontend",
      instrumentations: [
        getWebAutoInstrumentations({
          "@opentelemetry/instrumentation-xml-http-request": defaults,
          "@opentelemetry/instrumentation-fetch": defaults,
          "@opentelemetry/instrumentation-document-load": defaults,
        }),
      ],
    });

    // start up the SDK, wiring up OpenTelemetry for JS
    sdk.start();
  } catch (e) {
    console.log(`An error occurred wiring up Honeycomb...`);
    console.error(e);
  }
}
