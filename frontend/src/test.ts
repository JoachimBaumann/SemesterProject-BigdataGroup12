import { Kafka } from 'kafkajs';
import avro from 'avsc'

const kafka = new Kafka({
  clientId: 'example-consumer',
  brokers: ['redpanda-0.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-1.redpanda.redpanda.svc.cluster.local:9093', 'redpanda-2.redpanda.redpanda.svc.cluster.local:9093'],
})

const consumer = kafka.consumer({ groupId: 'test-group-6' });
const host = 'http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081'
const topic = 'taxi-average'

const response = await fetch(`${host}/subjects/${topic}-value/versions/latest/schema`);
const schema = await response.json()
// const type = avro.parse(schema)

console.log(schema)

const run = async () => {

  await consumer.connect();
  await consumer.subscribe({ topic });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {

      if (message.value === null)
        return undefined

      // const decodedValue = type.fromBuffer(message.value)
      console.log(message.value)
    },
  })
}

run().catch(async e => {
  console.error(e)
  consumer && await consumer.disconnect()
})