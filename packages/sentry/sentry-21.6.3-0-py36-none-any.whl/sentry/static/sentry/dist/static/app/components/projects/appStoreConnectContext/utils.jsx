import moment from 'moment';
import { t } from 'app/locale';
export var appStoreConnectAlertMessage = {
    iTunesSessionInvalid: t('The iTunes session of your configured App Store Connect has expired.'),
    appStoreCredentialsInvalid: t('The credentials of your configured App Store Connect are invalid.'),
    isTodayAfterItunesSessionRefreshAt: t('The iTunes session of your configured App Store Connect will likely expire soon.'),
};
export function getAppConnectStoreUpdateAlertMessage(appConnectValidationData) {
    if (appConnectValidationData.itunesSessionValid === false) {
        return appStoreConnectAlertMessage.iTunesSessionInvalid;
    }
    if (appConnectValidationData.appstoreCredentialsValid === false) {
        return appStoreConnectAlertMessage.appStoreCredentialsInvalid;
    }
    var itunesSessionRefreshAt = appConnectValidationData.itunesSessionRefreshAt;
    if (!itunesSessionRefreshAt) {
        return undefined;
    }
    var isTodayAfterItunesSessionRefreshAt = moment().isAfter(moment(itunesSessionRefreshAt));
    if (!isTodayAfterItunesSessionRefreshAt) {
        return undefined;
    }
    return appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt;
}
//# sourceMappingURL=utils.jsx.map