module.exports = {
  networks: {
    development: {
      // Localhost IP address (own device)
      host: "127.0.0.1",
      // This is the port Ethereum app will use
      port: 8545,
      // It connects to network ID
      network_id: "*",
    },
  },
  compilers: {
    solc: {
      // Version of the Solidity language used to compile contracts
      version: "0.8.17",
    },
  },
};

