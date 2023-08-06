import { __assign } from "tslib";
import { Token } from './parser';
/**
 * Utility function to visit every Token node within an AST tree and apply
 * a transform to those nodes.
 */
export function treeTransformer(tree, transform) {
    var nodeVisitor = function (token) {
        switch (token.type) {
            case Token.Filter:
                return transform(__assign(__assign({}, token), { key: nodeVisitor(token.key), value: nodeVisitor(token.value) }));
            case Token.KeyExplicitTag:
                return transform(__assign(__assign({}, token), { key: nodeVisitor(token.key) }));
            case Token.KeyAggregate:
                return transform(__assign(__assign({}, token), { name: nodeVisitor(token.name), args: token.args ? nodeVisitor(token.args) : token.args, argsSpaceBefore: nodeVisitor(token.argsSpaceBefore), argsSpaceAfter: nodeVisitor(token.argsSpaceAfter) }));
            case Token.LogicGroup:
                return transform(__assign(__assign({}, token), { inner: token.inner.map(nodeVisitor) }));
            case Token.KeyAggregateArgs:
                return transform(__assign(__assign({}, token), { args: token.args.map(function (v) { return (__assign(__assign({}, v), { value: nodeVisitor(v.value) })); }) }));
            case Token.ValueNumberList:
            case Token.ValueTextList:
                return transform(__assign(__assign({}, token), { 
                    // TODO(ts): Not sure why `v` cannot be inferred here
                    items: token.items.map(function (v) { return (__assign(__assign({}, v), { value: nodeVisitor(v.value) })); }) }));
            default:
                return transform(token);
        }
    };
    return tree.map(nodeVisitor);
}
/**
 * Utility to get the string name of any type of key.
 */
export var getKeyName = function (key, options) {
    if (options === void 0) { options = {}; }
    var aggregateWithArgs = options.aggregateWithArgs;
    switch (key.type) {
        case Token.KeySimple:
            return key.value;
        case Token.KeyExplicitTag:
            return key.key.value;
        case Token.KeyAggregate:
            return aggregateWithArgs
                ? key.name.value + "(" + (key.args ? key.args.text : '') + ")"
                : key.name.value;
        default:
            return '';
    }
};
export function isWithinToken(node, position) {
    return position >= node.location.start.offset && position <= node.location.end.offset;
}
//# sourceMappingURL=utils.jsx.map