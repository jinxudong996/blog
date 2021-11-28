#!/usr/bin/env node
const Compiler = require("./compiler");
const options = require("../wpk.config");
new Compiler(options).run();