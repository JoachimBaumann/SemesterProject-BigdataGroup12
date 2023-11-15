import { Elysia } from "elysia";
import { html } from "@elysiajs/html";
import { BaseHtml } from "./components/base";
import Stream from "@elysiajs/stream";
import { Kafka } from 'kafkajs';
import { scaleQuantize } from 'd3-scale';
import { schemeBlues } from 'd3-scale-chromatic';
import { GeoPermissibleObjects, geoPath, geoAlbers } from 'd3-geo';
import * as topojson from 'topojson-client';
import ny from './data/ny.json';

const counties = topojson.feature(ny, ny.objects.collection);
const width = 1000, height = 1000;
const albersProjection = geoAlbers()
    .rotate([74, 0])
    .center([0, 41.7128])
    .parallels([29.5, 45.5])
    .translate([width / 5, height / 1.5])
    .scale(10000);
const path = geoPath(albersProjection);
const colorScale = scaleQuantize([1, 10], schemeBlues[9]);
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['redpanda-0.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-1.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-2.redpanda.redpanda.svc.cluster.local:9093'],
})
const consumer = kafka.consumer({ groupId: 'test-group' });

await consumer.connect();
await consumer.subscribe({ topic: 'taxi-average' });

interface TripStatistics {
  AVG_DISTANCE: number;
  TOTAL_TRIPS: number;
  AVG_TIP: number;
}

const app = new Elysia()
  .use(html())
  .get('/stats_stream', async () => {
    const stream = new Stream();
    await consumer.run({
      eachMessage: async ({ message }) => {
        if (message.value) {
          try {
            const { AVG_DISTANCE, AVG_TIP, TOTAL_TRIPS }: TripStatistics = JSON.parse(message.value.toString());
            stream.event = "distance-traveled";
            stream.send(<>{AVG_DISTANCE.toFixed(2)} km</>);
            stream.event = "trips-completed-value";
            stream.send(<>{TOTAL_TRIPS.toFixed(0)}</>);
            stream.event = "average-tip-value";
            stream.send(<>{AVG_TIP.toFixed(2)} $</>);
          } catch (e) {
            console.error("Error parsing JSON:", e);
          }
        }
      },
    });
    return stream;
  })
  .get("/stream_map", () => {
    const stream = new Stream();
    const interval = setInterval(() => { 
      const svg = 
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} style={{ maxWidth: "100%", height: "auto", backgroundColor: "transparent" }}>
          <g class="data">
          {counties.features.map((county: GeoPermissibleObjects) => {
              const color_value = getRandomIntInclusive(1, 10)
              let color = colorScale(color_value)
              const geoId: string = county.properties.geo_id
              if (geoId == "BK93") {
                color = "none"
              }
              return (
              <g>
                <path id={geoId} fill={color} d={path(county)} />
              </g>)
            })}
          </g>
        </svg>;
      stream.send(svg);
    }, 3333);

    setTimeout(() => {
      clearInterval(interval);
      stream.close();
    }, 30000);

    return stream;
  })
  .get("/", () => 
    <BaseHtml>
      <div class="flex flex-col mt-4 justify-center content-center">

        <div hx-ext="sse" sse-connect="/stats_stream" class="stats shadow-lg" >
          <div class="stat">
            <div class="stat-figure text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2" /><circle cx="7" cy="17" r="2" /><path d="M9 17h6" /><circle cx="17" cy="17" r="2" /></g></svg>
            </div>
            <div class="stat-title">Distance traveled</div>
            <div sse-swap="distance-traveled" class="stat-value countdown">
              <span class="loading loading-bars loading-md"></span>
            </div>
            <div class="stat-desc">Last 60 minutes</div>
          </div>

          <div class="stat">
            <div class="stat-figure text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="m9 11l3 3L22 4" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" /></g></svg>
            </div>
            <div class="stat-title">Trips completed</div>
            <div sse-swap="trips-completed-value" class="stat-value">
              <div class="loading loading-bars loading-md"></div>
            </div>
            <div class="stat-desc">Last 60 minutes</div>
          </div>

          <div class="stat">
            <div class="stat-figure text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m3 15l5.12-5.12A3 3 0 0 1 10.24 9H13a2 2 0 1 1 0 4h-2.5m4-.68l4.17-4.89a1.88 1.88 0 0 1 2.92 2.36l-4.2 5.94A3 3 0 0 1 14.96 17H9.83a2 2 0 0 0-1.42.59L7 19m-5-5l6 6" /></svg>   </div>
            <div class="stat-title">Average tip</div>
            <div sse-swap="average-tip-value" class="stat-value">
              <div class="loading loading-bars loading-md"></div>
            </div>
            <div class="stat-desc">Last 60 minutes</div>
          </div>
        </div>

        
        <div class="flex flex-row justify-center content-center items-center" hx-ext="sse" sse-connect="/stream_map" sse-swap="message">
          <div class="loading loading-ring mt-48 w-1/3"></div>
        </div>
      </div>
      
    </BaseHtml>
    
  )
  .listen(3001);

console.log(`🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`);

function getRandomIntInclusive(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1) + min);
}
