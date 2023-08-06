import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { Content } from 'app/components/dropdownControl';
import { IconFilter } from 'app/icons';
import { t, tn } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function FilterSection(_a) {
    var id = _a.id, label = _a.label, items = _a.items, toggleSection = _a.toggleSection, toggleFilter = _a.toggleFilter;
    var checkedItemsCount = items.filter(function (item) { return item.checked; }).length;
    return (<Fragment>
      <Header>
        <span>{label}</span>
        <CheckboxFancy isChecked={checkedItemsCount === items.length} isIndeterminate={checkedItemsCount > 0 && checkedItemsCount !== items.length} onClick={function (event) {
            event.stopPropagation();
            toggleSection(id);
        }}/>
      </Header>
      {items
            .filter(function (item) { return !item.filtered; })
            .map(function (item) { return (<ListItem key={item.value} isChecked={item.checked} onClick={function (event) {
                event.stopPropagation();
                toggleFilter(id, item.value);
            }}>
            <TeamName>{item.label}</TeamName>
            <CheckboxFancy isChecked={item.checked}/>
          </ListItem>); })}
    </Fragment>);
}
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggleFilter = function (sectionId, value) {
            var _a = _this.props, onFilterChange = _a.onFilterChange, dropdownSections = _a.dropdownSections;
            var section = dropdownSections.find(function (dropdownSection) { return dropdownSection.id === sectionId; });
            var newSelection = new Set(section.items.filter(function (item) { return item.checked; }).map(function (item) { return item.value; }));
            if (newSelection.has(value)) {
                newSelection.delete(value);
            }
            else {
                newSelection.add(value);
            }
            onFilterChange(sectionId, newSelection);
        };
        _this.toggleSection = function (sectionId) {
            var onFilterChange = _this.props.onFilterChange;
            var section = _this.props.dropdownSections.find(function (dropdownSection) { return dropdownSection.id === sectionId; });
            var activeItems = section.items.filter(function (item) { return item.checked; });
            var newSelection = section.items.length === activeItems.length
                ? new Set()
                : new Set(section.items.map(function (item) { return item.value; }));
            onFilterChange(sectionId, newSelection);
        };
        _this.getNumberOfActiveFilters = function () {
            return _this.props.dropdownSections
                .map(function (section) { return section.items; })
                .flat()
                .filter(function (item) { return item.checked; }).length;
        };
        return _this;
    }
    Filter.prototype.render = function () {
        var _this = this;
        var _a = this.props, dropdownItems = _a.dropdownSections, header = _a.header;
        var checkedQuantity = this.getNumberOfActiveFilters();
        var dropDownButtonProps = {
            children: t('Filter'),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = tn('%s Active Filter', '%s Active Filters', checkedQuantity);
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<DropdownControl menuWidth="240px" blendWithActor alwaysRenderMenu={false} button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} icon={<IconFilter size="xs"/>} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
            {dropDownButtonProps.children}
          </StyledDropdownButton>);
            }}>
        {function (_a) {
                var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps;
                return (<MenuContent {...getMenuProps()} isOpen={isOpen} blendCorner alignMenu="left" width="240px">
            <List>
              {header}
              {dropdownItems.map(function (section) { return (<FilterSection key={section.id} {...section} toggleSection={_this.toggleSection} toggleFilter={_this.toggleFilter}/>); })}
            </List>
          </MenuContent>);
            }}
      </DropdownControl>);
    };
    return Filter;
}(Component));
var MenuContent = styled(Content)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-height: 290px;\n  overflow-y: auto;\n"], ["\n  max-height: 290px;\n  overflow-y: auto;\n"])));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.dropdown; });
var List = styled('ul')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled('li')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, CheckboxFancy, function (p) { return p.theme.blue300; });
var TeamName = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis);
export default Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=filter.jsx.map