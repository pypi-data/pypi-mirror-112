import { __assign } from "tslib";
/* global __dirname */
/* eslint import/no-nodejs-modules:0 */
import fs from 'fs';
import path from 'path';
var FIXTURES_ROOT = path.join(__dirname, '../../fixtures');
/**
 * Loads a directory of fixtures. Supports js and json fixtures.
 */
export function loadFixtures(dir, opts) {
    if (opts === void 0) { opts = {}; }
    var from = path.join(FIXTURES_ROOT, dir);
    var files = fs.readdirSync(from);
    var fixturesPairs = files.map(function (file) {
        var filePath = path.join(from, file);
        if (/[jt]sx?$/.test(file)) {
            var module_1 = require(filePath);
            if (Object.keys(module_1).includes('default')) {
                throw new Error('Javascript fixtures cannot use default export');
            }
            return [file, module_1];
        }
        if (/json$/.test(file)) {
            return [file, JSON.parse(fs.readFileSync(filePath).toString())];
        }
        throw new Error("Invalid fixture type found: " + file);
    });
    var fixtures = Object.fromEntries(fixturesPairs);
    if (opts.flatten) {
        return Object.values(fixtures).reduce(function (acc, val) { return (__assign(__assign({}, acc), val)); }, {});
    }
    return fixtures;
}
//# sourceMappingURL=loadFixtures.js.map