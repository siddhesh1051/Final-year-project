const { createClient } = require("redis");

let redisClient;

const connect = async () => {
  try {
    // redisClient = createClient("redis://redis:6379"); // Default port 6379
    redisClient = createClient({ url: 'redis://localhost:6379', legacyMode: true });
    await redisClient.connect();
    console.log("Redis connected!!");
  } catch (err) {
    console.log(err);
    // throw new Error(err)
  }
};

const flushAllData = async () => {
  try {
    // Ensure the client is connected before flushing
    if (redisClient && redisClient.status === 'ready') {
      await redisClient.flushAll("ASYNC");
      console.log("Redis data flushed!!");
    } else {
      console.log("Redis client is not ready yet.");
    }
  } catch (err) {
    console.log(err);
  }
};

// Connect to Redis
connect()
  .then(() => {
    // After connecting, flush all data
    flushAllData();
  })
  .catch((err) => {
    console.error("Error connecting to Redis:", err);
  });

module.exports = { redisClient };



// const redis = require("redis");
// const redisClient = redis.createClient({
//   host: "redis", // Use the Docker service name as the hostname
//   port: 6379,    // Default Redis port
// });

// redisClient.on("error", (err) => {
//   console.error("Redis Error:", err);
// });

// redisClient.on("connect", () => {
//   console.log("Connected to Redis");
// });

// module.exports = redisClient;



//old code
// const { createClient } = require("redis");

// let redisClient;

// const connect = async () => {
//   try {
//     // redisClient = createClient("redis://redis:6379"); //Default port 6379
//     redisClient = createClient({ url: 'redis://redis:6379',   legacyMode: true })//for docker
//     await redisClient.connect();
//     await redisClient.flushAll("ASYNC");
//     console.log("Redis connected!!");
//   } catch (err) {
//     console.log(err);
//     // throw new Error(err)
//   }
// };

// connect();

// module.exports = {redisClient };
