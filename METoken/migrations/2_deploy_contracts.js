var METoken = artifacts.require("METoken");
var METFaucet = artifacts.require("METFaucet");

module.exports = function(deployer, network, accounts) {

	var owner = accounts[0];
	// Deploy the METoken contract first
	deployer.deploy(METoken, {from: owner}).then(function() {
		// Then deploy METFaucet and pass the address of METoken and the
		// address of the owner of all the MET who will approve METFaucet
		return deployer.deploy(METFaucet, METoken.address, owner);
  	});
}