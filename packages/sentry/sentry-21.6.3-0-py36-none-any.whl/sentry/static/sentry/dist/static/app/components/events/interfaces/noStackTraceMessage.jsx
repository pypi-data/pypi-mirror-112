import Alert from 'app/components/alert';
import { t } from 'app/locale';
function NoStackTraceMessage(_a) {
    var message = _a.message;
    return <Alert type="error">{message !== null && message !== void 0 ? message : t('No or unknown stacktrace')}</Alert>;
}
export default NoStackTraceMessage;
//# sourceMappingURL=noStackTraceMessage.jsx.map