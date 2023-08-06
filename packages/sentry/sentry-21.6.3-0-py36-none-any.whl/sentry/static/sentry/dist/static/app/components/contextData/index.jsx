import { __extends, __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import isArray from 'lodash/isArray';
import isNumber from 'lodash/isNumber';
import isString from 'lodash/isString';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import ExternalLink from 'app/components/links/externalLink';
import { IconOpen } from 'app/icons';
import { isUrl } from 'app/utils';
import Toggle from './toggle';
import { analyzeStringForRepr, naturalCaseInsensitiveSort } from './utils';
var ContextData = /** @class */ (function (_super) {
    __extends(ContextData, _super);
    function ContextData() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ContextData.prototype.renderValue = function (value) {
        var _a = this.props, preserveQuotes = _a.preserveQuotes, meta = _a.meta, withAnnotatedText = _a.withAnnotatedText, jsonConsts = _a.jsonConsts, maxDefaultDepth = _a.maxDefaultDepth;
        var maxDepth = maxDefaultDepth !== null && maxDefaultDepth !== void 0 ? maxDefaultDepth : 2;
        function getValueWithAnnotatedText(v, meta) {
            return <AnnotatedText value={v} meta={meta}/>;
        }
        /* eslint no-shadow:0 */
        function walk(value, depth) {
            var i = 0;
            var children = [];
            if (value === null) {
                return <span className="val-null">{jsonConsts ? 'null' : 'None'}</span>;
            }
            if (value === true || value === false) {
                return (<span className="val-bool">
            {jsonConsts ? (value ? 'true' : 'false') : value ? 'True' : 'False'}
          </span>);
            }
            if (isString(value)) {
                var valueInfo = analyzeStringForRepr(value);
                var valueToBeReturned = withAnnotatedText
                    ? getValueWithAnnotatedText(valueInfo.repr, meta)
                    : valueInfo.repr;
                var out = [
                    <span key="value" className={(valueInfo.isString ? 'val-string' : '') +
                            (valueInfo.isStripped ? ' val-stripped' : '') +
                            (valueInfo.isMultiLine ? ' val-string-multiline' : '')}>
            {preserveQuotes ? "\"" + valueToBeReturned + "\"" : valueToBeReturned}
          </span>,
                ];
                if (valueInfo.isString && isUrl(value)) {
                    out.push(<ExternalLink key="external" href={value} className="external-icon">
              <StyledIconOpen size="xs"/>
            </ExternalLink>);
                }
                return out;
            }
            if (isNumber(value)) {
                var valueToBeReturned = withAnnotatedText && meta ? getValueWithAnnotatedText(value, meta) : value;
                return <span>{valueToBeReturned}</span>;
            }
            if (isArray(value)) {
                for (i = 0; i < value.length; i++) {
                    children.push(<span className="val-array-item" key={i}>
              {walk(value[i], depth + 1)}
              {i < value.length - 1 ? (<span className="val-array-sep">{', '}</span>) : null}
            </span>);
                }
                return (<span className="val-array">
            <span className="val-array-marker">{'['}</span>
            <Toggle highUp={depth <= maxDepth} wrapClassName="val-array-items">
              {children}
            </Toggle>
            <span className="val-array-marker">{']'}</span>
          </span>);
            }
            if (React.isValidElement(value)) {
                return value;
            }
            var keys = Object.keys(value);
            keys.sort(naturalCaseInsensitiveSort);
            for (i = 0; i < keys.length; i++) {
                var key = keys[i];
                children.push(<span className="val-dict-pair" key={key}>
            <span className="val-dict-key">
              <span className="val-string">{preserveQuotes ? "\"" + key + "\"" : key}</span>
            </span>
            <span className="val-dict-col">{': '}</span>
            <span className="val-dict-value">
              {walk(value[key], depth + 1)}
              {i < keys.length - 1 ? <span className="val-dict-sep">{', '}</span> : null}
            </span>
          </span>);
            }
            return (<span className="val-dict">
          <span className="val-dict-marker">{'{'}</span>
          <Toggle highUp={depth <= maxDepth - 1} wrapClassName="val-dict-items">
            {children}
          </Toggle>
          <span className="val-dict-marker">{'}'}</span>
        </span>);
        }
        return walk(value, 0);
    };
    ContextData.prototype.render = function () {
        var _a = this.props, data = _a.data, _preserveQuotes = _a.preserveQuotes, _withAnnotatedText = _a.withAnnotatedText, _meta = _a.meta, children = _a.children, other = __rest(_a, ["data", "preserveQuotes", "withAnnotatedText", "meta", "children"]);
        return (<pre {...other}>
        {this.renderValue(data)}
        {children}
      </pre>);
    };
    ContextData.defaultProps = {
        data: null,
        withAnnotatedText: false,
    };
    return ContextData;
}(React.Component));
var StyledIconOpen = styled(IconOpen)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
export default ContextData;
var templateObject_1;
//# sourceMappingURL=index.jsx.map