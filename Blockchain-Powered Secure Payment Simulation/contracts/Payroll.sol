pragma solidity ^0.8.0;

contract Migrations {
    // Saves the address of the person who deployed the contract
    address public owner;
    // Keeps track of the last migration step that was completed
    uint public last_completed_migration;

    // This runs once when the contract is deployed, it sets the owner to the person who deployed the contract
    constructor() {
        owner = msg.sender;
    }

    // This is used to allow only the owner to run certain functions
    modifier restricted() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    // Lets the owner update the last completed migration step (Only the owner can call this function)
    function setCompleted(uint completed) public restricted {
        last_completed_migration = completed;
    }
}

