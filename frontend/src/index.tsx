import { Elysia, Static, t } from "elysia";
import { html } from "@elysiajs/html";
import { BaseHtml } from "./components/base";
import Stream from "@elysiajs/stream";
import { ScaleQuantize, scaleQuantize } from 'd3-scale';
import { schemeBlues } from 'd3-scale-chromatic';
import { GeoPermissibleObjects, geoPath, geoAlbers } from 'd3-geo';
import * as topojson from 'topojson-client';
import ny from './data/ny.json';
import { TripStatistics, taxiAverage, taxiPuLocation } from "./kafka";

const counties = topojson.feature(ny, ny.objects.collection);
const width = 1000, height = 1000;
const albersProjection = geoAlbers()
  .rotate([74, 0])
  .center([0, 41.7128])
  .parallels([29.5, 45.5])
  .translate([width / 5, height / 1.5])
  .scale(10000);
const path = geoPath(albersProjection);

const map_type = t.Union([
  t.Literal('count'),
  t.Literal('tip'),
  t.Literal('distance')
])


type MapType = Static<typeof map_type>


function calculate_color_value(value: TripStatistics, min: TripStatistics, max: TripStatistics, type: MapType) {

  switch (type) {
    case 'count':
      return (Math.log10(value.TOTAL_TRIPS) - Math.log10(min.TOTAL_TRIPS)) / (Math.log10(max.TOTAL_TRIPS) - Math.log10(min.TOTAL_TRIPS)) * 10;

    case 'distance':
      return Math.log10(value.AVG_DISTANCE) / Math.log10(max.AVG_DISTANCE) * 10;

    case 'tip':
      return Math.log10(value.AVG_TIP) / Math.log10(max.AVG_TIP) * 10;
    default:
      return 0;
  }

}

function createChoroplethSvg(colorScale: ScaleQuantize<string, never>, type: MapType) {
  const min = taxiPuLocation.get_min();
  const max = taxiPuLocation.get_max();
  const svg =
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} style={{ maxWidth: "100%", height: "auto", backgroundColor: "transparent" }}>
      <g class="data">
        {counties.features.map((county: GeoPermissibleObjects) => {
          const geoId: string = county.properties.geo_id
          let trip_stats = taxiPuLocation.map.get(geoId)
          if (!trip_stats) {
            trip_stats = {
              AVG_DISTANCE: 0,
              AVG_TIP: 0,
              TOTAL_TRIPS: 0
            }
          }

          const color_value = calculate_color_value(trip_stats, min, max, type)
          let color = colorScale(Math.ceil(color_value))

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

  return svg

}

function createChoroplethTab(type: MapType) {

  const colorScale = scaleQuantize([1, 10], schemeBlues[9]);

  const mapTypes = ['count', 'tip', 'distance'] as const

  return (<>
    <div role="tablist" class="tabs tabs-boxed">
      {mapTypes.map((v) => <button hx-get={`/tab/${v}`} aria-selected="false" role="tab" hx-trigger={(v === type ) ? "every 5s" : ""} aria-controls="tab-content" class={(v === type) ? "tab tab-active" : "tab"}>{v}</button>)}
    </div>

    <div id="tab-content" role="tabpanel">
      {createChoroplethSvg(colorScale, type)}
    </div>
  </>)

}

const app = new Elysia()
  .use(html())
  .get('/stats_stream', async () => {
    const stream = new Stream();

    const { AVG_DISTANCE, TOTAL_TRIPS, AVG_TIP } = taxiAverage.current!

    const interval = setInterval(() => {
      stream.event = "distance-traveled";
      stream.send(<>{AVG_DISTANCE.toFixed(2)} km</>);
      stream.event = "trips-completed-value";
      stream.send(<>{TOTAL_TRIPS.toFixed(0)}</>);
      stream.event = "average-tip-value";
      stream.send(<>{AVG_TIP.toFixed(2)} $</>);
    }, 5000)

    setTimeout(() => {
      clearInterval(interval)
      stream.close()
    }, 30000)

    return stream;
  })
  .get("/tab/:type", ({ params }) => {

    return createChoroplethTab(params.type)
  }, {
    params: t.Object({
      type: map_type
    })
  })
  .get("/stream_map", () => {
    const stream = new Stream();
    const colorScale = scaleQuantize([1, 10], schemeBlues[9]);
    const interval = setInterval(() => {

      stream.send(createChoroplethSvg(colorScale, 'count'))
    }, 3333);

    setTimeout(() => {
      clearInterval(interval);
      stream.close();
    }, 30000);

    return stream;
  })
  .get("/", () => {

    const colorScale = scaleQuantize([1, 10], schemeBlues[9]);
    const loadingBar = <div class="loading loading-bars loading-md"></div>

    let avgDistance = loadingBar
    let avgTip = loadingBar
    let totalTrips = loadingBar

    if (taxiAverage.current) {
      avgDistance = <>{taxiAverage.current.AVG_DISTANCE.toFixed(2)} km</>
      totalTrips = <>{taxiAverage.current.TOTAL_TRIPS.toFixed(0)}</>
      avgTip = <>{taxiAverage.current.AVG_TIP.toFixed(2)} $</>
    }


    return (
      <BaseHtml>
        <div class="flex flex-col mt-4 justify-center content-center">

          <div hx-ext="sse" sse-connect="/stats_stream" class="stats shadow-lg" >
            <div class="stat">
              <div class="stat-figure text-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2" /><circle cx="7" cy="17" r="2" /><path d="M9 17h6" /><circle cx="17" cy="17" r="2" /></g></svg>
              </div>
              <div class="stat-title">Distance traveled</div>
              <div sse-swap="distance-traveled" class="stat-value countdown">
                {avgDistance}
              </div>
              <div class="stat-desc">Last 60 minutes</div>
            </div>

            <div class="stat">
              <div class="stat-figure text-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="m9 11l3 3L22 4" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" /></g></svg>
              </div>
              <div class="stat-title">Trips completed</div>
              <div sse-swap="trips-completed-value" class="stat-value">
                {totalTrips}
              </div>
              <div class="stat-desc">Last 60 minutes</div>
            </div>

            <div class="stat">
              <div class="stat-figure text-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m3 15l5.12-5.12A3 3 0 0 1 10.24 9H13a2 2 0 1 1 0 4h-2.5m4-.68l4.17-4.89a1.88 1.88 0 0 1 2.92 2.36l-4.2 5.94A3 3 0 0 1 14.96 17H9.83a2 2 0 0 0-1.42.59L7 19m-5-5l6 6" /></svg>   </div>
              <div class="stat-title">Average tip</div>
              <div sse-swap="average-tip-value" class="stat-value">
                {avgTip}
              </div>
              <div class="stat-desc">Last 60 minutes</div>
            </div>
          </div>


          <div id="tabs" hx-target="#tabs" hx-swap="innerHTML" class="shrink justify-center place-self-center">
            {createChoroplethTab('count')}

          </div>
        </div>

      </BaseHtml>
    )
  }

  )
  .listen(3000);

console.log(`🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`);