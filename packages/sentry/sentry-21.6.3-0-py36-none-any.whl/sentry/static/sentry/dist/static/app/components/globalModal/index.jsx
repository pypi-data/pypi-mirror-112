import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import ReactDOM from 'react-dom';
import { browserHistory } from 'react-router';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import { createFocusTrap } from 'focus-trap';
import { AnimatePresence, motion } from 'framer-motion';
import { closeModal as actionCloseModal } from 'app/actionCreators/modal';
import { ROOT_ELEMENT } from 'app/constants';
import ModalStore from 'app/stores/modalStore';
import space from 'app/styles/space';
import getModalPortal from 'app/utils/getModalPortal';
import testableTransition from 'app/utils/testableTransition';
import { makeClosableHeader, makeCloseButton, ModalBody, ModalFooter } from './components';
function GlobalModal(_a) {
    var _b;
    var _c = _a.visible, visible = _c === void 0 ? false : _c, _d = _a.options, options = _d === void 0 ? {} : _d, children = _a.children, onClose = _a.onClose;
    var closeModal = React.useCallback(function () {
        var _a;
        // Option close callback, from the thing which opened the modal
        (_a = options.onClose) === null || _a === void 0 ? void 0 : _a.call(options);
        // Action creator, actually closes the modal
        actionCloseModal();
        // GlobalModal onClose prop callback
        onClose === null || onClose === void 0 ? void 0 : onClose();
    }, [options]);
    var handleEscapeClose = React.useCallback(function (e) { return e.key === 'Escape' && closeModal(); }, [closeModal]);
    var portal = getModalPortal();
    var focusTrap = React.useRef();
    // SentryApp might be missing on tests
    if (window.SentryApp) {
        window.SentryApp.modalFocusTrap = focusTrap;
    }
    React.useEffect(function () {
        focusTrap.current = createFocusTrap(portal, {
            preventScroll: true,
            escapeDeactivates: false,
            fallbackFocus: portal,
        });
    }, [portal]);
    React.useEffect(function () {
        var _a;
        var body = document.querySelector('body');
        var root = document.getElementById(ROOT_ELEMENT);
        if (!body || !root) {
            return function () { return void 0; };
        }
        var reset = function () {
            var _a;
            body.style.removeProperty('overflow');
            root.removeAttribute('aria-hidden');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.deactivate();
            portal.removeEventListener('keydown', handleEscapeClose);
        };
        if (visible) {
            body.style.overflow = 'hidden';
            root.setAttribute('aria-hidden', 'true');
            (_a = focusTrap.current) === null || _a === void 0 ? void 0 : _a.activate();
            portal.addEventListener('keydown', handleEscapeClose);
        }
        else {
            reset();
        }
        return reset;
    }, [portal, handleEscapeClose, visible]);
    var renderedChild = children === null || children === void 0 ? void 0 : children({
        CloseButton: makeCloseButton(closeModal),
        Header: makeClosableHeader(closeModal),
        Body: ModalBody,
        Footer: ModalFooter,
        closeModal: closeModal,
    });
    // Default to enabled backdrop
    var backdrop = (_b = options.backdrop) !== null && _b !== void 0 ? _b : true;
    // Only close when we directly click outside of the modal.
    var containerRef = React.useRef(null);
    var clickClose = function (e) {
        return containerRef.current === e.target && closeModal();
    };
    return ReactDOM.createPortal(<React.Fragment>
      <Backdrop style={backdrop && visible ? { opacity: 0.5, pointerEvents: 'auto' } : {}}/>
      <Container ref={containerRef} style={{ pointerEvents: visible ? 'auto' : 'none' }} onClick={backdrop === true ? clickClose : undefined}>
        <AnimatePresence>
          {visible && (<Modal role="dialog" css={options.modalCss}>
              <Content role="document">{renderedChild}</Content>
            </Modal>)}
        </AnimatePresence>
      </Container>
    </React.Fragment>, portal);
}
var fullPageCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"], ["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"])));
var Backdrop = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  background: ", ";\n  will-change: opacity;\n  transition: opacity 200ms;\n  pointer-events: none;\n  opacity: 0;\n"], ["\n  ", ";\n  z-index: ", ";\n  background: ", ";\n  will-change: opacity;\n  transition: opacity 200ms;\n  pointer-events: none;\n  opacity: 0;\n"])), fullPageCss, function (p) { return p.theme.zIndex.modal; }, function (p) { return p.theme.gray500; });
var Container = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  overflow-y: auto;\n"], ["\n  ", ";\n  z-index: ", ";\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  overflow-y: auto;\n"])), fullPageCss, function (p) { return p.theme.zIndex.modal; });
var Modal = styled(motion.div)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 640px;\n  pointer-events: auto;\n  padding: 80px ", " ", " ", ";\n"], ["\n  width: 640px;\n  pointer-events: auto;\n  padding: 80px ", " ", " ", ";\n"])), space(2), space(4), space(2));
Modal.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 15 },
    transition: testableTransition({
        opacity: { duration: 0.2 },
        y: { duration: 0.25 },
    }),
};
var Content = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", ";\n  background: ", ";\n  border-radius: 8px;\n  border: ", ";\n  box-shadow: ", ";\n"], ["\n  padding: ", ";\n  background: ", ";\n  border-radius: 8px;\n  border: ", ";\n  box-shadow: ", ";\n"])), space(4), function (p) { return p.theme.background; }, function (p) { return p.theme.modalBorder; }, function (p) { return p.theme.modalBoxShadow; });
var GlobalModalContainer = /** @class */ (function (_super) {
    __extends(GlobalModalContainer, _super);
    function GlobalModalContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            modalStore: ModalStore.get(),
        };
        _this.unlistener = ModalStore.listen(function (modalStore) { return _this.setState({ modalStore: modalStore }); }, undefined);
        return _this;
    }
    GlobalModalContainer.prototype.componentDidMount = function () {
        // Listen for route changes so we can dismiss modal
        this.unlistenBrowserHistory = browserHistory.listen(function () { return actionCloseModal(); });
    };
    GlobalModalContainer.prototype.componentWillUnmount = function () {
        var _a, _b;
        (_a = this.unlistenBrowserHistory) === null || _a === void 0 ? void 0 : _a.call(this);
        (_b = this.unlistener) === null || _b === void 0 ? void 0 : _b.call(this);
    };
    GlobalModalContainer.prototype.render = function () {
        var modalStore = this.state.modalStore;
        var visible = !!modalStore && typeof modalStore.renderer === 'function';
        return (<GlobalModal {...this.props} {...modalStore} visible={visible}>
        {visible ? modalStore.renderer : null}
      </GlobalModal>);
    };
    return GlobalModalContainer;
}(React.Component));
export default GlobalModalContainer;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map