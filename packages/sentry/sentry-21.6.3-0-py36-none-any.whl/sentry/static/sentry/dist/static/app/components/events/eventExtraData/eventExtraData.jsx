import { __read } from "tslib";
import { memo, useState } from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import { t } from 'app/locale';
import EventDataContent from './eventDataContent';
var EventExtraData = memo(function (_a) {
    var event = _a.event;
    var _b = __read(useState(false), 2), raw = _b[0], setRaw = _b[1];
    return (<EventDataSection type="extra" title={t('Additional Data')} toggleRaw={function () { return setRaw(!raw); }} raw={raw}>
        <EventDataContent raw={raw} data={event.context}/>
      </EventDataSection>);
}, function (prevProps, nextProps) { return prevProps.event.id !== nextProps.event.id; });
export default EventExtraData;
//# sourceMappingURL=eventExtraData.jsx.map