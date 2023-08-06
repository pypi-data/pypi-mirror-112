import { __assign, __read } from "tslib";
import { loadFixtures } from 'sentry-test/loadFixtures';
import { parseSearch, Token, } from 'app/components/searchSyntax/parser';
import { treeTransformer } from 'app/components/searchSyntax/utils';
/**
 * Normalize results to match the json test cases
 */
var normalizeResult = function (tokens) {
    return treeTransformer(tokens, function (token) {
        // XXX: This attempts to keep the test data simple, only including keys
        // that are really needed to validate functionality.
        // @ts-ignore
        delete token.location;
        // @ts-ignore
        delete token.text;
        // @ts-ignore
        delete token.config;
        if (token.type === Token.Filter && token.invalid === null) {
            // @ts-ignore
            delete token.invalid;
        }
        if (token.type === Token.ValueIso8601Date) {
            // Date values are represented as ISO strings in the test case json
            return __assign(__assign({}, token), { value: token.value.toISOString() });
        }
        return token;
    });
};
describe('searchSyntax/parser', function () {
    var testData = loadFixtures('search-syntax');
    var registerTestCase = function (testCase) {
        return it("handles " + testCase.query, function () {
            var result = parseSearch(testCase.query);
            // Handle errors
            if (testCase.raisesError) {
                expect(result).toBeNull();
                return;
            }
            if (result === null) {
                throw new Error('Parsed result as null without raiseError true');
            }
            expect(normalizeResult(result)).toEqual(testCase.result);
        });
    };
    Object.entries(testData).map(function (_a) {
        var _b = __read(_a, 2), name = _b[0], cases = _b[1];
        return describe("" + name, function () {
            cases.map(registerTestCase);
        });
    });
});
//# sourceMappingURL=parser.spec.jsx.map