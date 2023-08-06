import { __assign, __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
import { DisplayOption, SortOption } from './utils';
function ReleaseListSortOptions(_a) {
    var _b, _c, _d;
    var selected = _a.selected, selectedDisplay = _a.selectedDisplay, onSelect = _a.onSelect, organization = _a.organization;
    var sortOptions = __assign((_b = {}, _b[SortOption.DATE] = t('Date Created'), _b[SortOption.SESSIONS] = t('Total Sessions'), _b), (selectedDisplay === DisplayOption.USERS
        ? (_c = {},
            _c[SortOption.USERS_24_HOURS] = t('Active Users'),
            _c[SortOption.CRASH_FREE_USERS] = t('Crash Free Users'),
            _c) : (_d = {},
        _d[SortOption.SESSIONS_24_HOURS] = t('Active Sessions'),
        _d[SortOption.CRASH_FREE_SESSIONS] = t('Crash Free Sessions'),
        _d)));
    if (organization.features.includes('semver')) {
        sortOptions[SortOption.BUILD] = t('Build Number');
        sortOptions[SortOption.SEMVER] = t('Semantic Version');
    }
    if (organization.features.includes('release-adoption-stage')) {
        sortOptions[SortOption.ADOPTION] = t('Date Adopted');
    }
    return (<StyledReleaseListDropdown label={t('Sort By')} options={sortOptions} selected={selected} onSelect={onSelect}/>);
}
export default ReleaseListSortOptions;
var StyledReleaseListDropdown = styled(ReleaseListDropdown)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"], ["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseListSortOptions.jsx.map