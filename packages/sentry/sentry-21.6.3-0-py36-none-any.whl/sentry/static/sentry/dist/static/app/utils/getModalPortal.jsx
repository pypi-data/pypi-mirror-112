import memoize from 'lodash/memoize';
var getModalPortal = memoize(function () {
    var portal = document.getElementById('modal-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'modal-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
export default getModalPortal;
//# sourceMappingURL=getModalPortal.jsx.map