import { Elysia } from "elysia";
import { html } from "@elysiajs/html";
import { BaseHtml } from "./components/base";
import Stream from "@elysiajs/stream";


/**
 * Generates a random integer between two inclusive bounds.
 * @param {number} min - The inclusive lower bound of the range.
 * @param {number} max - The inclusive upper bound of the range.
 * @returns {number} A random integer between the inclusive bounds.
 */
function getRandomIntInclusive(min: number, max: number) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1) + min);
}

const app = new Elysia()
  .use(html())
  .get('/stats_stream', () => {
    const stream = new Stream()

    const interval_1 = setInterval(() => {
      const i = getRandomIntInclusive(1, 100)
      stream.event = "distance-traveled"
      stream.send(<>{i} km</>)
    }, 3000)

    const interval_2 = setInterval(() => {
      const count = getRandomIntInclusive(1000, 7000)
      stream.event = "trips-completed-value"
      stream.send(<>{count}</>)

      const percent = getRandomIntInclusive(1, 40)
      const change = count * (percent / 100)
      stream.event = "trips-completed-desc"
      stream.send(<>↗︎ {change.toFixed(0)} ({percent.toFixed(0)}%)</>)

    }, 1200)

    const interval_3 = setInterval(() => {
      const average = getRandomIntInclusive(1, 600) / 100
      stream.event = "average-tip-value"
      stream.send(<>{average.toFixed(2)} $</>)

      const percent = getRandomIntInclusive(1, 40)
      const change = average * (percent / 100)
      stream.event = "average-tip-desc"
      stream.send(<>↗︎ {change.toFixed(2)}$ ({percent.toFixed(0)}%)</>)
    }, 2050)

    setTimeout(() => {
      clearInterval(interval_1)
      clearInterval(interval_2)
      clearInterval(interval_3)
      stream.close()
    }, 30_000)

    return stream
  })
  .get("/", () => {
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
              <div sse-swap="trips-completed-desc" class="stat-desc"></div>
            </div>

            <div class="stat">
              <div class="stat-figure text-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m3 15l5.12-5.12A3 3 0 0 1 10.24 9H13a2 2 0 1 1 0 4h-2.5m4-.68l4.17-4.89a1.88 1.88 0 0 1 2.92 2.36l-4.2 5.94A3 3 0 0 1 14.96 17H9.83a2 2 0 0 0-1.42.59L7 19m-5-5l6 6" /></svg>   </div>
              <div class="stat-title">Average tip</div>
              <div sse-swap="average-tip-value" class="stat-value">
                <div class="loading loading-bars loading-md"></div>
              </div>
              <div sse-swap="average-tip-desc" class="stat-desc"></div>
            </div>
          </div>

        </div>
      </BaseHtml>
    )
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);


