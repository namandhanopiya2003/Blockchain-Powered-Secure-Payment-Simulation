// Loads the compiled Payroll smart contract
const Payroll = artifacts.require("Payroll");

// This function runs when the contract is being deployed
module.exports = function (deployer) {
  // Deploys the Payroll contract to the blockchain
  deployer.deploy(Payroll);
};

