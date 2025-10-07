// This line loads the compiled "Migrations" smart contract
const Migrations = artifacts.require("Migrations");

// This is the main function that runs when it deploy the contracts
module.exports = function (deployer) {
  // This line tells to deploy the Migrations contract to the blockchain
  deployer.deploy(Migrations);
};

