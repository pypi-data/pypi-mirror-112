import { __makeTemplateObject, __rest } from "tslib";
import { Fragment } from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { Token } from './parser';
function renderToken(token) {
    switch (token.type) {
        case Token.Spaces:
            return token.value;
        case Token.Filter:
            return <FilterToken filter={token}/>;
        case Token.ValueTextList:
        case Token.ValueNumberList:
            return <ListToken token={token}/>;
        case Token.ValueNumber:
            return <NumberToken token={token}/>;
        case Token.ValueBoolean:
            return <Boolean>{token.text}</Boolean>;
        case Token.ValueIso8601Date:
            return <DateTime>{token.text}</DateTime>;
        case Token.LogicGroup:
            return <LogicGroup>{renderResult(token.inner)}</LogicGroup>;
        case Token.LogicBoolean:
            return <LogicBoolean>{token.value}</LogicBoolean>;
        default:
            return token.text;
    }
}
function renderResult(result) {
    return result
        .map(renderToken)
        .map(function (renderedToken, i) { return <Fragment key={i}>{renderedToken}</Fragment>; });
}
/**
 * Renders the parsed query with syntax highlighting.
 */
export default function HighlightQuery(_a) {
    var parsedQuery = _a.parsedQuery;
    var rendered = renderResult(parsedQuery);
    return <Fragment>{rendered}</Fragment>;
}
var FilterToken = function (_a) {
    var filter = _a.filter;
    return (<Filter>
    {filter.negated && <Negation>!</Negation>}
    <KeyToken token={filter.key} negated={filter.negated}/>
    {filter.operator && <Operator>{filter.operator}</Operator>}
    <Value>{renderToken(filter.value)}</Value>
  </Filter>);
};
var KeyToken = function (_a) {
    var token = _a.token, negated = _a.negated;
    var value = token.text;
    if (token.type === Token.KeyExplicitTag) {
        value = (<ExplicitKey prefix={token.prefix}>
        {token.key.quoted ? "\"" + token.key.value + "\"" : token.key.value}
      </ExplicitKey>);
    }
    return <Key negated={!!negated}>{value}:</Key>;
};
var ListToken = function (_a) {
    var token = _a.token;
    return (<InList>
    {token.items.map(function (_a) {
            var value = _a.value, separator = _a.separator;
            return [
                <ListComma key="comma">{separator}</ListComma>,
                renderToken(value),
            ];
        })}
  </InList>);
};
var NumberToken = function (_a) {
    var token = _a.token;
    return (<Fragment>
    {token.value}
    <Unit>{token.unit}</Unit>
  </Fragment>);
};
var Filter = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  --token-bg: ", ";\n  --token-border: ", ";\n  --token-value-color: ", ";\n"], ["\n  --token-bg: ", ";\n  --token-border: ", ";\n  --token-value-color: ", ";\n"])), function (p) { return p.theme.searchTokenBackground; }, function (p) { return p.theme.searchTokenBorder; }, function (p) { return p.theme.blue300; });
var filterCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: var(--token-bg);\n  border: 0.5px solid var(--token-border);\n  padding: ", " 0;\n"], ["\n  background: var(--token-bg);\n  border: 0.5px solid var(--token-border);\n  padding: ", " 0;\n"])), space(0.25));
var Negation = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"], ["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"])), filterCss, function (p) { return p.theme.red300; });
var Key = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ", ";\n"], ["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ", ";\n"])), filterCss, function (p) {
    return !p.negated
        ? css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "], ["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "]))) : css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n          border-left: none;\n          margin-left: 0;\n        "], ["\n          border-left: none;\n          margin-left: 0;\n        "])));
});
var ExplicitKey = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"], ["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.prefix; });
var Operator = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"], ["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"])), filterCss, function (p) { return p.theme.orange400; });
var Value = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: var(--token-value-color);\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"], ["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: var(--token-value-color);\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"])), filterCss);
var Unit = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var LogicBoolean = styled('span')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
var Boolean = styled('span')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.pink300; });
var DateTime = styled('span')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var ListComma = styled('span')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var InList = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"], ["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, Value, function (p) { return p.theme.purple300; });
var LogicGroup = styled(function (_a) {
    var children = _a.children, props = __rest(_a, ["children"]);
    return (<span {...props}>
    <span>(</span>
    {children}
    <span>)</span>
  </span>);
})(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  > span:first-child,\n  > span:last-child {\n    position: relative;\n    color: transparent;\n\n    &:before {\n      position: absolute;\n      top: -5px;\n      color: ", ";\n      font-size: 16px;\n      font-weight: bold;\n    }\n  }\n\n  > span:first-child:before {\n    left: -3px;\n    content: '(';\n  }\n  > span:last-child:before {\n    right: -3px;\n    content: ')';\n  }\n"], ["\n  > span:first-child,\n  > span:last-child {\n    position: relative;\n    color: transparent;\n\n    &:before {\n      position: absolute;\n      top: -5px;\n      color: ", ";\n      font-size: 16px;\n      font-weight: bold;\n    }\n  }\n\n  > span:first-child:before {\n    left: -3px;\n    content: '(';\n  }\n  > span:last-child:before {\n    right: -3px;\n    content: ')';\n  }\n"])), function (p) { return p.theme.orange400; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=renderer.jsx.map