import { __assign, __extends, __makeTemplateObject, __read, __rest, __spreadArray, __values } from "tslib";
import { createRef, Fragment, PureComponent } from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { generateFieldAsString, getColumnType } from 'app/utils/discover/fields';
import Input from 'app/views/settings/components/forms/controls/input';
var NONE_SELECTED = -1;
var ArithmeticInput = /** @class */ (function (_super) {
    __extends(ArithmeticInput, _super);
    function ArithmeticInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: _this.props.value,
            partialTerm: null,
            rawOptions: _this.props.options,
            dropdownVisible: false,
            dropdownOptionGroups: makeOptions(_this.props.options, null),
            activeSelection: NONE_SELECTED,
        };
        _this.input = createRef();
        _this.blur = function () {
            var _a;
            (_a = _this.input.current) === null || _a === void 0 ? void 0 : _a.blur();
        };
        _this.focus = function (position) {
            var _a, _b;
            (_a = _this.input.current) === null || _a === void 0 ? void 0 : _a.focus();
            (_b = _this.input.current) === null || _b === void 0 ? void 0 : _b.setSelectionRange(position, position);
        };
        _this.handleChange = function (event) {
            var query = event.target.value.replace('\n', '');
            _this.setState({ query: query }, _this.updateAutocompleteOptions);
        };
        _this.handleClick = function () {
            _this.updateAutocompleteOptions();
        };
        _this.handleFocus = function () {
            _this.setState({ dropdownVisible: true });
        };
        _this.handleBlur = function () {
            _this.props.onUpdate(_this.state.query);
            _this.setState({ dropdownVisible: false });
        };
        _this.handleKeyDown = function (event) {
            var key = event.key;
            var options = _this.props.options;
            var _a = _this.state, activeSelection = _a.activeSelection, partialTerm = _a.partialTerm;
            var startedSelection = activeSelection >= 0;
            // handle arrow navigation
            if (key === 'ArrowDown' || key === 'ArrowUp') {
                event.preventDefault();
                var newOptionGroups = makeOptions(options, partialTerm);
                var flattenedOptions = newOptionGroups.map(function (group) { return group.options; }).flat();
                var newSelection = void 0;
                if (!startedSelection) {
                    newSelection = key === 'ArrowUp' ? flattenedOptions.length - 1 : 0;
                }
                else {
                    newSelection =
                        key === 'ArrowUp'
                            ? (activeSelection - 1 + flattenedOptions.length) % flattenedOptions.length
                            : (activeSelection + 1) % flattenedOptions.length;
                }
                // This is modifying the `active` value of the references so make sure to
                // use `newOptionGroups` at the end.
                flattenedOptions[newSelection].active = true;
                _this.setState({
                    activeSelection: newSelection,
                    dropdownOptionGroups: newOptionGroups,
                });
                return;
            }
            // handle selection
            if (startedSelection && (key === 'Tab' || key === 'Enter')) {
                event.preventDefault();
                var selection = _this.getSelection(activeSelection);
                if (selection) {
                    _this.handleSelect(selection);
                }
                return;
            }
            if (key === 'Enter') {
                _this.blur();
                return;
            }
        };
        _this.handleKeyUp = function (event) {
            // Other keys are managed at handleKeyDown function
            if (event.key !== 'Escape') {
                return;
            }
            event.preventDefault();
            var activeSelection = _this.state.activeSelection;
            var startedSelection = activeSelection >= 0;
            if (!startedSelection) {
                _this.blur();
                return;
            }
        };
        _this.handleSelect = function (option) {
            var _a = _this.splitQuery(), prefix = _a.prefix, suffix = _a.suffix;
            _this.setState({
                // make sure to insert a space after the autocompleted term
                query: "" + prefix + option.value + " " + suffix,
                activeSelection: NONE_SELECTED,
            }, function () {
                // updating the query will cause the input to lose focus
                // and make sure to move the cursor behind the space after
                // the end of the autocompleted term
                _this.focus(prefix.length + option.value.length + 1);
                _this.updateAutocompleteOptions();
            });
        };
        return _this;
    }
    ArithmeticInput.getDerivedStateFromProps = function (props, state) {
        var changed = !isEqual(state.rawOptions, props.options);
        if (changed) {
            return __assign(__assign({}, state), { rawOptions: props.options, dropdownOptionGroups: makeOptions(props.options, state.partialTerm), activeSelection: NONE_SELECTED });
        }
        return __assign({}, state);
    };
    ArithmeticInput.prototype.getCursorPosition = function () {
        var _a, _b;
        return (_b = (_a = this.input.current) === null || _a === void 0 ? void 0 : _a.selectionStart) !== null && _b !== void 0 ? _b : -1;
    };
    ArithmeticInput.prototype.splitQuery = function () {
        var query = this.state.query;
        var currentPosition = this.getCursorPosition();
        // The current term is delimited by whitespaces. So if no spaces are found,
        // the entire string is taken to be 1 term.
        //
        // TODO: add support for when there are no spaces
        var matches = __spreadArray([], __read(query.substring(0, currentPosition).matchAll(/\s|^/g)));
        var match = matches[matches.length - 1];
        var startOfTerm = match[0] === '' ? 0 : (match.index || 0) + 1;
        var cursorOffset = query.slice(currentPosition).search(/\s|$/);
        var endOfTerm = currentPosition + (cursorOffset === -1 ? 0 : cursorOffset);
        return {
            startOfTerm: startOfTerm,
            endOfTerm: endOfTerm,
            prefix: query.substring(0, startOfTerm),
            term: query.substring(startOfTerm, endOfTerm),
            suffix: query.substring(endOfTerm),
        };
    };
    ArithmeticInput.prototype.getSelection = function (selection) {
        var e_1, _a;
        var dropdownOptionGroups = this.state.dropdownOptionGroups;
        try {
            for (var dropdownOptionGroups_1 = __values(dropdownOptionGroups), dropdownOptionGroups_1_1 = dropdownOptionGroups_1.next(); !dropdownOptionGroups_1_1.done; dropdownOptionGroups_1_1 = dropdownOptionGroups_1.next()) {
                var group = dropdownOptionGroups_1_1.value;
                if (selection >= group.options.length) {
                    selection -= group.options.length;
                    continue;
                }
                return group.options[selection];
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (dropdownOptionGroups_1_1 && !dropdownOptionGroups_1_1.done && (_a = dropdownOptionGroups_1.return)) _a.call(dropdownOptionGroups_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return null;
    };
    ArithmeticInput.prototype.updateAutocompleteOptions = function () {
        var options = this.props.options;
        var term = this.splitQuery().term;
        var partialTerm = term || null;
        this.setState({
            dropdownOptionGroups: makeOptions(options, partialTerm),
            partialTerm: partialTerm,
        });
    };
    ArithmeticInput.prototype.render = function () {
        var _a = this.props, _onUpdate = _a.onUpdate, _options = _a.options, props = __rest(_a, ["onUpdate", "options"]);
        var _b = this.state, dropdownVisible = _b.dropdownVisible, dropdownOptionGroups = _b.dropdownOptionGroups;
        return (<Container isOpen={dropdownVisible}>
        <StyledInput {...props} ref={this.input} autoComplete="off" className="form-control" value={this.state.query} onClick={this.handleClick} onChange={this.handleChange} onBlur={this.handleBlur} onFocus={this.handleFocus} onKeyDown={this.handleKeyDown}/>
        <TermDropdown isOpen={dropdownVisible} optionGroups={dropdownOptionGroups} handleSelect={this.handleSelect}/>
      </Container>);
    };
    ArithmeticInput.defaultProps = {
        options: [],
    };
    return ArithmeticInput;
}(PureComponent));
export default ArithmeticInput;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  box-shadow: inset ", ";\n  background: ", ";\n  position: relative;\n\n  border-radius: ", ";\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"], ["\n  border: 1px solid ", ";\n  box-shadow: inset ", ";\n  background: ", ";\n  position: relative;\n\n  border-radius: ", ";\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.background; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"
        : p.theme.borderRadius;
}, function (p) { return p.theme.backgroundSecondary; });
var StyledInput = styled(Input)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 40px;\n  padding: 7px 10px;\n  border: 0;\n  box-shadow: none;\n\n  &:hover,\n  &:focus {\n    border: 0;\n    box-shadow: none;\n  }\n"], ["\n  height: 40px;\n  padding: 7px 10px;\n  border: 0;\n  box-shadow: none;\n\n  &:hover,\n  &:focus {\n    border: 0;\n    box-shadow: none;\n  }\n"])));
function TermDropdown(_a) {
    var isOpen = _a.isOpen, optionGroups = _a.optionGroups, handleSelect = _a.handleSelect;
    return (<DropdownContainer isOpen={isOpen}>
      <DropdownItemsList>
        {optionGroups.map(function (group) {
            var title = group.title, options = group.options;
            return (<Fragment key={title}>
              <ListItem>
                <DropdownTitle>{title}</DropdownTitle>
              </ListItem>
              {options.map(function (option) {
                    return (<DropdownListItem key={option.value} className={option.active ? 'active' : undefined} onClick={function () { return handleSelect(option); }} 
                    // prevent the blur event on the input from firing
                    onMouseDown={function (event) { return event.preventDefault(); }} 
                    // scroll into view if it is the active element
                    ref={function (element) { var _a; return option.active && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}>
                    <DropdownItemTitleWrapper>{option.value}</DropdownItemTitleWrapper>
                  </DropdownListItem>);
                })}
              {options.length === 0 && <Info>{t('No items found')}</Info>}
            </Fragment>);
        })}
      </DropdownItemsList>
    </DropdownContainer>);
}
function makeFieldOptions(columns, partialTerm) {
    var options = columns
        .filter(function (_a) {
        var kind = _a.kind;
        return kind !== 'equation';
    })
        .filter(function (option) {
        var columnType = getColumnType(option);
        return (columnType === 'number' || columnType === 'integer' || columnType === 'duration');
    })
        .map(function (option) { return ({
        kind: 'field',
        active: false,
        value: generateFieldAsString(option),
    }); })
        .filter(function (_a) {
        var value = _a.value;
        return (partialTerm ? value.includes(partialTerm) : true);
    });
    return {
        title: 'Fields',
        options: options,
    };
}
function makeOperatorOptions(partialTerm) {
    var options = ['+', '-', '*', '/']
        .filter(function (operator) { return (partialTerm ? operator.includes(partialTerm) : true); })
        .map(function (operator) { return ({
        kind: 'operator',
        active: false,
        value: operator,
    }); });
    return {
        title: 'Operators',
        options: options,
    };
}
function makeOptions(columns, partialTerm) {
    return [makeFieldOptions(columns, partialTerm), makeOperatorOptions(partialTerm)];
}
var DropdownContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Container has a border that we need to account for */\n  display: ", ";\n  position: absolute;\n  top: 100%;\n  left: -1px;\n  right: -1px;\n  z-index: ", ";\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  max-height: 300px;\n  overflow-y: auto;\n"], ["\n  /* Container has a border that we need to account for */\n  display: ", ";\n  position: absolute;\n  top: 100%;\n  left: -1px;\n  right: -1px;\n  z-index: ", ";\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  max-height: 300px;\n  overflow-y: auto;\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); }, function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadiusBottom; });
var DropdownItemsList = styled('ul')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"], ["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"])));
var ListItem = styled('li')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; });
var DropdownTitle = styled('header')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n\n  margin: 0;\n  padding: ", " ", ";\n\n  & > svg {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n\n  margin: 0;\n  padding: ", " ", ";\n\n  & > svg {\n    margin-right: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), space(1));
var DropdownListItem = styled(ListItem)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  scroll-margin: 40px 0;\n  font-size: ", ";\n  padding: ", " ", ";\n  cursor: pointer;\n\n  &:hover,\n  &.active {\n    background: ", ";\n  }\n"], ["\n  scroll-margin: 40px 0;\n  font-size: ", ";\n  padding: ", " ", ";\n  cursor: pointer;\n\n  &:hover,\n  &.active {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space(1), space(2), function (p) { return p.theme.focus; });
var DropdownItemTitleWrapper = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  margin: 0;\n  line-height: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  margin: 0;\n  line-height: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.text.lineHeightHeading; }, overflowEllipsis);
var Info = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n  font-size: ", ";\n  color: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  display: flex;\n  padding: ", " ", ";\n  font-size: ", ";\n  color: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(1), space(2), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.innerBorder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=arithmeticInput.jsx.map