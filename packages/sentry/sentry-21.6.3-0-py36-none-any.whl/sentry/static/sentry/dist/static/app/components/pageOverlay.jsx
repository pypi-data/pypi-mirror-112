import { __extends, __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import Text from 'app/components/text';
import space from 'app/styles/space';
import testableTransition from 'app/utils/testableTransition';
/**
 * The default wrapper for the detail text.
 *
 * This can be overridden using the `customWrapper` prop for when the overlay
 * needs some special sizing due to background illustration constraints.
 */
var DefaultWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 500px;\n"], ["\n  width: 500px;\n"])));
var subItemAnimation = {
    initial: {
        opacity: 0,
        x: 60,
    },
    animate: {
        opacity: 1,
        x: 0,
        transition: testableTransition({
            type: 'spring',
            duration: 0.4,
        }),
    },
};
var Header = styled(motion.h2)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-weight: normal;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  font-weight: normal;\n  margin-bottom: ", ";\n"])), space(1));
Header.defaultProps = {
    variants: subItemAnimation,
    transition: testableTransition(),
};
var Body = styled(motion.div)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
Body.defaultProps = {
    variants: subItemAnimation,
    transition: testableTransition(),
};
/**
 * When a background with a anchor is used and no positioningStrategy is
 * provided, by default we'll align the top left of the container to the anchor
 */
var defaultPositioning = function (_a) {
    var mainRect = _a.mainRect, anchorRect = _a.anchorRect;
    return ({
        x: anchorRect.x - mainRect.x,
        y: anchorRect.y - mainRect.y,
    });
};
/**
 * Wrapper component that will render the wrapped content with an animated
 * overlay.
 *
 * If children are given they will be placed behind the overlay and hidden from
 * pointer events.
 *
 * If a background is given, the background will be rendered _above_ any
 * children (and will receive framer-motion variant changes for animations).
 * The background may also provide a `anchorRef` to aid in alignment of the
 * wrapper to a safe space in the background to aid in alignment of the wrapper
 * to a safe space in the background.
 */
var PageOverlay = /** @class */ (function (_super) {
    __extends(PageOverlay, _super);
    function PageOverlay() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Used to re-anchor the text wrapper to the anchor point in the background when
         * the size of the page changes.
         */
        _this.bgResizeObserver = null;
        _this.contentRef = React.createRef();
        _this.wrapperRef = React.createRef();
        _this.anchorRef = React.createRef();
        /**
         * Align the wrapper component to the anchor by computing x/y values using
         * the passed function. By default if no function is specified it will align
         * to the top left of the anchor.
         */
        _this.anchorWrapper = function () {
            if (_this.contentRef.current === null ||
                _this.wrapperRef.current === null ||
                _this.anchorRef.current === null) {
                return;
            }
            // Absolute position the container, this avoids the browser having to reflow
            // the component
            _this.wrapperRef.current.style.position = 'absolute';
            _this.wrapperRef.current.style.left = "0px";
            _this.wrapperRef.current.style.top = "0px";
            var mainRect = _this.contentRef.current.getBoundingClientRect();
            var anchorRect = _this.anchorRef.current.getBoundingClientRect();
            var wrapperRect = _this.wrapperRef.current.getBoundingClientRect();
            // Compute the position of the wrapper
            var _a = _this.props.positioningStrategy({ mainRect: mainRect, anchorRect: anchorRect, wrapperRect: wrapperRect }), x = _a.x, y = _a.y;
            var transform = "translate(" + Math.round(x) + "px, " + Math.round(y) + "px)";
            _this.wrapperRef.current.style.transform = transform;
        };
        return _this;
    }
    PageOverlay.prototype.componentDidMount = function () {
        if (this.contentRef.current === null || this.anchorRef.current === null) {
            return;
        }
        this.anchorWrapper();
        // Observe changes to the upsell container to reanchor if available
        if (window.ResizeObserver) {
            this.bgResizeObserver = new ResizeObserver(this.anchorWrapper);
            this.bgResizeObserver.observe(this.contentRef.current);
        }
    };
    PageOverlay.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.bgResizeObserver) === null || _a === void 0 ? void 0 : _a.disconnect();
    };
    PageOverlay.prototype.render = function () {
        var _a = this.props, text = _a.text, children = _a.children, animateDelay = _a.animateDelay, BackgroundComponent = _a.background, customWrapper = _a.customWrapper, props = __rest(_a, ["text", "children", "animateDelay", "background", "customWrapper"]);
        var Wrapper = customWrapper !== null && customWrapper !== void 0 ? customWrapper : DefaultWrapper;
        var transition = testableTransition({
            delay: 1,
            duration: 1.2,
            ease: 'easeInOut',
            delayChildren: animateDelay !== null && animateDelay !== void 0 ? animateDelay : (BackgroundComponent ? 0.5 : 1.5),
            staggerChildren: 0.15,
        });
        return (<MaskedContent {...props}>
        {children}
        <ContentWrapper ref={this.contentRef} transition={transition} variants={{ animate: {} }}>
          {BackgroundComponent && (<Background>
              <BackgroundComponent anchorRef={this.anchorRef}/>
            </Background>)}
          <Wrapper ref={this.wrapperRef}>
            <Text>{text({ Body: Body, Header: Header })}</Text>
          </Wrapper>
        </ContentWrapper>
      </MaskedContent>);
    };
    PageOverlay.defaultProps = {
        positioningStrategy: defaultPositioning,
    };
    return PageOverlay;
}(React.Component));
var absoluteFull = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n"])));
var ContentWrapper = styled(motion.div)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n  padding: 10%;\n  z-index: 900;\n"], ["\n  ", "\n  padding: 10%;\n  z-index: 900;\n"])), absoluteFull);
ContentWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
};
var Background = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", "\n  z-index: -1;\n  padding: 60px;\n  display: flex;\n  align-items: center;\n\n  > * {\n    width: 100%;\n    min-height: 600px;\n    height: 100%;\n  }\n"], ["\n  ", "\n  z-index: -1;\n  padding: 60px;\n  display: flex;\n  align-items: center;\n\n  > * {\n    width: 100%;\n    min-height: 600px;\n    height: 100%;\n  }\n"])), absoluteFull);
var MaskedContent = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: relative;\n  overflow: hidden;\n  flex-grow: 1;\n  flex-basis: 0;\n\n  /* Specify bottom margin specifically to offset the margin of the footer, so\n   * the hidden content flows directly to the border of the footer\n   */\n  margin-bottom: -20px;\n"], ["\n  position: relative;\n  overflow: hidden;\n  flex-grow: 1;\n  flex-basis: 0;\n\n  /* Specify bottom margin specifically to offset the margin of the footer, so\n   * the hidden content flows directly to the border of the footer\n   */\n  margin-bottom: -20px;\n"])));
export default PageOverlay;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=pageOverlay.jsx.map