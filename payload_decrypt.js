#!/usr/bin/env node

"use strict";
//var lora_packet = require('../lib/index.js');
var cmdlineArgs = process.argv;
var lora_packet = require('lora-packet');

var nwkskeyIndex = cmdlineArgs.indexOf("--nwkskey");
var appskeyIndex = cmdlineArgs.indexOf("--appskey");
var payloadIndex = cmdlineArgs.indexOf("--payload");
// decode a packet
var nwkskeyStr = cmdlineArgs[nwkskeyIndex+1]
var appskeyStr = cmdlineArgs[appskeyIndex+1]
var payloadStr = cmdlineArgs[payloadIndex+1]

var nwksKeyStr = 'f5305e78929e59dc1329b52a5fbcad6c'
var appskeyStr = '57a1e0fb95e104aee164577a9e8d3d2b'

var packet = lora_packet.fromWire(new Buffer(payloadStr, 'base64'));
var NwkSKey = new Buffer(nwkskeyStr, 'hex');
var AppSKey = new Buffer(appskeyStr, 'hex');
var value = lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex');
console.log(value)
