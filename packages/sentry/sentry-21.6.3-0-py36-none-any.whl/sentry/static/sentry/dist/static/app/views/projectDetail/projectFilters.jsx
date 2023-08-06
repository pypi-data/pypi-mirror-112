import { __awaiter, __generator } from "tslib";
import SmartSearchBar from 'app/components/smartSearchBar';
import { t } from 'app/locale';
var supportedTags = {
    'sentry.semver': {
        key: 'sentry.semver',
        name: 'sentry.semver',
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
function ProjectFilters(_a) {
    var _this = this;
    var query = _a.query, tagValueLoader = _a.tagValueLoader, onSearch = _a.onSearch;
    var getTagValues = function (tag, currentQuery) { return __awaiter(_this, void 0, void 0, function () {
        var values;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, tagValueLoader(tag.key, currentQuery)];
                case 1:
                    values = _a.sent();
                    return [2 /*return*/, values.map(function (_a) {
                            var value = _a.value;
                            return value;
                        })];
            }
        });
    }); };
    return (<SmartSearchBar query={query} placeholder={t('Search by release version')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={onSearch} onGetTagValues={getTagValues}/>);
}
export default ProjectFilters;
//# sourceMappingURL=projectFilters.jsx.map