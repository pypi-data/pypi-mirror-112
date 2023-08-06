import { __awaiter, __generator, __rest } from "tslib";
import * as React from 'react';
import ModalActions from 'app/actions/modalActions';
/**
 * Show a modal
 */
export function openModal(renderer, options) {
    ModalActions.openModal(renderer, options);
}
/**
 * Close modal
 */
export function closeModal() {
    ModalActions.closeModal();
}
export function openSudo(_a) {
    if (_a === void 0) { _a = {}; }
    var onClose = _a.onClose, args = __rest(_a, ["onClose"]);
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/sudoModal')];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...args}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
export function openEmailVerification(_a) {
    if (_a === void 0) { _a = {}; }
    var onClose = _a.onClose, args = __rest(_a, ["onClose"]);
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/emailVerificationModal')];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...args}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
export function openDiffModal(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/diffModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openCreateTeamModal(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/createTeamModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
export function openCreateOwnershipRule(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/createOwnershipRuleModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openEditOwnershipRules(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/editOwnershipRulesModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { backdrop: 'static', modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openCommandPalette(options) {
    if (options === void 0) { options = {}; }
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/commandPalette')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openRecoveryOptions(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/recoveryOptionsModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
export function openTeamAccessRequestModal(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/teamAccessRequestModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; });
                    return [2 /*return*/];
            }
        });
    });
}
export function redirectToProject(newProjectSlug) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/redirectToProject')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} slug={newProjectSlug}/>; }, {});
                    return [2 /*return*/];
            }
        });
    });
}
export function openHelpSearchModal(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/helpSearchModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openDebugFileSourceModal(_a) {
    var onClose = _a.onClose, restOptions = __rest(_a, ["onClose"]);
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, import(
                    /* webpackChunkName: "DebugFileCustomRepository" */ 'app/components/modals/debugFileCustomRepository')];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...restOptions}/>; }, {
                        modalCss: modalCss,
                        onClose: onClose,
                    });
                    return [2 /*return*/];
            }
        });
    });
}
export function openInviteMembersModal(options) {
    if (options === void 0) { options = {}; }
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/inviteMembersModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openAddDashboardWidgetModal(options) {
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal, modalCss;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/addDashboardWidgetModal')];
                case 1:
                    mod = _a.sent();
                    Modal = mod.default, modalCss = mod.modalCss;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { backdrop: 'static', modalCss: modalCss });
                    return [2 /*return*/];
            }
        });
    });
}
export function openReprocessEventModal(_a) {
    var onClose = _a.onClose, options = __rest(_a, ["onClose"]);
    return __awaiter(this, void 0, void 0, function () {
        var mod, Modal;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, import('app/components/modals/reprocessEventModal')];
                case 1:
                    mod = _b.sent();
                    Modal = mod.default;
                    openModal(function (deps) { return <Modal {...deps} {...options}/>; }, { onClose: onClose });
                    return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=modal.jsx.map