import { __assign, __read, __spreadArray } from "tslib";
import { filterTypeConfig, interchangeableFilterOperators, TermOperator, } from 'app/components/searchSyntax/parser';
import { IconClock, IconStar, IconTag, IconToggle, IconUser } from 'app/icons';
import { t } from 'app/locale';
import { ItemType } from './types';
export function addSpace(query) {
    if (query === void 0) { query = ''; }
    if (query.length !== 0 && query[query.length - 1] !== ' ') {
        return query + ' ';
    }
    return query;
}
export function removeSpace(query) {
    if (query === void 0) { query = ''; }
    if (query[query.length - 1] === ' ') {
        return query.slice(0, query.length - 1);
    }
    return query;
}
/**
 * Given a query, and the current cursor position, return the string-delimiting
 * index of the search term designated by the cursor.
 */
export function getLastTermIndex(query, cursor) {
    // TODO: work with quoted-terms
    var cursorOffset = query.slice(cursor).search(/\s|$/);
    return cursor + (cursorOffset === -1 ? 0 : cursorOffset);
}
/**
 * Returns an array of query terms, including incomplete terms
 *
 * e.g. ["is:unassigned", "browser:\"Chrome 33.0\"", "assigned"]
 */
export function getQueryTerms(query, cursor) {
    return query.slice(0, cursor).match(/\S+:"[^"]*"?|\S+/g);
}
function getTitleForType(type) {
    if (type === ItemType.TAG_VALUE) {
        return t('Tag Values');
    }
    if (type === ItemType.RECENT_SEARCH) {
        return t('Recent Searches');
    }
    if (type === ItemType.DEFAULT) {
        return t('Common Search Terms');
    }
    if (type === ItemType.TAG_OPERATOR) {
        return t('Operator Helpers');
    }
    return t('Tags');
}
function getIconForTypeAndTag(type, tagName) {
    if (type === ItemType.RECENT_SEARCH) {
        return <IconClock size="xs"/>;
    }
    if (type === ItemType.DEFAULT) {
        return <IconStar size="xs"/>;
    }
    // Change based on tagName and default to "icon-tag"
    switch (tagName) {
        case 'is':
            return <IconToggle size="xs"/>;
        case 'assigned':
        case 'bookmarks':
            return <IconUser size="xs"/>;
        case 'firstSeen':
        case 'lastSeen':
        case 'event.timestamp':
            return <IconClock size="xs"/>;
        default:
            return <IconTag size="xs"/>;
    }
}
export function createSearchGroups(searchItems, recentSearchItems, tagName, type, maxSearchItems, queryCharsLeft) {
    var activeSearchItem = 0;
    if (maxSearchItems && maxSearchItems > 0) {
        searchItems = searchItems.filter(function (value, index) {
            return index < maxSearchItems || value.ignoreMaxSearchItems;
        });
    }
    if (queryCharsLeft || queryCharsLeft === 0) {
        searchItems = searchItems.filter(function (value) { return value.value.length <= queryCharsLeft; });
        if (recentSearchItems) {
            recentSearchItems = recentSearchItems.filter(function (value) { return value.value.length <= queryCharsLeft; });
        }
    }
    var searchGroup = {
        title: getTitleForType(type),
        type: type === ItemType.INVALID_TAG ? type : 'header',
        icon: getIconForTypeAndTag(type, tagName),
        children: __spreadArray([], __read(searchItems)),
    };
    var recentSearchGroup = recentSearchItems && {
        title: t('Recent Searches'),
        type: 'header',
        icon: <IconClock size="xs"/>,
        children: __spreadArray([], __read(recentSearchItems)),
    };
    if (searchGroup.children && !!searchGroup.children.length) {
        searchGroup.children[activeSearchItem] = __assign({}, searchGroup.children[activeSearchItem]);
    }
    return {
        searchGroups: __spreadArray([searchGroup], __read((recentSearchGroup ? [recentSearchGroup] : []))),
        flatSearchItems: __spreadArray(__spreadArray([], __read(searchItems)), __read((recentSearchItems ? recentSearchItems : []))),
        activeSearchItem: -1,
    };
}
/**
 * Items is a list of dropdown groups that have a `children` field. Only the
 * `children` are selectable, so we need to find which child is selected given
 * an index that is in range of the sum of all `children` lengths
 *
 * @return Returns a tuple of [groupIndex, childrenIndex]
 */
export function filterSearchGroupsByIndex(items, index) {
    var _index = index;
    var foundSearchItem = [undefined, undefined];
    items.find(function (_a, i) {
        var children = _a.children;
        if (!children || !children.length) {
            return false;
        }
        if (_index < children.length) {
            foundSearchItem = [i, _index];
            return true;
        }
        _index -= children.length;
        return false;
    });
    return foundSearchItem;
}
export function generateOperatorEntryMap(tag) {
    var _a;
    return _a = {},
        _a[TermOperator.Default] = {
            type: ItemType.TAG_OPERATOR,
            value: ':',
            desc: tag + ":" + t('[value] is equal to'),
        },
        _a[TermOperator.GreaterThanEqual] = {
            type: ItemType.TAG_OPERATOR,
            value: ':>=',
            desc: tag + ":" + t('>=[value] is greater than or equal to'),
        },
        _a[TermOperator.LessThanEqual] = {
            type: ItemType.TAG_OPERATOR,
            value: ':<=',
            desc: tag + ":" + t('<=[value] is less than or equal to'),
        },
        _a[TermOperator.GreaterThan] = {
            type: ItemType.TAG_OPERATOR,
            value: ':>',
            desc: tag + ":" + t('>[value] is greater than'),
        },
        _a[TermOperator.LessThan] = {
            type: ItemType.TAG_OPERATOR,
            value: ':<',
            desc: tag + ":" + t('<[value] is less than'),
        },
        _a[TermOperator.Equal] = {
            type: ItemType.TAG_OPERATOR,
            value: ':=',
            desc: tag + ":" + t('=[value] is equal to'),
        },
        _a[TermOperator.NotEqual] = {
            type: ItemType.TAG_OPERATOR,
            value: '!:',
            desc: "!" + tag + ":" + t('[value] is not equal to'),
        },
        _a;
}
export function getValidOps(filterToken) {
    var _a, _b;
    // If the token is invalid we want to use the possible expected types as our filter type
    var validTypes = (_b = (_a = filterToken.invalid) === null || _a === void 0 ? void 0 : _a.expectedType) !== null && _b !== void 0 ? _b : [filterToken.filter];
    // Determine any interchangable filter types for our valid types
    var interchangeableTypes = validTypes.map(function (type) { var _a; return (_a = interchangeableFilterOperators[type]) !== null && _a !== void 0 ? _a : []; });
    // Combine all types
    var allValidTypes = __spreadArray([], __read(new Set(__spreadArray(__spreadArray([], __read(validTypes)), __read(interchangeableTypes.flat())))));
    // Find all valid operations
    var validOps = new Set(allValidTypes.map(function (type) { return filterTypeConfig[type].validOps; }).flat());
    return __spreadArray([], __read(validOps));
}
//# sourceMappingURL=utils.jsx.map