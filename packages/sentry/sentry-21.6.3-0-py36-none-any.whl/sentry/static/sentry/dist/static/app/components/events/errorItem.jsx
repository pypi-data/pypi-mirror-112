import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import startCase from 'lodash/startCase';
import moment from 'moment';
import Button from 'app/components/button';
import KeyValueList from 'app/components/events/interfaces/keyValueList';
import { getMeta } from 'app/components/events/meta/metaProxy';
import ListItem from 'app/components/list/listItem';
import { JavascriptProcessingErrors } from 'app/constants/eventErrors';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import ExternalLink from '../links/externalLink';
var keyMapping = {
    image_uuid: 'Debug ID',
    image_name: 'File Name',
    image_path: 'File Path',
};
var ErrorItem = /** @class */ (function (_super) {
    __extends(ErrorItem, _super);
    function ErrorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.handleToggle = function () {
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        return _this;
    }
    ErrorItem.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.isOpen !== nextState.isOpen;
    };
    ErrorItem.prototype.cleanedData = function (errorData) {
        var data = __assign({}, errorData);
        // The name is rendered as path in front of the message
        if (typeof data.name === 'string') {
            delete data.name;
        }
        if (data.message === 'None') {
            // Python ensures a message string, but "None" doesn't make sense here
            delete data.message;
        }
        if (typeof data.image_path === 'string') {
            // Separate the image name for readability
            var separator = /^([a-z]:\\|\\\\)/i.test(data.image_path) ? '\\' : '/';
            var path = data.image_path.split(separator);
            data.image_name = path.splice(-1, 1)[0];
            data.image_path = path.length ? path.join(separator) + separator : '';
        }
        if (typeof data.server_time === 'string' && typeof data.sdk_time === 'string') {
            data.message = t('Adjusted timestamps by %s', moment
                .duration(moment.utc(data.server_time).diff(moment.utc(data.sdk_time)))
                .humanize());
        }
        return Object.entries(data).map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: keyMapping[key] || startCase(key),
                meta: getMeta(data, key),
            });
        });
    };
    ErrorItem.prototype.renderPath = function (data) {
        var name = data.name;
        if (!name || typeof name !== 'string') {
            return null;
        }
        return (<React.Fragment>
        <strong>{name}</strong>
        {': '}
      </React.Fragment>);
    };
    ErrorItem.prototype.renderTroubleshootingLink = function (error) {
        if (Object.values(JavascriptProcessingErrors).includes(error.type)) {
            return (<React.Fragment>
          {' '}
          (
          {tct('see [docsLink]', {
                    docsLink: (<StyledExternalLink href="https://docs.sentry.io/platforms/javascript/sourcemaps/troubleshooting_js/">
                {t('Troubleshooting for JavaScript')}
              </StyledExternalLink>),
                })}
          )
        </React.Fragment>);
        }
        return null;
    };
    ErrorItem.prototype.render = function () {
        var _a;
        var error = this.props.error;
        var isOpen = this.state.isOpen;
        var data = (_a = error === null || error === void 0 ? void 0 : error.data) !== null && _a !== void 0 ? _a : {};
        var cleanedData = this.cleanedData(data);
        return (<StyledListItem>
        <OverallInfo>
          <div>
            {this.renderPath(data)}
            {error.message}
            {this.renderTroubleshootingLink(error)}
          </div>
          {!!cleanedData.length && (<ToggleButton onClick={this.handleToggle} priority="link">
              {isOpen ? t('Collapse') : t('Expand')}
            </ToggleButton>)}
        </OverallInfo>
        {isOpen && <KeyValueList data={cleanedData} isContextData/>}
      </StyledListItem>);
    };
    return ErrorItem;
}(React.Component));
export default ErrorItem;
var ToggleButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"], ["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"])), space(1.5), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
var StyledListItem = styled(ListItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(0.75));
var StyledExternalLink = styled(ExternalLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* && is here to increase specificity to override default styles*/\n  && {\n    font-weight: inherit;\n    color: inherit;\n    text-decoration: underline;\n  }\n"], ["\n  /* && is here to increase specificity to override default styles*/\n  && {\n    font-weight: inherit;\n    color: inherit;\n    text-decoration: underline;\n  }\n"])));
var OverallInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=errorItem.jsx.map