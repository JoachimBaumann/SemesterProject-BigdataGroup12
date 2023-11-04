// src/routes/events/+server.js
import { events } from 'sveltekit-sse'

/**
 * @param {number} milliseconds
 * @returns
 */
const delay = milliseconds => new Promise(r => setTimeout(r, milliseconds))


/**
 * Generates a random integer between two inclusive bounds.
 * @param {number} min - The inclusive lower bound of the range.
 * @param {number} max - The inclusive upper bound of the range.
 * @returns {number} A random integer between the inclusive bounds.
 */
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1) + min);
}

export function GET() {
  return events(async emit => {
    while (true) {

      {
        const i = getRandomIntInclusive(1, 100)
        emit('distance-traveled',`${i.toFixed(0)} km`)
      }

      {
        const count = getRandomIntInclusive(1000, 7000)
        emit('trips-completed-value', count.toFixed(0))

        const percent = getRandomIntInclusive(1, 40)
        const change = count * (percent / 100)
        emit('trips-completed-desc', `↗︎ ${change.toFixed(0)} (${percent.toFixed(0)}%)`)
      }

      {
        const average = getRandomIntInclusive(1, 600) / 100
        emit('average-tip-value', `${average.toFixed(2)} $`)

        const percent = getRandomIntInclusive(1, 40)
        const change = average * (percent / 100)
        emit('average-tip-desc', `↗︎ ${change.toFixed(2)}$ (${percent.toFixed(0)}%)`)
      }

      await delay(1200)
    }
  }).toResponse()
}