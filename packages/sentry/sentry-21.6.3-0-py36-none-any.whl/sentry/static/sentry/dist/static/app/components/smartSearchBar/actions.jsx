import { __assign, __awaiter, __generator, __makeTemplateObject, __rest } from "tslib";
import { browserHistory, withRouter } from 'react-router';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import { pinSearch, unpinSearch } from 'app/actionCreators/savedSearches';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import MenuItem from 'app/components/menuItem';
import { IconAdd, IconPin, IconSliders } from 'app/icons';
import { t } from 'app/locale';
import { SavedSearchType } from 'app/types';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import CreateSavedSearchModal from 'app/views/issueList/createSavedSearchModal';
import { removeSpace } from './utils';
/**
 * The Pin Search action toggles the current as a pinned search
 */
export function makePinSearchAction(_a) {
    var _this = this;
    var pinnedSearch = _a.pinnedSearch, sort = _a.sort;
    var PinSearchAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant, savedSearchType = _a.savedSearchType, organization = _a.organization, api = _a.api, query = _a.query, location = _a.location;
        var onTogglePinnedSearch = function (evt) { return __awaiter(_this, void 0, void 0, function () {
            var _a, _cursor, _page, currentQuery, resp;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        evt.preventDefault();
                        evt.stopPropagation();
                        if (savedSearchType === undefined) {
                            return [2 /*return*/];
                        }
                        _a = location.query, _cursor = _a.cursor, _page = _a.page, currentQuery = __rest(_a, ["cursor", "page"]);
                        trackAnalyticsEvent({
                            eventKey: 'search.pin',
                            eventName: 'Search: Pin',
                            organization_id: organization.id,
                            action: !!pinnedSearch ? 'unpin' : 'pin',
                            search_type: savedSearchType === SavedSearchType.ISSUE ? 'issues' : 'events',
                            query: (_b = pinnedSearch === null || pinnedSearch === void 0 ? void 0 : pinnedSearch.query) !== null && _b !== void 0 ? _b : query,
                        });
                        if (!!pinnedSearch) {
                            unpinSearch(api, organization.slug, savedSearchType, pinnedSearch).then(function () {
                                browserHistory.push(__assign(__assign({}, location), { pathname: "/organizations/" + organization.slug + "/issues/", query: __assign(__assign({}, currentQuery), { query: pinnedSearch.query, sort: pinnedSearch.sort }) }));
                            });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, pinSearch(api, organization.slug, savedSearchType, removeSpace(query), sort)];
                    case 1:
                        resp = _c.sent();
                        if (!resp || !resp.id) {
                            return [2 /*return*/];
                        }
                        browserHistory.push(__assign(__assign({}, location), { pathname: "/organizations/" + organization.slug + "/issues/searches/" + resp.id + "/", query: currentQuery }));
                        return [2 /*return*/];
                }
            });
        }); };
        var pinTooltip = !!pinnedSearch ? t('Unpin this search') : t('Pin this search');
        return menuItemVariant ? (<MenuItem withBorder data-test-id="pin-icon" icon={<IconPin isSolid={!!pinnedSearch} size="xs"/>} onClick={onTogglePinnedSearch}>
        {!!pinnedSearch ? t('Unpin Search') : t('Pin Search')}
      </MenuItem>) : (<ActionButton title={pinTooltip} disabled={!query} aria-label={pinTooltip} onClick={onTogglePinnedSearch} isActive={!!pinnedSearch} data-test-id="pin-icon" icon={<IconPin isSolid={!!pinnedSearch} size="xs"/>}/>);
    };
    return { key: 'pinSearch', Action: withRouter(PinSearchAction) };
}
/**
 * The Save Search action triggers the create saved search modal from the
 * current query.
 */
export function makeSaveSearchAction(_a) {
    var sort = _a.sort;
    var SavedSearchAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant, query = _a.query, organization = _a.organization;
        var onClick = function () {
            return openModal(function (deps) { return (<CreateSavedSearchModal {...deps} {...{ organization: organization, query: query, sort: sort }}/>); });
        };
        return (<Access organization={organization} access={['org:write']}>
        {menuItemVariant ? (<MenuItem withBorder icon={<IconAdd size="xs"/>} onClick={onClick}>
            {t('Create Saved Search')}
          </MenuItem>) : (<ActionButton onClick={onClick} data-test-id="save-current-search" icon={<IconAdd size="xs"/>} title={t('Add to organization saved searches')} aria-label={t('Add to organization saved searches')}/>)}
      </Access>);
    };
    return { key: 'saveSearch', Action: SavedSearchAction };
}
/**
 * The Search Builder action toggles the Issue Stream search builder
 */
export function makeSearchBuilderAction(_a) {
    var onSidebarToggle = _a.onSidebarToggle;
    var SearchBuilderAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant;
        return menuItemVariant ? (<MenuItem withBorder icon={<IconSliders size="xs"/>} onClick={onSidebarToggle}>
        {t('Toggle sidebar')}
      </MenuItem>) : (<ActionButton title={t('Toggle search builder')} tooltipProps={{ containerDisplayMode: 'inline-flex' }} aria-label={t('Toggle search builder')} onClick={onSidebarToggle} icon={<IconSliders size="xs"/>}/>);
    };
    return { key: 'searchBuilder', Action: SearchBuilderAction };
}
export var ActionButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  width: 18px;\n\n  &,\n  &:hover,\n  &:focus {\n    background: transparent;\n  }\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  width: 18px;\n\n  &,\n  &:hover,\n  &:focus {\n    background: transparent;\n  }\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return (p.isActive ? p.theme.blue300 : p.theme.gray300); }, function (p) { return p.theme.gray400; });
ActionButton.defaultProps = {
    type: 'button',
    borderless: true,
    size: 'zero',
};
var templateObject_1;
//# sourceMappingURL=actions.jsx.map