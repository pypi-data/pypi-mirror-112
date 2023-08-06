/* eslint no-native-reassign:0 */
var _a;
/**
 * Set the webpack public path at runtime. This is necessary so that imports
 * can be resolved properly
 *
 * NOTE: This MUST be loaded before any other app modules in the entrypoint.
 *
 * This may not be as necessary without versioned asset URLs. (Rather, instead of a version directory
 * that is generated on backend, frontend assets will be "versioned" by webpack with a content hash in
 * its filename). This means that the public path does not need to be piped from the backend.
 *
 * XXX(epurkhiser): Currently we only boot with hydration in experimental SPA
 * mode, where assets are *currently not versioned*. We hardcode `/_assets/` here
 * for now as a quick workaround for the index.html being aware of versioned
 * asset paths.
 */
__webpack_public_path__ = ((_a = window.__initialData) === null || _a === void 0 ? void 0 : _a.distPrefix) || '/_assets/';
//# sourceMappingURL=statics-setup.jsx.map