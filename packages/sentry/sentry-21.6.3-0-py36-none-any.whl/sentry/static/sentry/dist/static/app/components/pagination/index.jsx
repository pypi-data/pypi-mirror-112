import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconChevron } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
import parseLinkHeader from 'app/utils/parseLinkHeader';
var defaultProps = {
    size: 'small',
    onCursor: function (cursor, path, query, _direction) {
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: cursor }),
        });
    },
};
var Pagination = /** @class */ (function (_super) {
    __extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, className = _a.className, onCursor = _a.onCursor, pageLinks = _a.pageLinks, size = _a.size, caption = _a.caption;
        if (!pageLinks) {
            return null;
        }
        var location = this.context.location;
        var path = this.props.to || location.pathname;
        var query = location.query;
        var links = parseLinkHeader(pageLinks);
        var previousDisabled = links.previous.results === false;
        var nextDisabled = links.next.results === false;
        return (<Wrapper className={className}>
        {caption}
        <ButtonBar merged>
          <Button icon={<IconChevron direction="left" size="sm"/>} aria-label={t('Previous')} size={size} disabled={previousDisabled} onClick={function () {
                callIfFunction(onCursor, links.previous.cursor, path, query, -1);
            }}/>
          <Button icon={<IconChevron direction="right" size="sm"/>} aria-label={t('Next')} size={size} disabled={nextDisabled} onClick={function () {
                callIfFunction(onCursor, links.next.cursor, path, query, 1);
            }}/>
        </ButtonBar>
      </Wrapper>);
    };
    Pagination.contextTypes = {
        location: PropTypes.object,
    };
    Pagination.defaultProps = defaultProps;
    return Pagination;
}(Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: ", " 0 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: ", " 0 0 0;\n"])), space(3));
export default Pagination;
var templateObject_1;
//# sourceMappingURL=index.jsx.map