import { __read } from "tslib";
import EventDataSection from 'app/components/events/eventDataSection';
import KeyValueList from 'app/components/events/interfaces/keyValueList';
import Annotated from 'app/components/events/meta/annotated';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { t } from 'app/locale';
import { objectIsEmpty } from 'app/utils';
var Message = function (_a) {
    var data = _a.data;
    var renderParams = function () {
        var params = data === null || data === void 0 ? void 0 : data.params;
        if (!params || objectIsEmpty(params)) {
            return null;
        }
        // NB: Always render params, regardless of whether they appear in the
        // formatted string due to structured logging frameworks, like Serilog. They
        // only format some parameters into the formatted string, but we want to
        // display all of them.
        if (Array.isArray(params)) {
            var arrayData = params.map(function (value, i) {
                var key = "#" + i;
                return {
                    key: key,
                    value: value,
                    subject: key,
                };
            });
            return <KeyValueList data={arrayData} isSorted={false} isContextData/>;
        }
        var objectData = Object.entries(params).map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: key,
                meta: getMeta(params, key),
            });
        });
        return <KeyValueList data={objectData} isSorted={false} isContextData/>;
    };
    return (<EventDataSection type="message" title={t('Message')}>
      <Annotated object={data} objectKey="formatted">
        {function (value) { return <pre className="plain">{value}</pre>; }}
      </Annotated>
      {renderParams()}
    </EventDataSection>);
};
export default Message;
//# sourceMappingURL=message.jsx.map