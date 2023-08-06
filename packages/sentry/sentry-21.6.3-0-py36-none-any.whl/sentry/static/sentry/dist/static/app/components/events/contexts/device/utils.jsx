import { __assign, __read } from "tslib";
import { defined, formatBytesBase2 } from 'app/utils';
import { DeviceKnownDataType } from './types';
export function formatMemory(memory_size, free_memory, usable_memory) {
    if (!Number.isInteger(memory_size) ||
        memory_size <= 0 ||
        !Number.isInteger(free_memory) ||
        free_memory <= 0) {
        return null;
    }
    var memory = "Total: " + formatBytesBase2(memory_size) + " / Free: " + formatBytesBase2(free_memory);
    if (Number.isInteger(usable_memory) && usable_memory > 0) {
        memory = memory + " / Usable: " + formatBytesBase2(usable_memory);
    }
    return memory;
}
export function formatStorage(storage_size, free_storage, external_storage_size, external_free_storage) {
    if (!Number.isInteger(storage_size) || storage_size <= 0) {
        return null;
    }
    var storage = "Total: " + formatBytesBase2(storage_size);
    if (Number.isInteger(free_storage) && free_storage > 0) {
        storage = storage + " / Free: " + formatBytesBase2(free_storage);
    }
    if (Number.isInteger(external_storage_size) &&
        external_storage_size > 0 &&
        Number.isInteger(external_free_storage) &&
        external_free_storage > 0) {
        storage = storage + " (External Total: " + formatBytesBase2(external_storage_size) + " / Free: " + formatBytesBase2(external_free_storage) + ")";
    }
    return storage;
}
// List of common display resolutions taken from the source: https://en.wikipedia.org/wiki/Display_resolution#Common_display_resolutions
export var commonDisplayResolutions = {
    '640x360': 'nHD',
    '800x600': 'SVGA',
    '1024x768': 'XGA',
    '1280x720': 'WXGA',
    '1280x800': 'WXGA',
    '1280x1024': 'SXGA',
    '1360x768': 'HD',
    '1366x768': 'HD',
    '1440x900': 'WXGA+',
    '1536x864': 'NA',
    '1600x900': 'HD+',
    '1680x1050': 'WSXGA+',
    '1920x1080': 'FHD',
    '1920x1200': 'WUXGA',
    '2048x1152': 'QWXGA',
    '2560x1080': 'N/A',
    '2560x1440': 'QHD',
    '3440x1440': 'N/A',
    '3840x2160': '4K UHD',
};
export function getInferredData(data) {
    var _a, _b, _c;
    var screenResolution = data[DeviceKnownDataType.SCREEN_RESOLUTION];
    var screenWidth = data[DeviceKnownDataType.SCREEN_WIDTH_PIXELS];
    var screenHeight = data[DeviceKnownDataType.SCREEN_HEIGHT_PIXELS];
    if (screenResolution) {
        var displayResolutionDescription = commonDisplayResolutions[screenResolution];
        var commonData = __assign(__assign({}, data), (_a = {}, _a[DeviceKnownDataType.SCREEN_RESOLUTION] = displayResolutionDescription
            ? screenResolution + " (" + displayResolutionDescription + ")"
            : screenResolution, _a));
        if (!defined(screenWidth) && !defined(screenHeight)) {
            var _d = __read(screenResolution.split('x'), 2), width = _d[0], height = _d[1];
            if (width && height) {
                return __assign(__assign({}, commonData), (_b = {}, _b[DeviceKnownDataType.SCREEN_WIDTH_PIXELS] = Number(width), _b[DeviceKnownDataType.SCREEN_HEIGHT_PIXELS] = Number(height), _b));
            }
        }
        return commonData;
    }
    if (defined(screenWidth) && defined(screenHeight)) {
        var displayResolution = screenWidth + "x" + screenHeight;
        var displayResolutionDescription = commonDisplayResolutions[displayResolution];
        return __assign(__assign({}, data), (_c = {}, _c[DeviceKnownDataType.SCREEN_RESOLUTION] = displayResolutionDescription
            ? displayResolution + " (" + displayResolutionDescription + ")"
            : displayResolution, _c));
    }
    return data;
}
//# sourceMappingURL=utils.jsx.map