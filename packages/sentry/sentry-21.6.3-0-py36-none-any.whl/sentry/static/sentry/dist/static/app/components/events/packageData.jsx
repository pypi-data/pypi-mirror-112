import { __extends, __read } from "tslib";
import { Component } from 'react';
import ClippedBox from 'app/components/clippedBox';
import ErrorBoundary from 'app/components/errorBoundary';
import EventDataSection from 'app/components/events/eventDataSection';
import KeyValueList from 'app/components/events/interfaces/keyValueList';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { t } from 'app/locale';
var EventPackageData = /** @class */ (function (_super) {
    __extends(EventPackageData, _super);
    function EventPackageData() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventPackageData.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event.id !== nextProps.event.id;
    };
    EventPackageData.prototype.render = function () {
        var event = this.props.event;
        var longKeys, title;
        var packages = Object.entries(event.packages || {}).map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: key,
                meta: getMeta(event.packages, key),
            });
        });
        switch (event.platform) {
            case 'csharp':
                longKeys = true;
                title = t('Assemblies');
                break;
            default:
                longKeys = false;
                title = t('Packages');
        }
        return (<EventDataSection type="packages" title={title}>
        <ClippedBox>
          <ErrorBoundary mini>
            <KeyValueList data={packages} longKeys={longKeys}/>
          </ErrorBoundary>
        </ClippedBox>
      </EventDataSection>);
    };
    return EventPackageData;
}(Component));
export default EventPackageData;
//# sourceMappingURL=packageData.jsx.map