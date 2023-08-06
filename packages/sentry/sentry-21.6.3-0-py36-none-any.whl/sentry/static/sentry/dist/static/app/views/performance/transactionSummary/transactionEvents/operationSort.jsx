import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import ReactDOM from 'react-dom';
import { Manager, Popper, Reference } from 'react-popper';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import MenuItem from 'app/components/menuItem';
import Radio from 'app/components/radio';
import { t } from 'app/locale';
var OperationSort = /** @class */ (function (_super) {
    __extends(OperationSort, _super);
    function OperationSort(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isOpen: false,
        };
        _this.handleClickOutside = function (event) {
            if (!_this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (_this.menuEl.contains(event.target)) {
                return;
            }
            _this.setState({ isOpen: false });
        };
        _this.toggleOpen = function () {
            _this.setState(function (_a) {
                var isOpen = _a.isOpen;
                return ({ isOpen: !isOpen });
            });
        };
        var portal = document.getElementById('transaction-events-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'transaction-events-portal');
            document.body.appendChild(portal);
        }
        _this.portalEl = portal;
        _this.menuEl = null;
        return _this;
    }
    OperationSort.prototype.componentDidUpdate = function (_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    };
    OperationSort.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.handleClickOutside, true);
        this.portalEl.remove();
    };
    OperationSort.prototype.generateSortLink = function (field) {
        var _a = this.props, eventView = _a.eventView, tableMeta = _a.tableMeta, location = _a.location;
        if (!tableMeta) {
            return undefined;
        }
        var nextEventView = eventView.sortOnField(field, tableMeta, 'desc');
        var queryStringObject = nextEventView.generateQueryStringObject();
        return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { sort: queryStringObject.sort }) });
    };
    OperationSort.prototype.renderMenuItem = function (operation, title) {
        var _this = this;
        var eventView = this.props.eventView;
        return (<DropdownMenuItem>
        <MenuItemContent>
          <RadioLabel>
            <StyledRadio readOnly radioSize="small" checked={eventView.sorts.some(function (_a) {
            var field = _a.field;
            return field === operation;
        })} onClick={function () {
                var sortLink = _this.generateSortLink({ field: operation });
                if (sortLink)
                    browserHistory.push(sortLink);
            }}/>
            <span>{title}</span>
          </RadioLabel>
        </MenuItemContent>
      </DropdownMenuItem>);
    };
    OperationSort.prototype.renderMenuContent = function () {
        return (<DropdownContent>
        {this.renderMenuItem('spans.http', t('Sort By HTTP'))}
        {this.renderMenuItem('spans.db', t('Sort By DB'))}
        {this.renderMenuItem('spans.resource', t('Sort By Resource'))}
        {this.renderMenuItem('spans.browser', t('Sort By Browser'))}
      </DropdownContent>);
    };
    OperationSort.prototype.renderMenu = function () {
        var _this = this;
        var modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        return ReactDOM.createPortal(<Popper placement="top" modifiers={modifiers}>
        {function (_a) {
                var popperRef = _a.ref, style = _a.style, placement = _a.placement;
                return (<DropdownWrapper ref={function (ref) {
                        popperRef(ref);
                        _this.menuEl = ref;
                    }} style={style} data-placement={placement}>
            {_this.renderMenuContent()}
          </DropdownWrapper>);
            }}
      </Popper>, this.portalEl);
    };
    OperationSort.prototype.render = function () {
        var _this = this;
        var Title = this.props.title;
        var isOpen = this.state.isOpen;
        var menu = isOpen ? this.renderMenu() : null;
        return (<Manager>
        <Reference>
          {function (_a) {
                var ref = _a.ref;
                return (<TitleWrapper ref={ref}>
              <Title onClick={_this.toggleOpen}/>
            </TitleWrapper>);
            }}
        </Reference>
        {menu}
      </Manager>);
    };
    return OperationSort;
}(Component));
var DropdownWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Adapted from the dropdown-menu class */\n  border: none;\n  border-radius: 2px;\n  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);\n  background-clip: padding-box;\n  background-color: ", ";\n  width: 220px;\n  overflow: visible;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    right: auto;\n  }\n\n  &:before {\n    border-left: 9px solid transparent;\n    border-right: 9px solid transparent;\n    left: calc(50% - 9px);\n    z-index: -2;\n  }\n\n  &:after {\n    border-left: 8px solid transparent;\n    border-right: 8px solid transparent;\n    left: calc(50% - 8px);\n    z-index: -1;\n  }\n\n  &[data-placement*='bottom'] {\n    margin-top: 9px;\n\n    &:before {\n      border-bottom: 9px solid ", ";\n      top: -9px;\n    }\n\n    &:after {\n      border-bottom: 8px solid ", ";\n      top: -8px;\n    }\n  }\n\n  &[data-placement*='top'] {\n    margin-bottom: 9px;\n\n    &:before {\n      border-top: 9px solid ", ";\n      bottom: -9px;\n    }\n\n    &:after {\n      border-top: 8px solid ", ";\n      bottom: -8px;\n    }\n  }\n"], ["\n  /* Adapted from the dropdown-menu class */\n  border: none;\n  border-radius: 2px;\n  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);\n  background-clip: padding-box;\n  background-color: ", ";\n  width: 220px;\n  overflow: visible;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    right: auto;\n  }\n\n  &:before {\n    border-left: 9px solid transparent;\n    border-right: 9px solid transparent;\n    left: calc(50% - 9px);\n    z-index: -2;\n  }\n\n  &:after {\n    border-left: 8px solid transparent;\n    border-right: 8px solid transparent;\n    left: calc(50% - 8px);\n    z-index: -1;\n  }\n\n  &[data-placement*='bottom'] {\n    margin-top: 9px;\n\n    &:before {\n      border-bottom: 9px solid ", ";\n      top: -9px;\n    }\n\n    &:after {\n      border-bottom: 8px solid ", ";\n      top: -8px;\n    }\n  }\n\n  &[data-placement*='top'] {\n    margin-bottom: 9px;\n\n    &:before {\n      border-top: 9px solid ", ";\n      bottom: -9px;\n    }\n\n    &:after {\n      border-top: 8px solid ", ";\n      bottom: -8px;\n    }\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.zIndex.tooltip; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; });
var DropdownMenuItem = styled(MenuItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  font-size: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; });
var MenuItemContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: flex-start;\n  align-items: center;\n  width: 100%;\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: flex-start;\n  align-items: center;\n  width: 100%;\n"])));
var RadioLabel = styled('label')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  cursor: pointer;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"], ["\n  display: grid;\n  cursor: pointer;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"])));
var StyledRadio = styled(Radio)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var DropdownContent = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n"])));
var TitleWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  cursor: pointer;\n"], ["\n  cursor: pointer;\n"])));
export default OperationSort;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=operationSort.jsx.map