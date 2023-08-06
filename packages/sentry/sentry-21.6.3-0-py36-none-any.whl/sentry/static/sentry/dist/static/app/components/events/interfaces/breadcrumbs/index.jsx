import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import pick from 'lodash/pick';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import ErrorBoundary from 'app/components/errorBoundary';
import EventDataSection from 'app/components/events/eventDataSection';
import { IconWarning } from 'app/icons/iconWarning';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { BreadcrumbLevelType, BreadcrumbType, } from 'app/types/breadcrumbs';
import { EntryType } from 'app/types/event';
import { defined } from 'app/utils';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SearchBarAction from '../searchBarAction';
import SearchBarActionFilter from '../searchBarAction/searchBarActionFilter';
import Icon from './icon';
import Level from './level';
import List from './list';
import { aroundContentStyle } from './styles';
import { transformCrumbs } from './utils';
var Breadcrumbs = /** @class */ (function (_super) {
    __extends(Breadcrumbs, _super);
    function Breadcrumbs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            breadcrumbs: [],
            filteredByFilter: [],
            filteredBySearch: [],
            filterOptions: {},
            displayRelativeTime: false,
        };
        _this.handleSearch = function (value) {
            _this.setState(function (prevState) { return ({
                searchTerm: value,
                filteredBySearch: _this.filterBySearch(value, prevState.filteredByFilter),
            }); });
        };
        _this.handleFilter = function (filterOptions) {
            var filteredByFilter = _this.getFilteredCrumbsByFilter(filterOptions);
            _this.setState(function (prevState) { return ({
                filterOptions: filterOptions,
                filteredByFilter: filteredByFilter,
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, filteredByFilter),
            }); });
        };
        _this.handleSwitchTimeFormat = function () {
            _this.setState(function (prevState) { return ({
                displayRelativeTime: !prevState.displayRelativeTime,
            }); });
        };
        _this.handleCleanSearch = function () {
            _this.setState({ searchTerm: '' });
        };
        _this.handleResetFilter = function () {
            _this.setState(function (_a) {
                var breadcrumbs = _a.breadcrumbs, filterOptions = _a.filterOptions, searchTerm = _a.searchTerm;
                return ({
                    filteredByFilter: breadcrumbs,
                    filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                        accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (__assign(__assign({}, filterOption), { isChecked: false })); });
                        return accumulator;
                    }, {}),
                    filteredBySearch: _this.filterBySearch(searchTerm, breadcrumbs),
                });
            });
        };
        _this.handleResetSearchBar = function () {
            _this.setState(function (prevState) { return ({
                searchTerm: '',
                filteredBySearch: prevState.breadcrumbs,
            }); });
        };
        return _this;
    }
    Breadcrumbs.prototype.componentDidMount = function () {
        this.loadBreadcrumbs();
    };
    Breadcrumbs.prototype.loadBreadcrumbs = function () {
        var _a;
        var data = this.props.data;
        var breadcrumbs = data.values;
        // Add the (virtual) breadcrumb based on the error or message event if possible.
        var virtualCrumb = this.getVirtualCrumb();
        if (virtualCrumb) {
            breadcrumbs = __spreadArray(__spreadArray([], __read(breadcrumbs)), [virtualCrumb]);
        }
        var transformedCrumbs = transformCrumbs(breadcrumbs);
        var filterOptions = this.getFilterOptions(transformedCrumbs);
        this.setState({
            relativeTime: (_a = transformedCrumbs[transformedCrumbs.length - 1]) === null || _a === void 0 ? void 0 : _a.timestamp,
            breadcrumbs: transformedCrumbs,
            filteredByFilter: transformedCrumbs,
            filteredBySearch: transformedCrumbs,
            filterOptions: filterOptions,
        });
    };
    Breadcrumbs.prototype.getFilterOptions = function (breadcrumbs) {
        var types = this.getFilterTypes(breadcrumbs);
        var levels = this.getFilterLevels(types);
        var options = {};
        if (!!types.length) {
            options[t('Types')] = types.map(function (type) { return omit(type, 'levels'); });
        }
        if (!!levels.length) {
            options[t('Levels')] = levels;
        }
        return options;
    };
    Breadcrumbs.prototype.getFilterTypes = function (breadcrumbs) {
        var filterTypes = [];
        var _loop_1 = function (index) {
            var breadcrumb = breadcrumbs[index];
            var foundFilterType = filterTypes.findIndex(function (f) { return f.id === breadcrumb.type; });
            if (foundFilterType === -1) {
                filterTypes.push({
                    id: breadcrumb.type,
                    symbol: <Icon {...omit(breadcrumb, 'description')} size="xs"/>,
                    isChecked: false,
                    description: breadcrumb.description,
                    levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                });
                return "continue";
            }
            if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                filterTypes[foundFilterType].levels.push(breadcrumb.level);
            }
        };
        for (var index in breadcrumbs) {
            _loop_1(index);
        }
        return filterTypes;
    };
    Breadcrumbs.prototype.getFilterLevels = function (types) {
        var filterLevels = [];
        for (var indexType in types) {
            var _loop_2 = function (indexLevel) {
                var level = types[indexType].levels[indexLevel];
                if (filterLevels.some(function (f) { return f.id === level; })) {
                    return "continue";
                }
                filterLevels.push({
                    id: level,
                    symbol: <Level level={level}/>,
                    isChecked: false,
                });
            };
            for (var indexLevel in types[indexType].levels) {
                _loop_2(indexLevel);
            }
        }
        return filterLevels;
    };
    Breadcrumbs.prototype.moduleToCategory = function (module) {
        if (!module) {
            return undefined;
        }
        var match = module.match(/^.*\/(.*?)(:\d+)/);
        if (!match) {
            return module.split(/./)[0];
        }
        return match[1];
    };
    Breadcrumbs.prototype.getVirtualCrumb = function () {
        var event = this.props.event;
        var exception = event.entries.find(function (entry) { return entry.type === EntryType.EXCEPTION; });
        if (!exception && !event.message) {
            return undefined;
        }
        var timestamp = event.dateCreated;
        if (exception) {
            var _a = exception.data.values[0], type = _a.type, value = _a.value, mdl = _a.module;
            return {
                type: BreadcrumbType.ERROR,
                level: BreadcrumbLevelType.ERROR,
                category: this.moduleToCategory(mdl) || 'exception',
                data: {
                    type: type,
                    value: value,
                },
                timestamp: timestamp,
            };
        }
        var levelTag = (event.tags || []).find(function (tag) { return tag.key === 'level'; });
        return {
            type: BreadcrumbType.INFO,
            level: (levelTag === null || levelTag === void 0 ? void 0 : levelTag.value) || BreadcrumbLevelType.UNDEFINED,
            category: 'message',
            message: event.message,
            timestamp: timestamp,
        };
    };
    Breadcrumbs.prototype.filterBySearch = function (searchTerm, breadcrumbs) {
        if (!searchTerm.trim()) {
            return breadcrumbs;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        var searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        return breadcrumbs.filter(function (obj) {
            return Object.keys(pick(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(function (key) {
                var info = obj[key];
                if (!defined(info) || !String(info).trim()) {
                    return false;
                }
                return JSON.stringify(info)
                    .replace(/((^")|("$))/g, '')
                    .toLocaleLowerCase()
                    .trim()
                    .includes(searchFor);
            });
        });
    };
    Breadcrumbs.prototype.getFilteredCrumbsByFilter = function (filterOptions) {
        var checkedTypeOptions = new Set(Object.values(filterOptions)[0]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        var checkedLevelOptions = new Set(Object.values(filterOptions)[1]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        var breadcrumbs = this.state.breadcrumbs;
        if (!!__spreadArray([], __read(checkedTypeOptions)).length && !!__spreadArray([], __read(checkedLevelOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedTypeOptions.has(filteredCrumb.type) &&
                    checkedLevelOptions.has(filteredCrumb.level);
            });
        }
        if (!!__spreadArray([], __read(checkedTypeOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedTypeOptions.has(filteredCrumb.type);
            });
        }
        if (!!__spreadArray([], __read(checkedLevelOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedLevelOptions.has(filteredCrumb.level);
            });
        }
        return breadcrumbs;
    };
    Breadcrumbs.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, filteredBySearch = _a.filteredBySearch, filterOptions = _a.filterOptions;
        if (searchTerm && !filteredBySearch.length) {
            var hasActiveFilter = Object.values(filterOptions)
                .flatMap(function (filterOption) { return filterOption; })
                .find(function (filterOption) { return filterOption.isChecked; });
            return (<StyledEmptyMessage icon={<IconWarning size="xl"/>} action={hasActiveFilter ? (<Button onClick={this.handleResetFilter} priority="primary">
                {t('Reset filter')}
              </Button>) : (<Button onClick={this.handleResetSearchBar} priority="primary">
                {t('Clear search bar')}
              </Button>)}>
          {t('Sorry, no breadcrumbs match your search query')}
        </StyledEmptyMessage>);
        }
        return (<StyledEmptyMessage icon={<IconWarning size="xl"/>}>
        {t('There are no breadcrumbs to be displayed')}
      </StyledEmptyMessage>);
    };
    Breadcrumbs.prototype.render = function () {
        var _a = this.props, type = _a.type, event = _a.event, organization = _a.organization;
        var _b = this.state, filterOptions = _b.filterOptions, searchTerm = _b.searchTerm, filteredBySearch = _b.filteredBySearch, displayRelativeTime = _b.displayRelativeTime, relativeTime = _b.relativeTime;
        return (<StyledEventDataSection type={type} title={<GuideAnchor target="breadcrumbs" position="right">
            <h3>{t('Breadcrumbs')}</h3>
          </GuideAnchor>} actions={<StyledSearchBarAction placeholder={t('Search breadcrumbs')} onChange={this.handleSearch} query={searchTerm} filter={<SearchBarActionFilter onChange={this.handleFilter} options={filterOptions}/>}/>} wrapTitle={false} isCentered>
        {!!filteredBySearch.length ? (<ErrorBoundary>
            <List breadcrumbs={filteredBySearch} event={event} orgId={organization.slug} onSwitchTimeFormat={this.handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm} relativeTime={relativeTime} // relativeTime has to be always available, as the last item timestamp is the event created time
            />
          </ErrorBoundary>) : (this.getEmptyMessage())}
      </StyledEventDataSection>);
    };
    return Breadcrumbs;
}(React.Component));
export default Breadcrumbs;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StyledEmptyMessage = styled(EmptyMessage)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), aroundContentStyle);
var StyledSearchBarAction = styled(SearchBarAction)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  z-index: 2;\n"], ["\n  z-index: 2;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map