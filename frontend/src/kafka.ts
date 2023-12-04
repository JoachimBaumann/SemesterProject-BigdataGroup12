import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'example-consumer',
  brokers: ['redpanda-0.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-1.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-2.redpanda.redpanda.svc.cluster.local:9093'],
})

const consumer = kafka.consumer({ groupId: 'test-group-8' });
const topics = {
  taxi_pu_location: 'taxi-pu-location',
  taxi_average: 'taxi-average'
}

interface TripStatistics {
  AVG_DISTANCE: number;
  TOTAL_TRIPS: number;
  AVG_TIP: number;

}

class TaxiPuLocation {
  map = new Map<string, TripStatistics>();
  ingest({ key, value }: { key: Buffer, value: Buffer }) {
    try {

      const k = extractFirstQuotedString(key.toString());
      const v = JSON.parse(value.toString()) as TripStatistics;

      if (k && k != 'NaN') {
        this.map.set(k, v);
      }

    } catch (parseErr) {
      console.error('Error parsing JSON:', parseErr);
    }
  }
  get_min() {

    const array = [...this.map.values()];
    const min = array.reduce((sum, value) =>
      sum = Math.min(sum, value.TOTAL_TRIPS) 
      , Infinity);

    return min;
  }

  get_max() {

    const array = [...this.map.values()];
    const max = array.reduce((sum, value) =>
    sum = Math.max(sum, value.TOTAL_TRIPS) 
    , 0);

    return max;

  }
}

class TaxiAverage {
  current: TripStatistics | undefined = undefined
  ingest({ value }: { value: Buffer }) {
    try {
      const v = JSON.parse(value.toString()) as TripStatistics;
      this.current = v
    } catch (parseErr) {
      console.error('Error parsing JSON:', parseErr);
    }
  }
}

export const taxiPuLocation = new TaxiPuLocation()
export const taxiAverage = new TaxiAverage()


const run = async () => {
  // Assume consumer, topic, extractFirstQuotedString are defined and available

  await consumer.connect();
  await consumer.subscribe({ topics: [topics.taxi_average, topics.taxi_pu_location] });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      if (message.value === null || message.key === null)
        return undefined;

      switch (topic) {
        case topics.taxi_average:
          taxiAverage.ingest({ value: message.value })
          break;

        case topics.taxi_pu_location:
          taxiPuLocation.ingest({ key: message.key, value: message.value })
          break;

        default:
          break;
      }

    },
  });
};
run().catch(async e => {
  console.error(e)
  consumer && await consumer.disconnect()
})


// Handle Ctrl+C event
process.on('SIGINT', () => {
  console.log('\nCtrl+C pressed. Here is the dictionary:');
  console.log(taxiPuLocation.map);
  process.exit(0); // Exit the process to stop the Node.js application
});

function extractFirstQuotedString(input: string): string | null {
  // Regular expression to find the first quoted string
  const regex = /"(.*?)"/;

  // Apply the regex to the input string
  const match = input.match(regex);

  // If a match is found, return the first captured group, otherwise return null
  return match ? match[1] : null;
}
