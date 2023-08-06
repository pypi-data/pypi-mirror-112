import forEach from 'lodash/forEach';
import set from 'lodash/set';
export function expandKeys(obj) {
    var result = {};
    forEach(obj, function (value, key) {
        set(result, key.split('.'), value);
    });
    return result;
}
//# sourceMappingURL=utils.jsx.map