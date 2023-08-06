import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import { ClassNames } from '@emotion/react';
import memoize from 'lodash/memoize';
import SmartSearchBar from 'app/components/smartSearchBar';
import { NEGATION_OPERATOR, SEARCH_WILDCARD } from 'app/constants';
import { t } from 'app/locale';
var SEARCH_SPECIAL_CHARS_REGEXP = new RegExp("^" + NEGATION_OPERATOR + "|\\" + SEARCH_WILDCARD, 'g');
function SearchQueryField(_a) {
    var api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, tags = _a.tags, onSearch = _a.onSearch, onBlur = _a.onBlur;
    /**
     * Prepare query string (e.g. strip special characters like negation operator)
     */
    function prepareQuery(query) {
        return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, '');
    }
    function fetchTagValues(tagKey) {
        return api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/metrics/tags/" + tagKey + "/", {
            method: 'GET',
        });
    }
    function getTagValues(tag, _query) {
        return fetchTagValues(tag.key).then(function (tagValues) { return tagValues; }, function () {
            throw new Error('Unable to fetch tag values');
        });
    }
    var supportedTags = tags.reduce(function (acc, tag) {
        acc[tag] = { key: tag, name: tag };
        return acc;
    }, {});
    return (<ClassNames>
      {function (_a) {
            var css = _a.css;
            return (<SmartSearchBar placeholder={t('Search for tag')} onGetTagValues={memoize(getTagValues, function (_a, query) {
                var key = _a.key;
                return key + "-" + query;
            })} supportedTags={supportedTags} prepareQuery={prepareQuery} onSearch={onSearch} onBlur={onBlur} useFormWrapper={false} excludeEnvironment dropdownClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n            max-height: 300px;\n            overflow-y: auto;\n          "], ["\n            max-height: 300px;\n            overflow-y: auto;\n          "])))}/>);
        }}
    </ClassNames>);
}
export default SearchQueryField;
var templateObject_1;
//# sourceMappingURL=searchQueryField.jsx.map