import { __read } from "tslib";
import KeyValueList from 'app/components/events/interfaces/keyValueList';
import { getMeta } from 'app/components/events/meta/metaProxy';
function CSPContent(_a) {
    var data = _a.data;
    return (<div>
      <h4>
        <span>{data.effective_directive}</span>
      </h4>
      <KeyValueList data={Object.entries(data).map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                subject: key,
                value: value,
                meta: getMeta(data, key),
            });
        })} isContextData/>
    </div>);
}
export default CSPContent;
//# sourceMappingURL=cspContent.jsx.map